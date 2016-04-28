# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Caso(models.Model):
    enunciado = models.TextField()

    class Meta:
        
        db_table = 'caso'


class Estudiante(models.Model):
    nombre = models.CharField(max_length=50)
    documento = models.CharField(unique=True, max_length=12)
    genero = models.CharField(max_length=9)

    class Meta:
        
        db_table = 'estudiante'


class EstudianteGrupo(models.Model):
    estado = models.CharField(max_length=2)
    estudiante = models.ForeignKey(Estudiante, models.DO_NOTHING)
    grupo = models.ForeignKey('Grupo', models.DO_NOTHING)

    class Meta:
        
        db_table = 'estudiante_grupo'


class Examen(models.Model):
    nombre = models.CharField(max_length=50)
    numero_preguntas = models.IntegerField()
    materia = models.ForeignKey('Materia', models.DO_NOTHING)

    class Meta:
        
        db_table = 'examen'


class ExamenGrupo(models.Model):
    examen = models.ForeignKey(Examen, models.DO_NOTHING)
    grupo = models.ForeignKey('Grupo', models.DO_NOTHING)

    class Meta:
        
        db_table = 'examen_grupo'


class Grupo(models.Model):
    nombre = models.CharField(max_length=20)
    nivel = models.ForeignKey('Nivel', models.DO_NOTHING)

    class Meta:
        
        db_table = 'grupo'


class Materia(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        
        db_table = 'materia'


class Nivel(models.Model):
    nombre = models.CharField(max_length=20)

    class Meta:
        
        db_table = 'nivel'


class Opcion(models.Model):
    enunciado = models.TextField()
    tipo = models.CharField(max_length=1)

    class Meta:
        
        db_table = 'opcion'


class OpcionTest(models.Model):
    opcion = models.ForeignKey(Opcion, models.DO_NOTHING)

    class Meta:
        
        db_table = 'opcion_test'


class Pemisos(models.Model):
    grupo = models.ForeignKey(Grupo, models.DO_NOTHING)
    materia = models.ForeignKey(Materia, models.DO_NOTHING)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)

    class Meta:
        
        db_table = 'pemisos'


class Perfil(models.Model):
    nombre = models.CharField(max_length=50)
    documento = models.CharField(max_length=12)
    cargo = models.CharField(max_length=20)
    genero = models.CharField(max_length=12)

    class Meta:
        
        db_table = 'perfil'


class Pregunta(models.Model):
    enunciado = models.TextField()
    numero_opciones = models.IntegerField()
    caso = models.ForeignKey(Caso, models.DO_NOTHING, blank=True, null=True)
    materia = models.ForeignKey(Materia, models.DO_NOTHING)
    nivel = models.ForeignKey(Nivel, models.DO_NOTHING)

    class Meta:
        
        db_table = 'pregunta'


class PreguntaOpcion(models.Model):
    opcion = models.ForeignKey(Opcion, models.DO_NOTHING)
    pregunta = models.ForeignKey(Pregunta, models.DO_NOTHING)

    class Meta:

        db_table = 'pregunta_opcion'


class Respuesta(models.Model):
    opcion = models.ForeignKey(Opcion, models.DO_NOTHING)
    test = models.ForeignKey('Test', models.DO_NOTHING)

    class Meta:

        db_table = 'respuesta'


class Test(models.Model):
    estudiante = models.ForeignKey(Estudiante, models.DO_NOTHING)
    examen = models.ForeignKey(Examen, models.DO_NOTHING)
    pregunta = models.ForeignKey(Pregunta, models.DO_NOTHING)

    class Meta:

        db_table = 'test'


class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    grado = models.CharField(max_length=10)
    user = models.CharField(max_length=20)
    clave = models.CharField(max_length=128)

    class Meta:

        db_table = 'usuario'
