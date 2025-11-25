# Nombre del Proyecto Marketplace

# SignUp y Login en Forms.py

```python

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Item

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu usuario',
            'class': 'form-control'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'password',
            'class': 'form-control'
        }
    ))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu Usuario',
            'class': 'form-control'
        }
    ))

    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Tu Email',
            'class': 'form-control'
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repite Password',
            'class': 'form-control'
        }
    ))



{% extends 'store/base.html' %}

{% block title %}Registro | {% endblock %}

{% block content %}
<div class ="row p-4">
    <div class="col-6 bg-light p-4">
        <h4 class="mb-6 text-center">Registro</h4>
        <hr>
        <form action="." method="POST">
            {% crsf_token %}
            <div class="form-floating mb-3">
                <h6>Username:</h6>
                {{form.username}}
            </div>
            <div class="form-floating mb-3">
                <h6>Email:</h6>
                {{form.email}}
            </div>
            <div class="form-floating mb-3">
                <h6>Password:</h6>
                {{form.password1}}
            </div>
            <div class="form-floating mb-3">
                <h6>Repite Password:</h6>
                {{form.password2}}
            </div>

            {% if form.errors or form.non_field_errors %}
                <div class="mb-4 p-6 bg-danger">
                    {% for field in form %}
                        field.errors
                    {% endfor %}
                    {{ form.non_field_errors }}
                </div>
            {% endif %}
            <button class="btn btn-primary mb-6">Register</button>
        </form>
    </div>
</div>
{% endblock %}

```

# Funciones en Views.py

```python

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout

from .models import Item, Category

from .forms import SignupForm

# Create your views here.
def home(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    context = {
        'items': items,
        'categories': categories
    }
    return render(request, 'store/home.html', context)

def contact(request):
    context = {
        'msg': 'Quieres otros productos contactame!'
    }

    return render(request, 'store/contact.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    context={
        'item': item,
        'related_items': related_items
    }

    return render(request, 'store/item.html', context)

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()

    context = {
        'form': form
    }

    return render(request, 'store/signup.html', context)

```

# Login, Register urls.py

```python

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import contact, detail, register

from .forms import LoginForm

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm)),
    path('detail/<int:pk>/', detail, name='detail'),
]

```

# Templates templates/store login, signup

```python

{% extends 'store/base.html' %}

{% block title %}Login| {% endblock %}

{% block content %}

<div class="row p-4">
    <div class="col-6 bg-light p-4">
        <h4 class="mb-6 text-center">Registro</h4>
        <hr>
        <form action="." method="POST">
            {% csrf_token %}
            <div class="form-floating mb-3">
                <h6>Username:</h6>
                {{form.username}}
            </div>
            <div class="form-floating mb-3">
                <h6>Password:</h6>
                {{form.password}}
            </div>
        </form>
    </div>
    {% if form.errors or form.non_field_errors %}
    <div class="mb-4 p-6 bg-danger">
        {% for field in form %}
            fiels.errors
        {% endfor %}
        {{ form.non_field_errors }}
    </div>
    {% endif %}
</div>
<button class="btn btn-primary mb-6">Login</button>

{% endblock %}


{% extends 'store/base.html' %}

{% block title %}Registro| {% endblock %}

{% block content %}
<div class="row p-4">
    <div class="col-6 bg-light p-4">
        <h4 class="mb-6 text-center">Registro</h4>
        <hr>
        <form action="." method="POST">
            {% csrf_token %}
            <div class="form-floating mb-3">
                <h6>Username:</h6>
                {{form.username}}
            </div>
            <div class="form-floating mb-3">
                <h6>Email:</h6>
                {{form.email}}
            </div>
            <div class="form-floating mb-3">
                <h6>Password:</h6>
                {{form.password1}}
            </div>
            <div class="form-floating mb-3">
                <h6>Repite Password:</h6>
                {{form.password2}}
            </div>

            {% if form.errors or form.non_field_errors %}
                <div class="mb-4 p-6 bg-danger">
                    {% for field in form %}
                        fields.errors
                    {% endfor %}
                    {{ form.non_field_errors }}
                </div>
            {% endif %}

            <button class="btn btn-primary mb-6">Register</button>
        </form>
    </div>
</div>
{% endblock %}

```

# forms.py modificado

```python

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Item

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu usuario',
            'class': 'form-control'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'password',
            'class': 'form-control'
        }
    ))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Tu Usuario',
            'class': 'form-control'
        }
    ))

    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Tu Email',
            'class': 'form-control'
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repite Password',
            'class': 'form-control'
        }
    ))

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 100px'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }

```

# views.py modificado

```python

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Item, Category

from .forms import SignupForm
from .forms import NewItemForm

# Create your views here.
def home(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    context = {
        'items': items,
        'categories': categories
    }
    return render(request, 'store/home.html', context)

def contact(request):
    context = {
        'msg': 'Quieres otros productos contactame!'
    }

    return render(request, 'store/contact.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    context={
        'item': item,
        'related_items': related_items
    }

    return render(request, 'store/item.html', context)

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()

    context = {
        'form': form
    }

    return render(request, 'store/signup.html', context)

def logout_user(request):
    logout(request)

    return redirect('home')

@login_required
def add_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('detail', pk=item.id)
    else:
        form = NewItemForm()

    context = {
        'form': form,
        'title': 'New Item'
    }

    return render(request, 'store/form.html', context)


```

# creamos form.html en templates

```python

{% extends 'store/base.html' %}

{% block title %} {{ title }} {% endblock %}

{% block content%}
    <h4 class="mb-4 mt-4">{{ title }}</h4>
    <hr>
    <form action="." method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        <div>
        
            {{ form.as_p }}
        </div>

        {% if form.errors or form.non_field_errors %}
            <div class="mb-4 p-6 bg-danger">
                {% for field in form %}
                    {{ field.errors }}
                {% endfor %}

                {{ form.non_field_errors }}
            </div>
        {% endif %}

        <button class="btn btn-primary mb-6">Register</button>
    </form>
{% endblock%}

```

# urls.py modificado

```python

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, contact, detail, register, logout_user, add_item

from .forms import LoginForm

urlpatterns = [
    path ('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', logout_user, name= "logout"),
    path('add_item/', add_item, name='add_item'),
    path('detail/<int:pk>/', detail, name='detail'),
]


```

# navigation.html modificado

```python

<nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
    <div class="container-fluid">
        <a href="{% url 'home' %}" class="navbar-brand">Marketplace</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-control="navBarNav" aria-expanded="false" aria-label="Toggle Navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a href="" class="nav-link active">
                        Home
                    </a>
                </li>
                <li class="nav-item">
                    <a href="{% url 'contact' %}" class="nav-link active">
                        Contact
                    </a>
                </li>
               
                {% if request.user.is_authenticated %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'add_item'%}">Add Item</a>
                    </li>
                    <li class="nav-item">
                        <a href="{% url 'logout' %}" class="nav-link active">
                            Logout
                        </a>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a href="{% url 'login' %}" class="nav-link active">
                            Login
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="{% url 'register' %}" class="nav-link active">
                            Register
                        </a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>

```