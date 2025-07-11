from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (LoginSerializer, RegisterSerializer, UserSerializer,   
                          ResendEmailVerificationSerializer,ChangePasswordSerializer,
    ResetPasswordSerializer,
    SetPasswordSerializer)
from employees.serializers import EmployeeSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token 
import jwt
import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication

class LogoutApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Logout class
        """
        logout(request)
        return Response(
            {"non_field_errors": "successfully logged out"},
            status=status.HTTP_200_OK,
        )


class RegisterApiView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Register class
        """

        serializer = RegisterSerializer(data=request.data, many=False)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password1"]
            user = User.objects.create_user(
                username=username, password=password
            )
            authenticate(request, username=username, password=password)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Login view to get user credentials
        """
        email = request.data['email']
        password = request.data['password']

        #find user using email
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found:)')
            
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')

       
        payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        # token.decode('utf-8')
        #we set token via cookies
        

        response = Response() 

        response.set_cookie(key='jwt', value=token, httponly=True)  #httonly - frontend can't access cookie, only for backend

        response.data = {
            'jwt token': token
        }

        #if password correct
        return response
    

    # get user using cookie

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }

            if user.role == 'employee':
                employee = user.employee  # Assuming the related name is "student_account"
                if employee is not None:
                    # Add student data to the response data
                    employee_data = EmployeeSerializer(employee).data
                    response_data['data'] = employee_data

            return Response(response_data)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class EmailVerificationAPIView(APIView):
    """Confirm users email"""

    def get(self, request, token):
        # Decode the token to get the user id
        user_id = token_decoder(token)
        # Attempt to retrieve the user and activate the account
        try:
            user = get_object_or_404(User, pk=user_id)
            if user.is_verified:
                return Response(
                    {"message": "You are already verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response(
                {"message": "Account activated successfully!"},
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {"error": "Activation link is invalid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TypeError:
            return Response(user_id)


class ResendEmailVerificationAPIView(APIView):
    """Resend a verification email to user"""

    permission_classes = [permissions.AllowAny]
    serializer_class = ResendEmailVerificationSerializer

    def post(self, request):
        serializer = ResendEmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            # Get user from serilizer validate method
            user = serializer.validated_data["user"]
            # Generate a jwt token for resend confirm email
            token = token_generator(user)
            # Resending confirm email token
            confirm_url = self.request.build_absolute_uri(
                reverse("confirm_email", kwargs={"token": token["access"]})
            )
            msg = f"for confirm email click on: {confirm_url}"
            email_obj = EmailMessage("Confirm email", msg, to=[user.email])
            # Sending email with threading
            EmailThread(email_obj).start()
            return Response(
                {"message: The activation email has been sent again successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    """Change user password"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Get current user
            user: User = User.objects.get(id=self.request.user.id)
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]
            # Old password is correct
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "Your password has been changed successfully!"},
                    status=status.HTTP_200_OK,
                )
            # Old password is not correct
            else:
                return Response({"error": "Your old password is not correct"})
        # Serializer is not valid
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    """Reset user password"""

    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user: User = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "User does not exist!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Generate a jwt token for reset password
            token = token_generator(user)
            # Sending reset password email token
            set_password_url = self.request.build_absolute_uri(
                reverse("set_password", kwargs={"token": token["access"]})
            )
            msg = f"for reset password click on: {set_password_url}"
            email_obj = EmailMessage("Set password", msg, to=[user.email])
            # Sending email with threading
            EmailThread(email_obj).start()
            return Response(
                {"message: Reset password email has been sent!"},
                status=status.HTTP_200_OK,
            )

        return Response("")


class SetPasswordAPIView(APIView):
    """Set user password"""

    permission_classes = [permissions.AllowAny]
    serializer_class = SetPasswordSerializer

    def post(self, request, token):
        serializer = SetPasswordSerializer(data=request.data)
        # Decode the token to get the user id
        user_id = token_decoder(token)

        try:
            user = get_object_or_404(User, pk=user_id)
        except Http404:
            return Response(
                {"error": "Activation link is invalid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Token is not valid or expired
        except TypeError:
            return Response(user_id)

        if serializer.is_valid():
            new_password = serializer.validated_data["new_password"]
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Your password has been changed successfully!"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")
            #decode gets the user

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
        #cookies accessed if preserved