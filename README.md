# Sisters
Python Project for HR Management. This application uses [Django(5.2.1)](https://www.djangoproject.com/).

## Requirements
1. python >= 3.13.2
2. pip
3. Microsoft sql server - if you do not have this you can use docker.

## Setup
1. Create a virtual environment for python 3.10.2.
2. Install requirements  using a command like this one. `pip install -r requirements.txt`
3. Create a `.env` file following the example in `.env.example`
4. Run migrations. `python manage.py migrate`
5. Run application. `python manage.py runserver`.
Running the application should allow you to hit `http://127.0.0.1:8000` in your browser.

# Environment variables
- `.env` file is where we put all our environment variables for example the database name and password go there.
- The .env file is then read into `settings.py`
- Any secret key that should not be accessible to the public should go to the .env file.
- Any key whose value changes from one environment to another should go to the .env file.
- The .env file should not be part of version control. It is local to the machine the code is on.



Example
```python
class EmployeeList(APIView):
  
    def get(self, request, format=None):
        items = Employee.objects.all()
        serializer = EmployeeSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```

## Database(DB) Models
A django model is a way to define the columns on a table in database. A model is the single, definitive source of 
information about your data. It contains the essential fields and behaviors of the data you’re storing.
Generally, each model maps to a single database table. [Docs](https://docs.djangoproject.com/en/4.0/topics/db/models/)

There are columns/fields that each model will have such as created_at, updated_at, deleted_at. To 
add these to new model simply make use of the mixins created in `common/models.py`

An example
```python
from django.db import models


class Employee(models.Model):
    first_name = models.CharField(
        max_length=255,
    )
    last_name = models.CharField(
        max_length=255,
    )
    other_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    email = models.EmailField(unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```
## Django ORM
Once you’ve created your data models, Django automatically gives you a database-abstraction API that lets you create,
retrieve, update and delete objects. [Docs](https://docs.djangoproject.com/en/4.0/topics/db/queries/)

## Database(DB) Migrations
- Having created a model, you can run migrations like this.
- First you prepare the migration using the command. `python manage.py makemigrations`. This will create migration file.
- You can review the migration and file and if that is okay. You can go ahead and apply the migrations.
- To apply migrations use this command. `python manage.py migrate`. This applies the changes made.

## Docker
- Included is a docker container that has a microsoft sql server database that can be used for development purposes.
- This docker container is not intended for production but rather for local development.
- A few useful commands to get you started.
- Start container. Assumes you have docker installed on your computer. Run command. `docker-compose up`
- You can then get into the container and interact with the sql server using the command. `docker-compose exec db bash`
- Once in the container you get to the server using this command. `/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'Your_password123'`
- You can then create a database with these commands.
```sql
 CREATE DATABASE SistersHrDb;
 GO
```

## Super admin user
- To create a superuser you can use the command. `create superuser`.
- Follow along the commands.
- This will allow you to login when you hit /bankadmin.
Happy coding.