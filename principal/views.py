# -*- encoding: utf-8 -*-
import json, random
from django.contrib.auth.hashers import make_password
from django.shortcuts import render , render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from .models import *
from django.contrib.auth.models import User
from principal.validators import Validator
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import NON_FIELD_ERRORS
from .validators import FormRegistroValidator, FormLoginValidator
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import subprocess as spp
from zipfile import BadZipfile, ZipFile
import zipfile
from django.db.models import Count
from xml.dom.minidom import parse
import xml.dom.minidom
from datetime import datetime, date, time, timedelta
import calendar
import openpyxl
#import xhtml2pdf
#import xhtml2pdf.pisa as pisa
#import StringIO
BASE4 = "/home/maria/prinstitucional/pro_new/principal/";
BASE5= "/home/maria/prinstitucional/pro_new/static/documentos/";
BASE6 = "/home/maria/prinstitucional/pro_new/static/documentotmp/"

#PATH = dirname(__file__)
@login_required(login_url="/login") # Protegemos la vista con el decorador del loguin para que solo pueda ingresar un usuario logueado
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")

# Create your views here.
def login(request):
    """view del login
    """
    #Verificamos que los datos lleguen por el methodo POST

    if request.method == 'POST':
        #Cargamos el formulario (ver forms.py con los datos del POST)
        #validator = FormLoginValidator(request.POST)
        #formulario = LoginForm(data = request.POST)
        #Verificamos que los datos esten correctos segun su estructura
        usuario = request.POST['usuario']
        clave = request.POST['clave']
        error= "Usuario o Contraseña invalidos"
        acceso = auth.authenticate(username = usuario, password = clave)

        if acceso == None:
            return render_to_response('login.html', {'error': error } , context_instance = RequestContext(request))
        else:
            auth.login(request, acceso)
            usu =  User.objects.get(username=usuario)
            perfil = Estudiante.objects.filter(id_id=usu.id)

            try:
                estudiante = Estudiante.objects.get(id_id=usu.id)
                if estudiante != "":
                    return HttpResponseRedirect('/estudiantes?id='+str(usu.id))
            except:
                docente = Docente.objects.get(id_id=usu.id)

                return HttpResponseRedirect('/ShowUsers')

    return render_to_response('login.html', context_instance = RequestContext(request))

def ejemplo_pdf(request):
    result = StringIO.StringIO() #creamos una instancia del un objeto StringIO para
    html = render_to_string("doc_pdf.html", {"user": 'Darwin'}) #obtenemos la plantilla
    pdf = pisa.pisaDocument( html , result) # convertimos en pdf la template
    return HttpResponse(result.getvalue(), content_type='application/pdf')


def registro(request):
    grupo = Grupo.objects.all().order_by('nombre')
    error = False
    if request.user.is_authenticated():
         #user = request.user.first_name
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             mess=""
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):

                 if request.method == 'POST':
                    user_duplicate = User.objects.filter(username=request.POST['documento']).exists()
                    if user_duplicate is True:
                        mess="si"
                        return render_to_response('registro.html',{'perfil':perfil,'mess':mess},context_instance = RequestContext(request))
                    else:
                        usuario = User()
                        usuario.first_name = request.POST['name'].upper()
                        usuario.last_name = request.POST['apellidos'].upper()
                        usuario.username = request.POST['documento']
                        usuario.password = make_password(request.POST['documento'])
                        usuario.is_active = True
                        usuario.save()

                        estudiante = Estudiante()
                        estudiante.id = usuario
                        estudiante.grupo_id = request.POST['Grados']
                        estudiante.save()


    return render_to_response('registro.html',{'grados':grupo,'perfil':perfil,'mess':mess}, context_instance = RequestContext(request))

def RegistroUser(request):
    if request.user.is_authenticated():
         #user = request.user.first_name
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             mess=""
             if docente.perfil == "Docente":
                 return HttpResponseRedirect('/viw_grados_estudiantes')
             if docente.perfil == "Administrador":

                if request.method == 'POST':
                    user_duplicate = User.objects.filter(username=request.POST['user']).exists()
                    if user_duplicate is True:
                        mess="si"
                        return render_to_response('registro_docente.html',{'perfil':perfil,'mess':mess},context_instance = RequestContext(request))
                    else:
                        usuario = User()
                        usuario.first_name = request.POST['name'].upper()
                        usuario.username = request.POST['user']
                        usuario.password = make_password(request.POST['password'])
                        usuario.is_active = True
                        usuario.save()

                        docente = Docente()
                        docente.id = usuario
                        docente.perfil = request.POST['perfil']
                        docente.save()
                return render_to_response('registro_docente.html',{'perfil':perfil,'mess':mess},context_instance = RequestContext(request))
def ShowUsers(request):
    if request.user.is_authenticated():
         #user = request.user.first_name
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if docente.perfil == "Docente":
                 return HttpResponseRedirect('/viw_grados_estudiantes')
             if docente.perfil == "Administrador":
                 users = Docente.objects.values("id_id","id_id__first_name","id_id__username","id_id__last_login","perfil").all().order_by("id_id__first_name")

                 return render_to_response('ShowUsers.html',{'perfil':perfil,'users':users}, context_instance = RequestContext(request))

