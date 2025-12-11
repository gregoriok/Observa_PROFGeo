"""
URL configuration for Observa_PROFGeo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_unidade_associada.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('unidades/', include('app_unidade_associada.urls'), name='unidade_associada'),
    path('',home_page,name='home'),
    path('usuarios/',include('usuarios.urls'),name='usuarios'),
]
