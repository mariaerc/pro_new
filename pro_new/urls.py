"""examenes_semestrales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from principal.views import login
from principal.views import registro
from principal.views import perfil_docente
from principal.views import agregar
from principal.views import reportes

urlpatterns = [
    url('^login$',login, name='login'),
    url('^registro',registro, name='registro'),
    url('^docente',perfil_docente,name= 'perfil_docente'),
    url('^agregar',agregar, name = 'agregar'),
    url('^reportes',reportes, name = 'reportes'),
    url(r'^admin/', admin.site.urls)
]
