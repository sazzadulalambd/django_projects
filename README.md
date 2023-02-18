# django_projects
1. Install Django by running the following command in your terminal:
``` pip install django ```

2. Create a new Django project by running the following command in your terminal:
``` django-admin startproject myproject ```

3. Create a new Django app by running the following command in your terminal:
``` 
cd myproject
python manage.py startapp myapp
```

4. Open the myproject/settings.py file and add the following lines to the INSTALLED_APPS list:
``` 'myapp', ```

5. Open the myapp/models.py file and define a model that represents the data you want to store in your database:
 ``` 
 from django.db import models
class MyModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
        ```
     
