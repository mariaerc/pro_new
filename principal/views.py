# -*- encoding: utf-8 -*-

from django.shortcuts import render , render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from .models import Usuario, Nivel, Materia, Caso, Grupo
from .models import Pregunta
from validators import Validator
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import NON_FIELD_ERRORS
from .validators import FormRegistroValidator, FormLoginValidator
from django.contrib import auth



# Create your views here.
def login(request):
    """view del login
    """
    #Verificamos que los datos lleguen por el methodo POST

    if request.method == 'POST':
        #Cargamos el formulario (ver forms.py con los datos del POST)
        validator = FormLoginValidator(request.POST)
        #formulario = LoginForm(data = request.POST)
        #Verificamos que los datos esten correctos segun su estructura

        if validator.is_valid():
            # Capturamos las variables que llegan por POST
            usuario = request.POST['usuario']
            clave = request.POST['clave']
            auth.login(request, validator.acceso) # Crear una sesion
            return HttpResponseRedirect('agregar')
        else:
            return render_to_response('login.html', {'error': validator.getMessage() } , context_instance = RequestContext(request))

    return render_to_response('login.html', context_instance = RequestContext(request))



from django.contrib.auth.hashers import make_password
def registro(request):
    error = False
    if request.method == 'POST':
        validator = Validator(request.POST)
        validator.required = ['name', 'grado', 'user','password' ]

        if validator.is_valid():
            usuario= Usuario()
            usuario.nombre = request.POST['name']
            usuario.grado = request.POST['grado']
            usuario.user = request.POST['user']
            usuario.clave = make_password(request.POST['password'])
            #TODO /para la proxima/  ennviar correo electronico para confirmar cuenta
            usuario.is_active = True
            usuario.save()
        else:
            return render_to_response('registro.html', {'error': validator.getMessage() } , context_instance = RequestContext(request))
        # Agregar el usuario a la base de datos
    return render_to_response('registro.html', context_instance = RequestContext(request))

def perfil_docente(request):
    return render_to_response('perfil_docente.html', context_instance = RequestContext(request))

def agregar(request):
    if request.method == 'POST':
        pregunta = Pregunta()
        pregunta.materia = request.POST['Materias']
        pregunta.enunciado = request.POST['enunciado']
        pregunta.nivel = request.POST['Niveles']
        pregunta.caso = request.POST['casos']
        pregunta.numero_opciones = request.POST['Nopciones']
        pregunta.save()
    nivel = Nivel.objects.all()
    materias = Materia.objects.all()
    caso = Caso.objects.all()
    return render_to_response('agregar.html',{'niveles': nivel, 'materias':materias, 'casos':caso}, context_instance = RequestContext(request))

def reportes(request):
    nivel = Nivel.objects.all()
    materias = Materia.objects.all()
    grado = Grupo.objects.all()
    return render_to_response('reportes.html',{'niveles': nivel, 'materias':materias, 'grados':grado}, context_instance = RequestContext(request))