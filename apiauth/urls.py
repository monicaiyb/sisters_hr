from django.urls import path
from .views import LoginApiView, LogoutApiView, RegisterApiView, UserView,UserLoginView
from rest_framework_simplejwt import views as jwt_views



urlpatterns = [
    #     path('/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("loginUser/", UserLoginView.as_view(), name="user_login"),
    path("login/", LoginApiView.as_view(), name="login"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    path("register/", RegisterApiView.as_view(), name="register"),
     path('user/', UserView.as_view()),
]