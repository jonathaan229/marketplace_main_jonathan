</div>
</nav>

```
```



# Proyecto Marketplace – Documentación Parcial 3  
**Tecnologías:** Django · Python · HTML · Bootstrap  

---

## Introducción  
Django es un framework de desarrollo web basado en Python que permite crear aplicaciones completas de forma rápida y segura. Destaca porque ofrece herramientas listas para usar y funciones integradas para manejo de usuarios, bases de datos, rutas, formularios y un panel administrativo.

Su arquitectura MVT (Model–View–Template) mantiene el código organizado, separando la lógica, los datos y la interfaz visual. Esto facilita el mantenimiento del proyecto y el trabajo en equipo.

---

## Comandos utilizados en el desarrollo del proyecto

1. **cd nombre_carpeta** — Cambia de directorio.  
2. **md nombre_carpeta** — Crea una carpeta nueva.  
3. **python -m venv venv** — Crea el entorno virtual.  
4. **venv\Scripts\activate** — Activa el entorno virtual.  
5. **pip install django** — Instala Django.  
6. **django-admin startproject nombre_proyecto** — Crea el proyecto.  
7. **cd marketplace_main** — Entra al proyecto.  
8. **python manage.py runserver** — Inicia el servidor local.  
9. **python manage.py startapp store** — Crea la aplicación "store".  
10. **python manage.py migrate** — Aplica migraciones iniciales.  
11. **python manage.py createsuperuser** — Crea el usuario administrador.  
12. **python manage.py makemigrations** — Registra cambios en modelos.

---

## Arquitectura MVT en Django

- **Model:** Maneja los datos y la base de datos.  
- **View:** Contiene la lógica del proyecto.  
- **Template:** Muestra el contenido al usuario mediante HTML.

---

## Archivos principales del proyecto

---

## settings.py  
### Concepto  
Archivo central de configuración del proyecto Django. Controla apps instaladas, base de datos, archivos estáticos, plantillas y más.

### En resumen  
Determina cómo funciona y se comporta el proyecto.

---

## urls.py  
### Concepto  
Define las rutas disponibles en el sitio y qué vista se ejecuta cuando el usuario accede a una URL.

### En resumen  
Es el mapa del sitio web que conecta URLs con vistas.

### Código  
```python
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, contact, detail, register, logout_user, add_item
from .forms import LoginForm

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='store/login.html',
        authentication_form=LoginForm
    ), name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_item/', add_item, name='add_item'),
    path('detail/<int:pk>/', detail, name='detail'),
]
```

## Explicación de rutas
- **Home**: Página principal donde se muestran productos.

- **Contact**: Página con información de contacto.

- **Login**: Formulario para iniciar sesión.

- **Detail**: Muestra la información completa de un producto seleccionado.

- **Register**: Registro de nuevos usuarios.

- **Logout**: Cierra sesión.

- **Add_item**: Permite agregar nuevos artículos (solo usuarios autenticados).

## views.py
### Concepto 
Aquí se definen las funciones que procesan solicitudes, obtienen datos y devuelven respuestas HTML.

### En resumen
Controla la lógica entre los datos y la interfaz HTML.

### Código
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

## Explicación de vistas añadidas
- **Login()**: Maneja el inicio de sesión.

- **Logout_user()**: Cierra sesión.

- **Detail()**: Muestra un artículo por su ID.

- **Add_item()**: Permite crear artículos, protegido con @login_required.

- **@login_required**: Restringe vistas solo para usuarios autenticados.

## models.py
### Concepto
Define las tablas de la base de datos usando clases de Python.

### En resumen
Es el puente entre la base de datos y el código del proyecto.

### Código
```python

from django.contrib.auth.models import User
from django.db import models


class category(models.Model):
    name = models.CharField(max_length=255)


    class Meta:
        ordering = ('name', )
        verbose_name_plural = "categories"


    def __str__(self):
        return self.name


class item(models.Model):
    category = models.ForeignKey(category, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="item_images", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

```

## forms.py
### Concepto
Gestiona los formularios usados para registrar usuarios, iniciar sesión y crear artículos.

### En resumen
Define campos, valida datos y personaliza formularios.

### Código
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
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }

```

## Explicación de los formularios utilizados
- **LoginForm**:Formulario para iniciar sesión con usuario y contraseña.

- **SignupForm**:Permite registrar una nueva cuenta, validando que los datos sean correctos.

- **NewItemForm**:Formulario para crear nuevos artículos con imagen, precio, descripción, etc.

## Templates (store/templates/store/)

### base.html
Plantilla principal del proyecto. Todas las demás páginas la extienden.

### contact.html
Página donde aparecerá información para contacto.

### home.html
Página principal con tarjetas de productos.

### item.html
Muestra los detalles completos de un producto.

### navigation.html
Menú superior de navegación (Home, Contact, Login, Logout, etc.).

### login.html
Formulario para iniciar sesión.

### signup.html
Formulario para registrar un nuevo usuario.

### form.html
Plantilla usada para mostrar formularios como “Agregar Artículo”.

## Ejecución del proyecto
(Decidimos no incluír imágenes ya que nuestro ducumento contiene una gran cantidad de ellas.)

## Conclusiones
Este proyecto nos permitió comprender cómo Django estructura una aplicación web mediante MVT y cómo cada archivo cumple un rol importante. Aprendimos a trabajar con rutas, vistas, formularios, modelos y plantillas, además de entender cómo se conectan entre sí para crear una aplicación web funcional. Django resultó ser un framework poderoso que facilita el desarrollo y fomenta buenas prácticas en la organización del código.