@login_required(login_url="/login")
def CargarEstudiantes(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        docente = Docente.objects.get(id_id=user_id)
        perfil = docente.perfil
    try:
        DOMTree = xml.dom.minidom.parse(BASE5+"alumnos.xml")
        collection = DOMTree.documentElement

        alumnos = collection.getElementsByTagName("alumno")
        cursos = collection.getElementsByTagName("curso")
        for c in cursos:
            nombre = c.getAttribute("nombre")
            jornada = c.getAttribute("jornada").upper()
            curso = Grupo.objects.get(nombre=nombre,jornada=jornada)
            codigo = c.getAttribute("codigo")
        id_curso = curso.id

        for alumno in alumnos:

            nombre = alumno.getElementsByTagName('nombre')[0]
            apellidos = alumno.getElementsByTagName('apellidos')[0]
            documento = alumno.getElementsByTagName('documento')[0]

            usuario = User()
            usuario.first_name = nombre.childNodes[0].data.upper()
            ap=apellidos.childNodes[0].data
            usuario.last_name = apellidos.childNodes[0].data.upper()
            usuario.username = documento.childNodes[0].data
            usuario.password = make_password(documento.childNodes[0].data)
            usuario.is_active = True
            usuario.save()

            estudiante = Estudiante()
            estudiante.id = usuario
            estudiante.grupo_id = id_curso
            estudiante.save()
            print("EXITOOOOO")
        return HttpResponseRedirect('/viw_grados_estudiantes')
    except:
        mess="si"
        return render_to_response('CargarEstudiantes.html',{'perfil':perfil,'mess':mess}, context_instance = RequestContext(request))

@login_required(login_url="/login")
def LeerAlumnos(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        docente = Docente.objects.get(id_id=user_id)
        perfil = docente.perfil
        if request.method == 'POST':

            curso = request.POST['Grado']
            doc = openpyxl.load_workbook(BASE5+"alumnos.xlsx")
            hoja = doc.get_sheet_by_name('Sheet1')
            #hoja = doc.get_sheet_by_index(0)
            for fila in hoja.rows:
                nombres = fila[0].value
                apellidos = fila[1].value
                documento = fila[2].value

                user_duplicate = User.objects.filter(username=documento).exists()
                if user_duplicate is False:
                    usuario = User()
                    usuario.first_name = nombres.upper()
                    usuario.last_name = apellidos.upper()
                    usuario.username = documento
                    usuario.password = make_password(documento)
                    usuario.is_active = True
                    usuario.save()

                    estudiante = Estudiante()
                    estudiante.id = usuario
                    estudiante.grupo_id = curso
                    estudiante.save()

        return HttpResponseRedirect('/viw_grados_estudiantes')

@login_required(login_url="/login")
def ViwCargar(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             mess=""
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                 grados = Grupo.objects.all()
                 return render_to_response('CargarEstudiantes.html',{'perfil':perfil,'mess':mess,'grados':grados}, context_instance = RequestContext(request))



def test(request):

    if request.method == 'POST':

        estudiante = request.POST['estudiante']
        examen = request.POST['examen']
        preguntas = json.loads(request.POST['preguntas'])
        print(preguntas)
        for p in preguntas:
            t = Test()

            t.estudiante_id = estudiante
            t.examen_id = examen
            t.pregunta_id = p['pregunta']
            t.save()


            a = Respuesta()
            a.test_id = t.id
            a.opcion_id = p['opcion']
            a.save()
    res = {}
    #res['estado'] = 'Error al guardar, verifique los datos ingresados!.'
    #print(res)

    return HttpResponse(json.dumps(res), content_type="application/json")

@login_required(login_url="/login")
def activar_exam(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':
                    activo = ActivarExamen.objects.filter(examen_id=request.POST['Examen']).exists()
                    if activo is True:
                        exam_id = request.POST['Examen']
                        print(exam_id)
                        ac = ActivarExamen.objects.get(examen_id=exam_id)
                        ac.inicio = request.POST['fecha_inicio']
                        ac.fin = request.POST['fecha_fin']
                        ac.save()

                    if activo is False:
                        print("no hay nadaaa")
                        act = ActivarExamen()
                        act.examen_id = request.POST['Examen']
                        act.inicio = request.POST['fecha_inicio']
                        act.fin = request.POST['fecha_fin']
                        act.save()
                return redirect('/show_examenes')
@login_required(login_url="/login")
def desactivar_exam(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':

                    exam_id = request.POST['id_examen']
                    print(exam_id)
                    ac = ActivarExamen.objects.get(examen_id=exam_id)
                    ac.delete()
                return redirect('/show_examenes')

@login_required(login_url="/login")
def get_opciones(request):
    if request.method == 'POST':
        #opciones = Opcion.objects.all()

        data = {}
        #for o in opciones:
        #    data[str(o.id)] = [o.tipo, o.enunciado]

        po = []
        #return HttpResponse(json.dumps(data), content_type="application/json")
        preguntas = Pregunta.objects.filter(materia_id=request.POST['materia'], nivel_id=request.POST['nivel'])
        for p in preguntas:
            pro = PreguntaOpcion.objects.filter(pregunta_id=p.id)
            for pre in pro:
                po.append(pre.opcion_id)

        for o in po:
            lop = Opcion.objects.filter(id=o)[0]
            data[str(lop.id)] = [lop.tipo, lop.enunciado]

        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponse("No post")

@login_required(login_url="/login")
def agregar(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             mens=""
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                materias = Materia.objects.all()
                nivel = Nivel.objects.all()
                caso = Caso.objects.all()

                if request.method == 'POST':

                    res = {}

                    try:
                        pregunta = Pregunta()
                        pregunta.materia_id = request.POST['materia']
                        pregunta.enunciado = request.POST['enuPre']
                        pregunta.nivel_id = request.POST['nivel']
                        pregunta.numero_opciones = request.POST['numOp']

                        if request.POST['caso'] == '0':
                            pregunta.caso_id = None
                        else:
                            pregunta.caso_id = request.POST['caso']

                        pregunta.save()

                        ops = json.loads(request.POST['opciones'])
                        lops = []
                        for o in ops:
                            if(o['id'] != '0'):
                                lops.append(o['id'])
                            else:
                                top = Opcion()
                                top.enunciado = o['enunciado']
                                top.tipo = o['tipo']
                                top.save()
                                lops.append(top.id)

                        for o in lops:
                            po = PreguntaOpcion()
                            po.pregunta_id = pregunta.id
                            po.opcion_id = o
                            po.save()

                        res['estado'] = 'OK'
                    except:
                        res['estado'] = 'Error al guardar, verifique los datos ingresados!.'

                    return HttpResponse(json.dumps(res), content_type="application/json")
                else:
                    return render_to_response('agregar.html',{'niveles': nivel, 'materiass':materias, 'casos':caso,'perfil':perfil,'mens':mens}, context_instance = RequestContext(request))

@login_required(login_url="/login")
def EditPregunta(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':
                    datos=request.POST['area']
                    print (datos)
                    campos = datos.split(';')
                    for campo in campos:
                        info = campo.split(':')
                        if len(info)>1:
                            opcion_id = info[0]
                            opcion = Opcion.objects.get(id=opcion_id)
                            opcion.enunciado = info[1]
                            opcion.tipo = info[2]
                            opcion.save()
                    p = request.POST['id_pregunta']
                    pregunta = Pregunta.objects.get(id=p)
                    pregunta.enunciado = request.POST['enunciado']
                    pregunta.materia_id = request.POST['Materias']
                    pregunta.nivel_id = request.POST['Niveles']
                    if request.POST['name_file'] != "":
                        pregunta.imagen = request.POST['name_file']
                    if request.POST['caso_nuevo'] == "si":
                        caso = Caso()
                        caso.enunciado = request.POST['caso_enunciado_nuevo']
                        caso.nombre_caso = request.POST['nom_caso']
                        caso.save()
                        pregunta.caso_id = caso.id
                    pregunta.save()
                    if request.POST['caso_enunciado'] != "":
                        c = request.POST['id_caso']
                        caso= Caso.objects.get(id=c)
                        caso.enunciado = request.POST['caso_enunciado']
                        caso.save()

                return HttpResponseRedirect('/ViwMateriaPre')


@login_required(login_url="/login")
def infoPregunta(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':
                    niveles = Nivel.objects.all()
                    materias = Materia.objects.all()
                    casos = Caso.objects.all()
                    p = request.POST['id_pregunta']
                    pregunta = Pregunta.objects.get(id=p)
                    pre_opcion = PreguntaOpcion.objects.filter(pregunta_id=p)
                    op = []
                    for o in pre_opcion:
                        opcion = Opcion.objects.get(id = o.opcion_id)
                        op.append({'id':opcion.id, 'enunciado':opcion.enunciado,'tipo':opcion.tipo})
                    return render_to_response('EditPregunta.html',{'pregunta':pregunta,'opciones':op,'casos':casos,'materias':materias,'niveles':niveles,'perfil':perfil}, context_instance = RequestContext(request))

@login_required(login_url="/login")
def NewPregunta(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):

                niveles = Nivel.objects.all()
                materias = Materia.objects.all()
                casos = Caso.objects.all()

                return render_to_response('Newpregunta.html',{'casos':casos,'materias':materias,'niveles':niveles,'perfil':perfil}, context_instance = RequestContext(request))


@login_required(login_url="/login")
def SavePregunta(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':

                    pregunta = Pregunta()
                    pregunta.enunciado = request.POST['enunciado']
                    pregunta.materia_id = request.POST['Materias']
                    pregunta.nivel_id = request.POST['Niveles']
                    pregunta.numero_opciones = 4
                    if request.POST['name_file'] != "":
                        pregunta.imagen = request.POST['name_file']
                    if request.POST['caso_enunciado_nuevo'] != "":
                        caso = Caso()
                        caso.enunciado = request.POST['caso_enunciado_nuevo']
                        caso.nombre_caso = request.POST['nom_caso']
                        caso.save()
                        pregunta.caso_id = caso.id
                    pregunta.save()

                    datos=request.POST['area']
                    print (datos)
                    campos = datos.split(';')
                    for campo in campos:
                        info = campo.split(':')
                        if len(info)>1:
                            opcion = Opcion()
                            opcion.enunciado = info[0]
                            opcion.tipo = info[1]
                            opcion.save()
                            po = PreguntaOpcion()
                            po.pregunta_id = pregunta.id
                            po.opcion_id = opcion.id
                            po.save()


                return HttpResponseRedirect('/ViwMateriaPre')


@login_required(login_url="/login")
def reportes(request):
    mens=""
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                nivel = Nivel.objects.all()
                materias = Materia.objects.all()
                grado = Grupo.objects.all()
                años = Years.objects.all()
                estudiante = Estudiante.objects.all()

                return render_to_response('reportes.html',{'años':años,'mens':mens,'niveles': nivel, 'materias':materias, 'grados':grado,'estudiante':estudiante,'perfil':perfil}, context_instance = RequestContext(request))
def report_estudiante_materia(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':
                    periodo= request.POST['Periodo']
                    año= request.POST['Año']
                    est = Estudiante.objects.values("id_id__first_name","id_id__last_name","grupo__nombre").get(id_id=request.POST['id_estudiante'])
                    materia = Materia.objects.get(id=request.POST['id_materia'])
                    id_estudiante = request.POST['id_estudiante']
                    id_materia = request.POST['id_materia']
                    test= Test.objects.values("pregunta__enunciado","respuesta__opcion__enunciado","respuesta__opcion__tipo").filter(estudiante_id=id_estudiante, pregunta__materia_id=id_materia ).order_by("respuesta__opcion__tipo")

                    for i in test:
                        pregunta= i["pregunta__enunciado"]
                        respuesta= i["respuesta__opcion__enunciado"]
                        tipo= i["respuesta__opcion__tipo"]

                return render_to_response('ReporteEstMateria.html',{'periodo':periodo,'año':año,'perfil':perfil,'test':test,'est':est,'materia':materia}, context_instance = RequestContext(request))
def get_report(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         mens=""
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))

         except:

             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':

                    materia = Materia.objects.get(id=request.POST['Materias'])
                    grado = Grupo.objects.get(id=request.POST['Grados'])
                    periodo= request.POST['Periodo']
                    año= request.POST['Año']
                    #resultados = Estudiante.objects.raw("select * from pregunta where materia_id="+request.GET['materia']+" and nivel_id="+request.GET['nivel']+" ORDER by rand() limit "+request.GET['examen'])
                    resultados = Estudiante.objects.raw("SELECT estudiante.id_id, (SELECT COUNT(respuesta.id) FROM test,respuesta,opcion WHERE test.examen_id=examen.id and respuesta.test_id=test.id and respuesta.opcion_id=opcion.id and opcion.tipo='V' and test.estudiante_id=estudiante.id_id) as CORRE, (SELECT COUNT(respuesta.id) FROM test,respuesta,opcion WHERE test.examen_id=examen.id and respuesta.test_id=test.id and respuesta.opcion_id=opcion.id and opcion.tipo='F' and test.estudiante_id=estudiante.id_id) as INCO, (SELECT examen_contestado.calificacion FROM examen_contestado WHERE examen_contestado.estudiante_id=estudiante.id_id and examen_contestado.examen_id=examen.id and examen_contestado.grupo_id=examen_grupo.grupo_id ORDER BY examen_contestado.id DESC LIMIT 1) as CALI  from examen_grupo, examen, test, estudiante WHERE examen_grupo.grupo_id="+request.POST['Grados']+" and examen.materia_id="+request.POST['Materias']+" and examen_grupo.examen_id=examen.id and examen_grupo.periodo='"+request.POST['Periodo']+"' and examen_grupo.año="+request.POST['Año']+" and test.examen_id=examen.id and test.estudiante_id=estudiante.id_id GROUP by estudiante.id_id")

                    data = []

                    for r in resultados:

                        user = User.objects.get(id=r.id_id)
                        tmp = {}
                        tmp['id'] = r.id_id
                        tmp['estudiante'] = user.last_name+" "+user.first_name
                        tmp['corre'] = r.CORRE
                        tmp['inco'] = r.INCO
                        tmp['cali'] = r.CALI

                        data.append(tmp)

                    guide = []
                    for d in data:
                        guide.append(d['estudiante'])

                    guide.sort()

                    res = []
                    for g in guide:
                        for d in data:
                            if(g == d['estudiante']):
                                res.append(d)
                    resbien=0
                    resmal=0
                    for r in res:
                        resbien=resbien+r['corre']
                        resmal=resmal+r['inco']
                    print(resbien)
                    print(resmal)
                    return render_to_response('ReporteMateriaG.html',{'periodo':periodo,'año':año,'resmal':resmal,'resbien':resbien,'perfil':perfil,'materia':materia,'grado':grado,'data':res}, context_instance = RequestContext(request))
                else:
                    return HttpResponse("OOOO")


def grgrado(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         mens=""
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':
                    grado = Grupo.objects.get(id=request.POST['Grados'])
                    id_grado = request.POST['Grados']
                    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                    exameng = ExamenGrupo.objects.values("examen__id","examen__materia__id").filter(grupo_id=id_grado)
                    #print(exameng)
                    test1= Test.objects.values("examen__id","estudiante__id","estudiante__id__first_name","estudiante__id__last_name","respuesta__opcion__tipo","examen__materia__id").filter(estudiante__grupo_id=id_grado).annotate(contador=Count('respuesta__opcion__tipo')).order_by("estudiante__id","respuesta__opcion__tipo")

                    id_actual=""
                    cont = 0
                    resultados=[]
                    ids=[]
                    mate=[]
                    tot=[]
                    resbien=0
                    resmal=0
                    for i in test1:
                        id_actual = i["examen__materia__id"]


                        if id_actual == i["examen__materia__id"]:
                            if i["respuesta__opcion__tipo"] == "V":
                                resbien = resbien+1
                                resultados.append([i["examen__materia__id"],i["contador"],0])
                            else:
                                resultados.append([i["examen__materia__id"],0,i["contador"]])
                            cont += 1

                        #else:
                            #resultados[cont-1][1]=i["contador"]
                        if i["examen__materia__id"] not in mate:
                            mate.append(i["examen__materia__id"])

                    print(mate)
                    for m in mate:
                        for r in resultados:
                            if m == r[0]:
                                resmal = resmal+r[2]
                                resbien = resbien+r[1]
                        tot.append({"materia":m,"bien":resbien,"mal":resmal})
                        resbien=0
                        resmal=0


                    print(tot)
                    print(resmal)

                    if not resultados  :
                        mens = "si"
                        nivel = Nivel.objects.all()
                        materias = Materia.objects.all()
                        grado = Grupo.objects.all()
                        estudiante = Estudiante.objects.all()

                        return render_to_response('reportes.html',{'mens':mens,'niveles': nivel, 'materias':materias, 'grados':grado,'estudiante':estudiante,'perfil':perfil}, context_instance = RequestContext(request))
                    else:

                        return render_to_response('ReporteGrado.html',{ 'resbien':resbien,'resmal':resmal,'resultados':resultados, 'grado':grado}, context_instance = RequestContext(request))




@login_required(login_url="/login")
def index_estudiante(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        aux="no"
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":

                estu = Estudiante.objects.get(id_id=request.GET['id'])
                curso = Grupo.objects.get(id=estu.grupo_id)

                eg = ExamenGrupo.objects.filter(grupo_id=estu.grupo.id)
                s = []
                ac = ActivarExamen.objects.all()


                hoy = date.today()  # Obtiene fecha

                for w in eg:

                    t = {}
                    t['materia'] = w.examen.materia.nombre
                    t['materia_id'] = w.examen.materia.id
                    t['nivel'] = w.grupo.nivel.id
                    t['examen'] = w.examen.numero_preguntas
                    act = ActivarExamen.objects.filter(examen_id=w.examen.id).exists()
                    exc = ExamenContestado.objects.filter(estudiante_id=request.GET['id'],examen_id=w.examen.id).exists()
                    if exc is True:
                        pass
                    else:
                        if act is True:
                            a=ActivarExamen.objects.get(examen_id=w.examen.id)
                            if hoy >= a.inicio and hoy <= a.fin:
                                t['examen_id'] = w.examen.id
                                s.append(t)
                        if act is False:
                            pass

                if s == []:
                    mensaje="No tienes examenes disponibles"
                    return render_to_response('template_estudiante.html',{ 'eid':estu.id_id, 'curso':curso,'mensaje':mensaje}, context_instance = RequestContext(request))
                else:
                    print(s)
                    return render_to_response('index_estudiante.html',{'aux':aux,'examenes':s, 'eid':estu.id_id, 'curso':curso,'ac':ac}, context_instance = RequestContext(request))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                return HttpResponseRedirect('/viw_grados_estudiantes')

@login_required(login_url="/login")
def agre_examen(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                niveles = Nivel.objects.all()
                grupos = Grupo.objects.all()
                examenes = Examen.objects.all()
                materias = Materia.objects.all()
                if request.method == 'POST':
                    exam = Examen()
                    exam.nombre = request.POST['Nom_Examen']
                    exam.numero_preguntas = request.POST['numPre']
                    exam.materia_id = request.POST['Materias']
                    exam.save()

                return redirect('/show_examenes')
@login_required(login_url="/login")
def show_examenes(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                niveles = Nivel.objects.all()
                grupos = Grupo.objects.all()
                materias = Materia.objects.all()
                examenes = Examen.objects.all()
                eAsignado = []
                exam = []
                exam_sa = []

                for e in examenes:
                    exa_grupo = ExamenGrupo.objects.filter(examen_id=e.id)
                    exa_activo = ActivarExamen.objects.filter(examen_id=e.id).exists()
                    eAsignado.append({'nombre':e.nombre,'id':e.id})
                    for eg in exa_grupo:

                        if exa_activo is True:
                            eac = ActivarExamen.objects.get(examen_id=e.id)
                            exam.append({'id_a':e.id,'nombre':e.nombre,'npreguntas':e.numero_preguntas,'materia':e.materia_id,'grupo':eg.grupo_id,'finicio':eac.inicio,'ffin':eac.fin})
                            print(exam)
                        if exa_activo is False:
                            exam.append({'id_a':e.id,'nombre':e.nombre,'npreguntas':e.numero_preguntas,'materia':e.materia_id,'grupo':eg.grupo_id,'finicio':"",'ffin':""})

                return render_to_response('examen_nuevo.html',{'perfil':perfil,'eAsignado':eAsignado,'exam_sa':exam_sa,'materias':materias,'niveles':niveles,'examenes':examenes,'grupos':grupos,'list_examen':exam}, context_instance = RequestContext(request))
@login_required(login_url="/login")
def ShowEditExamen(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':
                    ex=[]
                    niveles = Nivel.objects.all()
                    grupos = Grupo.objects.all()
                    materias = Materia.objects.all()
                    grupo_id = request.POST['id_exa_grup']
                    examen_id = request.POST['id_examen_edit']
                    examen = Examen.objects.get(id=examen_id)
                    exa_grupo = ExamenGrupo.objects.get(examen_id=examen_id, grupo_id=grupo_id)
                    exa_activo = ActivarExamen.objects.filter(examen_id=examen_id).exists()
                    print(exa_grupo.año)
                    años= Years.objects.all()
                    if exa_activo is True:
                        eac = ActivarExamen.objects.get(examen_id=examen_id)
                        ex.append({'id':examen.id,'nombre':examen.nombre,'npreguntas':examen.numero_preguntas,'materia':examen.materia_id,'id_eg':exa_grupo.id,'grupo':exa_grupo.grupo_id,'periodo':exa_grupo.periodo,'year':exa_grupo.año,'id_ac':eac.id,'finicio':eac.inicio,'ffin':eac.fin})

                    if exa_activo is False:
                        ex.append({'id':examen.id,'nombre':examen.nombre,'npreguntas':examen.numero_preguntas,'materia':examen.materia_id,'id_eg':exa_grupo.id,'grupo':exa_grupo.grupo_id,'periodo':exa_grupo.periodo,'year':exa_grupo.año,'finicio':"",'ffin':""})

                return render_to_response('EditExamen.html',{'años':años,'perfil':perfil,'materias':materias,'niveles':niveles,'grupos':grupos,'list_examen':ex}, context_instance = RequestContext(request))


def EditExamen(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':
                    mat = Materia.objects.get(id=request.POST['Materias'])
                    grado = Grupo.objects.get(id=request.POST['Grados'])
                    per= request.POST['Periodo']
                    nom_Examen = mat.nombre[0:3]+"-"+per+"-"+grado.nombre+"J"+grado.jornada[0:1]

                    examen_id = request.POST['id_ex']
                    examen = Examen.objects.get(id=examen_id)
                    examen.nombre = nom_Examen
                    examen.numero_preguntas = request.POST['npreguntas']
                    examen.materia_id = request.POST['Materias']
                    examen.save()

                    examen_grupo = ExamenGrupo.objects.get(id=request.POST['id_eg'])
                    examen_grupo.grupo_id = request.POST['Grados']
                    examen_grupo.periodo = request.POST['Periodo']
                    examen_grupo.año = request.POST['Año']
                    examen_grupo.save()


                return HttpResponseRedirect('/show_examenes')

@login_required(login_url="/login")
def agre_grupo(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                if request.method == 'POST':
                    grupo=Grupo()
                    grupo.nombre=request.POST['Nom_Grupo']
                    grupo.nivel_id =request.POST['Niveles']
                    grupo.jornada =request.POST['Jornadas'].upper()
                    grupo.save()

                return redirect('/grupos_viw')


@login_required(login_url="/login")
def grupos_viw(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                print("holaaaaaaaaaaaa")
                niveles = Nivel.objects.all().order_by('nombre')
                grados = Grupo.objects.all().order_by('jornada','nivel_id__nombre','nombre')
                #grados = Grupo.objects.all().order_by('nivel_id__nombre','jornada')
                print(grados)
                return render_to_response('crear_grados.html',{'perfil':perfil,'niveles':niveles,'grupos':grados}, context_instance = RequestContext(request))

@login_required(login_url="/login")
def viw_estudiantes(request):
    if request.user.is_authenticated():
         user_id = request.user.id
         try:
             estudiante = Estudiante.objects.get(id_id=user_id)
             if estudiante != "":
                 return HttpResponseRedirect('/estudiantes?id='+str(user_id))
         except:
             docente = Docente.objects.get(id_id=user_id)
             perfil = docente.perfil
             if (docente.perfil == "Docente" or  docente.perfil == "Administrador"):

                if request.method == 'POST':
                    id_grado = request.POST['id_grado']
                    grado = Grupo.objects.get(id =id_grado)
                    grados = Grupo.objects.all()
                    Users = User.objects.all()
                    estudiantes = Estudiante.objects.filter(grupo_id = grado)
                    list_estudents = []

                    for u in Users:
                        for e in estudiantes:
                            if u.id == e.id_id :

                                list_estudents.append({'nombre':u.first_name,'apellidos':u.last_name,'user':u.username,'grado':e.grupo_id,'id_est':u.id})
    return render_to_response('ver_estudiantes.html',{'perfil':perfil,'grado':grado,'grados':grados,'estudiantes':list_estudents}, context_instance = RequestContext(request))

@login_required(login_url="/login")
def update_estudiante(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':
                    user_id = request.POST['id_est']
                    user = User.objects.get(id = user_id)
                    user.first_name = request.POST['name'].upper()
                    user.last_name = request.POST['apellido'].upper()
                    user.username = request.POST['user']
                    if request.POST['password'] != "":
                        user.password = make_password(request.POST['password'])
                    user.save()

                    estudiante = Estudiante.objects.get(id=user_id)
                    estudiante.grupo_id = request.POST['Grados']
                    estudiante.save()
                return HttpResponseRedirect('/viw_grados_estudiantes')

@login_required(login_url="/login")
def viw_grados_estudiantes(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                niveles = Nivel.objects.all()
                grupos = Grupo.objects.all().order_by('jornada','nombre')

                return render_to_response('ver_grados_estudiantes.html',{'perfil':perfil,'niveles':niveles,'grupos':grupos}, context_instance = RequestContext(request))

@login_required(login_url="/login")
def ViwMateriaPre(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                materia = Materia.objects.all().order_by('nombre')

                return render_to_response('ver_materiasPre.html',{'perfil':perfil,'materia':materia}, context_instance = RequestContext(request))

@login_required(login_url="/login")
def ViwPreguntas(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':

                    id_materia = request.POST['id_materia']
                    materia = Materia.objects.get(id= id_materia)
                    niveles = Nivel.objects.all().order_by('nombre')
                    preguntas = Pregunta.objects.filter(materia_id=materia).order_by('nivel_id')

    return render_to_response('ver_preguntas.html',{'perfil':perfil,'preguntas':preguntas,'niveles':niveles,'materia':materia}, context_instance = RequestContext(request))


@login_required(login_url="/login")
def grupo_examen(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                if request.method == 'POST':
                    mat = Materia.objects.get(id=request.POST['Materias'])
                    grado = Grupo.objects.get(id=request.POST['Grupos'])
                    per=request.POST['Periodo']
                    nom_Examen = mat.nombre[0:3]+"-"+per+"-"+grado.nombre+"J"+grado.jornada[0:1]

                    exam = Examen()
                    exam.nombre = nom_Examen
                    exam.numero_preguntas = request.POST['numPre']
                    exam.materia_id = request.POST['Materias']
                    exam.save()

                    exa_grup = ExamenGrupo()
                    exa_grup.examen_id=exam.id
                    exa_grup.grupo_id =request.POST['Grupos']
                    exa_grup.periodo =request.POST['Periodo']
                    exa_grup.año =request.POST['Año']
                    exa_grup.save()
                return redirect('/show_examenes')


@login_required(login_url="/login")
def materia_new(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                materias = Materia.objects.all().order_by('nombre')
                if request.method == 'POST':
                    new_mat=Materia()
                    new_mat.nombre=request.POST['Nom_mate'].upper()
                    new_mat.save()
                return render_to_response('Agre_materia.html',{'perfil':perfil,'materias':materias}, context_instance = RequestContext(request))


@login_required(login_url="/login")
def nivel_new(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                niveles = Nivel.objects.all().order_by('nombre')
                if request.method == 'POST':
                    new_nivel=Nivel()
                    new_nivel.nombre=request.POST['Nom_niv'].upper()
                    new_nivel.save()
                return render_to_response('Agre_nivel.html',{'perfil':perfil,'niveles':niveles}, context_instance = RequestContext(request))

@login_required(login_url="/login")
def estudiante_examen(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        aux="si"
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                pre = Pregunta.objects.raw("select * from pregunta where materia_id="+request.GET['materia']+" and nivel_id="+request.GET['nivel']+" ORDER by rand() limit "+request.GET['examen'])
                ex= Examen.objects.get(id=request.GET['xid'])
                #print(ex.materia_id)

                curso = Grupo.objects.get(id=estudiante.grupo_id)


                mate= Materia.objects.get(id=ex.materia_id)
                #print(mate.nombre)
                pids = []
                pes = []
                for p in pre:
                    ov = PreguntaOpcion.objects.get(pregunta_id=p.id, opcion__tipo='V')
                    of = PreguntaOpcion.objects.raw("select * from pregunta_opcion, opcion where pregunta_opcion.pregunta_id="+str(p.id)+" and opcion.tipo = 'F' and pregunta_opcion.opcion_id = opcion.id ORDER BY rand() limit "+str(p.numero_opciones-1))
                    ops = [{'id':ov.opcion.id, 'enu': ov.opcion.enunciado}]

                    tag = 'ABCDEFGHIJ'

                    for f in of:
                        ops.append({'id':f.opcion.id, 'enu': f.opcion.enunciado, 'tag': '*'})

                    random.shuffle(ops)

                    for i in range(len(ops)):
                        ops[i]['tag'] = tag[i]

                    tcaso = ''
                    if(p.caso != None):
                        tcaso = p.caso.enunciado
                    q=""
                    enu = p.enunciado
                    if p.imagen != None :
                        q=p.imagen
                    pids.append(p.id)

                    pes.append( {'id':p.id, 'pregunta':enu, 'caso':tcaso, 'opciones':ops,'imagen':q} )

                pids = list(str(pid) for pid in pids)
                pids = ",".join(pids)

                return render_to_response('estudiante_examen.html',{'aux':aux,'numpre':ex.numero_preguntas,'curso':curso,'pid':pids,'mater':mate.nombre,'exa':request.GET['xid'],'range':range(1,30), 'eid':request.GET['id'], 'preguntas':pes}, context_instance = RequestContext(request))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                return HttpResponseRedirect('/viw_grados_estudiantes')
def ExamenTerminado(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        aux="no"
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                if request.method == 'POST':
                    estudiante_id = request.POST['id_estu']
                    examen_id = request.POST['id_exa']
                    examen=Examen.objects.values("numero_preguntas","materia__nombre").get(id=request.POST['id_exa'])
                    print(examen["numero_preguntas"])
                    print("sssssssssssssssssssssss")
                    estudiante = Estudiante.objects.get(id=estudiante_id)
                    grado_id = Grupo.objects.get(id = estudiante.grupo_id)
                    curso = Grupo.objects.get(id = estudiante.grupo_id)


                    test1= Test.objects.values("respuesta__opcion__tipo").filter(estudiante_id=request.POST['id_estu'], examen_id=request.POST['id_exa'] ).annotate(contador=Count('respuesta__opcion__tipo')).order_by("estudiante__id","respuesta__opcion__tipo")

                    id_actual=""
                    cont = 0
                    resultados=[]
                    for i in test1:
                        if i["respuesta__opcion__tipo"] == "V":
                            resultados.append([i["contador"],0])
                        else:
                            resultados.append([0,i["contador"]])
                        cont += 1


                    resbien=0
                    resmal=0
                    for r in resultados:
                        resbien = resbien+r[0]
                        resmal = resmal+r[1]
                    n1= examen["numero_preguntas"]
                    print(n1)
                    calculo = 5/n1
                    print("cal", calculo)
                    nota = resbien*calculo
                    if nota == 0:
                        nota = 1
                    terminado = ExamenContestado()
                    terminado.estudiante_id=request.POST['id_estu']
                    terminado.examen_id=request.POST['id_exa']
                    terminado.grupo_id = grado_id.id
                    terminado.fpresentado= request.POST['fpresentado']
                    terminado.calificacion= nota
                    #terminado.fpresentado= ("2017-09-28")
                    terminado.save()

                    return render_to_response('ResultadosEstudiante.html',{'numpre':n1,'aux':aux,'curso':curso,'eid':estudiante.id_id,'examen':examen,'resmal':resmal,'resbien':resbien,'nota':nota}, context_instance = RequestContext(request))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if (docente.perfil == "Docente" or docente.perfil == "Administrador"):
                return HttpResponseRedirect('/viw_grados_estudiantes')


def index(request):
    return render_to_response('index.html', context_instance = RequestContext(request))

@login_required(login_url="/login")
def edit_nivel(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                nivel_id = request.POST['id_nivel']
                nivel = Nivel.objects.get( id = nivel_id)
                nivel.nombre = request.POST['Nom_nivel']
                nivel.save()
                return HttpResponseRedirect('/nivel_new')

@login_required(login_url="/login")
def delete_nivel(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                nivel_id = request.POST['id_nivel_del']
                nivel = Nivel.objects.get( id = nivel_id)
                grupo = Grupo.objects.filter(nivel_id= nivel).exists()

                if grupo is False:
                    nivel.delete()
                    return HttpResponseRedirect('/nivel_new')
                if grupo is True:
                    mensaje = "El nivel no puede ser eliminado, hay elementos que dependen de el"
                    return render_to_response('template_docentes.html',{'perfil':perfil,'mensaje':mensaje}, context_instance = RequestContext(request))



@login_required(login_url="/login")
def edit_grado(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                if request.method == 'POST':
                    grado_id = request.POST['id_grado']
                    grado = Grupo.objects.get( id = grado_id)
                    grado.nombre = request.POST['Nom_grado']
                    grado.nivel_id =request.POST['Nivel']
                    grado.jornada =request.POST['Jornada'].upper()
                    grado.save()
                return HttpResponseRedirect('/grupos_viw')

@login_required(login_url="/login")
def delete_grado(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                if request.method == 'POST':
                    grado_id = request.POST['id_grado_del']
                    grado = Grupo.objects.get( id = grado_id)
                    estudent = Estudiante.objects.filter(grupo_id=grado).exists()

                    if estudent is False:
                        examen = ExamenGrupo.objects.filter(grupo_id=grado).exists()
                        if examen is False:
                            grado.delete()
                            return HttpResponseRedirect('/grupos_viw')
                        if examen is True:
                            mensaje = "El Grado no puede ser eliminado, hay elementos que dependen de el"
                            return render_to_response('template_docentes.html',{'perfil':perfil,'mensaje':mensaje}, context_instance = RequestContext(request))
                    if estudent is True:
                        mensaje = "El Grado no puede ser eliminado, hay elementos que dependen de el"
                        return render_to_response('template_docentes.html',{'perfil':perfil,'mensaje':mensaje}, context_instance = RequestContext(request))
@login_required(login_url="/login")
def delete_pregunta(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if docente.perfil == "Docente" or docente.perfil == "Administrador":
                if request.method == 'POST':
                    pregunta_id = request.POST['id_pregunta_del']
                    pregunta = Pregunta.objects.get( id = pregunta_id)
                    pre_opcion = PreguntaOpcion.objects.filter(pregunta_id=pregunta_id)
                    test = Test.objects.filter(pregunta_id=pregunta_id).exists()
                    if test is True:
                        for t in test:
                            resp = Respuesta.objects.filter(test_id=t.id)
                            resp.delete()
                        test.delete()
                    for po in pre_opcion:
                        po.delete()
                        print("exiii")
                    pregunta.delete()
                return HttpResponseRedirect('/ViwMateriaPre')

@login_required(login_url="/login")
def delete_user(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                if request.method == 'POST':

                    docente = Docente.objects.get(id = request.POST['id_user_del'])
                    docente.delete()
                    user = User.objects.get( id = request.POST['id_user_del'])
                    user.delete()
                return HttpResponseRedirect('/ShowUsers')

@login_required(login_url="/login")
def delete_estudiante(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                if request.method == 'POST':
                    est_id = request.POST['id_estudiante_del']
                    test = Test.objects.filter(estudiante_id=est_id)
                    for t in test:
                        resp = Respuesta.objects.filter(test_id=t.id)
                        print(t.id)
                        resp.delete()
                    test.delete()
                    #act = ActualEstado.objects.filter(estudiante_id = est_id)
                    #act.delete()
                    estudiante = Estudiante.objects.get(id = est_id)
                    estudiante.delete()
                    user = User.objects.get( id = est_id)
                    user.delete()
                return HttpResponseRedirect('/viw_grados_estudiantes')

@login_required(login_url="/login")
def edit_materia(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                if request.method == 'POST':
                    materia_id = request.POST['id_materia']
                    materia = Materia.objects.get( id = materia_id)
                    materia.nombre = request.POST['Nom_materia'].upper()
                    materia.save()
                return HttpResponseRedirect('/materia_new')
@login_required(login_url="/login")
def update_user(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                if request.method == 'POST':
                    user = User.objects.get(id = request.POST['id_user'])
                    user.first_name = request.POST['name'].upper()
                    user.username = request.POST['user']
                    if request.POST['password'] != "":
                        user.password = make_password(request.POST['password'])
                    user.save()

                    docente = Docente.objects.get(id=request.POST['id_user'])
                    docente.perfil = request.POST['perfil']
                    docente.save()
                return HttpResponseRedirect('/ShowUsers')

@login_required(login_url="/login")
def delete_materia(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            estudiante = Estudiante.objects.get(id_id=user_id)
            if estudiante != "":
                return HttpResponseRedirect('/estudiantes?id='+str(user_id))
        except:
            docente = Docente.objects.get(id_id=user_id)
            perfil = docente.perfil
            if docente.perfil == "Docente":
                return HttpResponseRedirect('/viw_grados_estudiantes')
            if docente.perfil == "Administrador":
                if request.method == 'POST':
                    materia_id = request.POST['id_materia_del']
                    materia = Materia.objects.get( id = materia_id)
                    pregunta = Pregunta.objects.filter(materia_id= materia).exists()
                    examen = Examen.objects.filter(materia_id= materia).exists()
                    print("preguntaaaa")
                    print(pregunta)
                    print("exameeeee")
                    print(examen)

                    if pregunta is False and examen is False:
                        materia.delete()
                        return HttpResponseRedirect('/materia_new')
                    if pregunta is True or examen is True:
                        mensaje = "La Materia no puede ser eliminada, hay elementos que dependen de ella"
                        return render_to_response('template_docentes.html',{'perfil':perfil,'mensaje':mensaje}, context_instance = RequestContext(request))


@login_required(login_url="/login")
@csrf_exempt
def archivo(request):
    if(request.method == "POST"):
        action=request.POST["action"]
        print(action)
        if(action=="save"):
            upName=request.POST["upName"]
            upData=request.POST["upData"]
            count = upData.count(",")
            if(count>0):
                posicion = upData.find(",")
                upData = upData[posicion+1:]
            f = open(BASE5+"v_"+upName, "a")
            f.write(upData)
            f.close()
            return HttpResponse(upName, content_type="application/text")
        else:

            upName=request.POST["upName"]
            spp.Popen(["python3", BASE4+"liser.py", upName,BASE5])
            return HttpResponse(upName, content_type="application/text")
    return HttpResponse("Error")

@login_required(login_url="/login")
def descomprimir(request, pwd=None):
    if(request.method == "POST"):
        nivel = request.POST["Niveles"]
        materia = request.POST["Materias"]
        name = request.POST["name_file"]
        n= name.split('.')[0]
        fil=(BASE5+name)
        print("ssssssssssssssssssssssssssssssssssssssssssss")
        print(fil)
        #fil=("/home/maria/parces/pro_new/static/documentos/pregu.zip")
        with ZipFile(fil) as f:
            f.extractall(BASE5+"/"+n, pwd=pwd)
        lectura(n,nivel,materia)

    return HttpResponseRedirect('/ViwMateriaPre')


def lectura(n,nivel,materia):

    casocod = {}

    DOMTree = xml.dom.minidom.parse(BASE5+"/"+n+"/preguntas.xml")
    collection = DOMTree.documentElement

    preg = collection.getElementsByTagName("pregunta")
    casos = collection.getElementsByTagName("caso")
    for caso in casos:
        enunciado = caso.childNodes[0].data
        nombre = caso.getAttribute("nombre")
        codigo = caso.getAttribute("codigo")
        c = Caso()
        c.enunciado = enunciado
        c.nombre_caso = nombre
        c.save()
        casocod[codigo] = c.id

    for pregunt in preg:

        enunciado = pregunt.getElementsByTagName('enunciado')[0]
        cas = pregunt.getAttribute("caso")
        opciones = pregunt.getAttribute("opciones")
        op = pregunt.getElementsByTagName('opcion')

        print(op)
        p = Pregunta()
        p.materia_id = materia
        p.enunciado = enunciado.childNodes[0].data
        print("imgaaaaaa")
        try:
            imagen = pregunt.getElementsByTagName('imagen')[0]
            pim=n+"/img/"+imagen.childNodes[0].data
            p.imagen = pim
            print(pim)
        except:
            pass
        p.nivel_id = nivel
        p.numero_opciones = opciones

        if(cas in casocod.keys()):
            p.caso_id = casocod[cas]

        p.save()
        lops = []
        for opt in op:

            tipo = opt.getAttribute("tipo")
            top = Opcion()
            top.enunciado = opt.childNodes[0].data
            top.tipo = tipo.upper()
            top.save()
            lops.append(top.id)

        for o in lops:
            po = PreguntaOpcion()
            po.pregunta_id = p.id
            po.opcion_id = o
            po.save()
            print("echooo")
