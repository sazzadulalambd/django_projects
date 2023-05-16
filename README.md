<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/Django?style=plastic">
# django_projects
1. Install Django by running the following command in your terminal:
``` 
pip install django

```

2. Create a new Django project by running the following command in your terminal:
``` 
django-admin startproject myproject
```

3. Create a new Django app by running the following command in your terminal:
``` 
cd myproject
python manage.py startapp myapp
```

4. Open the myproject/settings.py file and add the following lines to the INSTALLED_APPS list:
``` 
'myapp',
```

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
        
6. Run the following command in your terminal to create the database table for your model:

```
python manage.py makemigrations myapp
python manage.py migrate
```

7. Open the myapp/forms.py file and define a form that corresponds to your model:

```
from django import forms
from .models import MyModel

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['name', 'email', 'phone']
```

8. Open the myapp/urls.py file

```
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create', views.create, name="create"),
    path('list', views.list, name="list"),
    path('update', views.update, name="update"),
    path('delete', views.delete, name="delete"),
    
]
```

9. Open the myapp/views.py file and define the views for your CRUD functionality:

```
from django.shortcuts import render, redirect, get_object_or_404
from .models import MyModel
from .forms import MyModelForm

def create(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = MyModelForm()
    return render(request, 'create.html', {'form': form})


def list(request):
    mymodels = MyModel.objects.all()
    return render(request, 'list.html', {'mymodels': mymodels})


def update(request, pk):
    mymodel = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, instance=mymodel)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = MyModelForm(instance=mymodel)
    return render(request, 'update.html', {'form': form})


def delete(request, pk):
    mymodel = get_object_or_404(MyModel, pk=pk)
    mymodel.delete()
    return redirect('list')
```

10. Create the HTML templates for your views. For example, create **create.html:**

```
{% extends 'base.html' %}

{% block content %}

<h1>Create a new model</h1>

<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>

<a href="{% url 'list' %}">Back to list</a>

{% endblock %}
```
 
In this example, we're extending a base template called ```'base.html'```, which could include common elements like a header, footer, or navigation menu. The ```content``` block is where we'll put the form for creating a new person.

We've created an HTML form that uses the POST method to submit the form data to the server. We've also included the ```enctype="multipart/form-data"``` attribute, which is required when the form includes file uploads.

Inside the form, we're using the Django template tag `csrf_token` to add a security token to the form. This is a required security measure in Django to prevent Cross-Site Request Forgery (CSRF) attacks.

To display the form fields, we're using the ```{{ form.as_p }}``` template tag, which will render the form fields as paragraphs (```<p>```) with labels and input fields. You could also use ```{{ form.as_table }}``` to render the fields in a table, or ```{{ form.as_ul }}``` to render them as an unordered list.
 

**list.html:**

```
{% extends 'base.html' %}

{% block content %}

<h1>My models</h1>

<ul>
 ```
 
**base.html**
 
 ```
 <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}{% endblock %}</title>
</head>
<body>
  <header>
    <h1>My App</h1>
    <nav>
      <ul>
        <li><a href="{% url 'home' %}">Home</a></li>
        <li><a href="{% url 'create' %}">Add Person</a></li>
      </ul>
    </nav>
  </header>
  <main>
    {% block content %}{% endblock %}
  </main>
  <footer>
    &copy; My App {{ year }}
  </footer>
</body>
</html>
 
```
