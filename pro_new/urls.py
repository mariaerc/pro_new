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
from principal.views import *
urlpatterns = [
    url('^login$',login, name='login'),
    url('^registro',registro, name='registro'),
    url('^agregar',agregar, name = 'agregar'),
    url('^NewPregunta',NewPregunta, name = 'NewPregunta'),
    url('^SavePregunta',SavePregunta, name = 'SavePregunta'),
    url('^reportes',reportes, name = 'reportes'),
    url('^get_report',get_report, name = 'get_report'),
    url('^LeerAlumnos',LeerAlumnos, name = 'LeerAlumnos'),
    url('^grgrado',grgrado, name = 'grgrado'),
    url('^estudiantes',index_estudiante, name='index_estudiante'),
    url('^examen',estudiante_examen, name='estudiante_examen'),
    url('^descomprimir',descomprimir, name='descomprimir'),
    url('^ExamenTerminado',ExamenTerminado, name='ExamenTerminado'),
    url('^report_estudiante_materia',report_estudiante_materia, name='report_estudiante_materia'),
    url('^logout$',logout, name='logout'),
    url('^getopciones',get_opciones, name='get_opciones'),
    url('^RegistroUser',RegistroUser, name='RegistroUser'),
    url('^ShowUsers',ShowUsers, name='ShowUsers'),
    url('^pdfs',ejemplo_pdf, name='ejemplo_pdf'),
    url('^new_exam',agre_examen, name='agre_examen'),
    url('^show_examenes',show_examenes, name='show_examenes'),
    url('^CargarEstudiantes',CargarEstudiantes, name='CargarEstudiantes'),
    url('^ViwCargar',ViwCargar, name='ViwCargar'),
    url('^ViwPreguntas',ViwPreguntas, name='ViwPreguntas'),
    url('^ViwMateriaPre',ViwMateriaPre, name='ViwMateriaPre'),
    url('^EditPregunta',EditPregunta, name='EditPregunta'),
    url('^infoPregunta',infoPregunta, name='infoPregunta'),
    url('^delete_pregunta',delete_pregunta, name='delete_pregunta'),
    url('^grupos_viw',grupos_viw, name='grupos_viw'),
    url('^viw_estudiantes',viw_estudiantes, name='viw_estudiantes'),
    url('^viw_grados_estudiantes',viw_grados_estudiantes, name='viw_grados_estudiantes'),
    url('^update_estudiante',update_estudiante, name='update_estudiante'),
    url('^delete_user',delete_user, name='delete_user'),
    url('^delete_estudiante',delete_estudiante, name='delete_estudiante'),
    url('^agre_grupo',agre_grupo, name='agre_grupo'),
    url('^grupo_examen',grupo_examen, name='grupo_examen'),
    url('^materia_new',materia_new, name='materia_new'),
    url('^nivel_new',nivel_new, name='nivel_new'),
    url('^activar_exam',activar_exam, name='activar_exam'),
    url('^desactivar_exam',desactivar_exam, name='desactivar_exam'),
    url('^ShowEditExamen',ShowEditExamen, name='ShowEditExamen'),
    url('^EditExamen',EditExamen, name='EditExamen'),
    url('^update_user',update_user, name='update_user'),
    url('^edit_nivel',edit_nivel, name='edit_nivel'),
    url('^delete_nivel',delete_nivel, name='delete_nivel'),
    url('^edit_grado',edit_grado, name='edit_grado'),
    url('^delete_grado',delete_grado, name='delete_grado'),
    url('^edit_materia',edit_materia, name='edit_materia'),
    url('^delete_materia',delete_materia, name='delete_materia'),
    url('^archivo',archivo, name='archivo'),
    url('^test',test, name='test'),
    url('^$',index, name='index'),



    url(r'^admin/', admin.site.urls)
]
