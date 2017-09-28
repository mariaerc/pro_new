from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Estudiante(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    grupo = models.ForeignKey('Grupo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estudiante'


class Caso(models.Model):
    nombre_caso = models.CharField(max_length=20)
    enunciado = models.TextField()

    class Meta:

        db_table = 'caso'

class ActivarExamen(models.Model):
    examen = models.ForeignKey('Examen', models.DO_NOTHING)
    inicio = models.DateField()
    fin = models.DateField()
    class Meta:

        db_table = 'activar_examen'
class Examen(models.Model):
    nombre = models.CharField(max_length=50)
    numero_preguntas = models.IntegerField()
    materia = models.ForeignKey('Materia', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'examen'

class Years(models.Model):
    año = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'years'


class ExamenGrupo(models.Model):
    examen = models.ForeignKey(Examen, models.DO_NOTHING)
    grupo = models.ForeignKey('Grupo', models.DO_NOTHING)
    periodo = models.CharField(max_length=20)
    año = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'examen_grupo'

class ExamenContestado(models.Model):
    estudiante = models.ForeignKey(Estudiante, models.DO_NOTHING)
    examen = models.ForeignKey(Examen, models.DO_NOTHING)
    grupo = models.ForeignKey('Grupo', models.DO_NOTHING)
    fpresentado = models.DateField()
    calificacion = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'examen_contestado'


class Grupo(models.Model):
    nombre = models.CharField(max_length=20)
    nivel = models.ForeignKey('Nivel', models.DO_NOTHING)
    jornada = models.CharField(max_length=25)
    class Meta:
        managed = False
        db_table = 'grupo'


class Materia(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'materia'


class Nivel(models.Model):
    nombre = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'nivel'


class Opcion(models.Model):
    enunciado = models.TextField()
    tipo = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'opcion'

class Pregunta(models.Model):
    enunciado = models.TextField()
    numero_opciones = models.IntegerField()
    caso = models.ForeignKey(Caso, models.DO_NOTHING, blank=True, null=True)
    materia = models.ForeignKey(Materia, models.DO_NOTHING)
    nivel = models.ForeignKey(Nivel, models.DO_NOTHING)
    imagen = models.CharField(max_length=50, null=True)
    class Meta:
        managed = False
        db_table = 'pregunta'


class PreguntaOpcion(models.Model):
    opcion = models.ForeignKey(Opcion, models.DO_NOTHING)
    pregunta = models.ForeignKey(Pregunta, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pregunta_opcion'


class Respuesta(models.Model):
    opcion = models.ForeignKey(Opcion, models.DO_NOTHING)
    test = models.ForeignKey('Test', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'respuesta'


class Test(models.Model):
    estudiante = models.ForeignKey(Estudiante, models.DO_NOTHING)
    examen = models.ForeignKey(Examen, models.DO_NOTHING)
    pregunta = models.ForeignKey(Pregunta, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'test'
class Docente(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    perfil = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'docente'
