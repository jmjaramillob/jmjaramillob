from django.db import models
from ..proyecto.models import Proyecto, Tecnica
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from .choices import TIPOS_SESION


"""MODELO  ESCALA CROMATICA------------------------------------------------------------------------------"""


class Escala(models.Model):

    nombre = models.TextField()
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Escala Cromática'
        verbose_name_plural = 'Escalas Cromáticas'

    def __str__(self):
        return u'{0}'.format(self.nombre)


"""MODELO OPCIONES DE LA ESCALA------------------------------------------------------------------------------"""


class OpcionEscala(models.Model):

    nombre = models.TextField()
    abreviacion = models.CharField(max_length=1)
    codigoColor = models.TextField(null=True)
    descripcion = models.TextField(null=True, blank=True)
    idEscala = models.ForeignKey(Escala, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Opción Escala Cromática'
        verbose_name_plural = 'Opciones Escalas Cromáticas'
        unique_together = ('nombre', 'abreviacion', 'idEscala')

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.nombre, self.abreviacion, self.idEscala)


"""MODELO ESTUDIO ABACO DE REGNIER-----------------------------------------------------------------------"""


class EstudioAbaco(models.Model):

    tipoTecnica = models.ForeignKey(Tecnica, null=True)  # el tipo se agrega mandando e objeto por contexto
    titulo = models.CharField(max_length=200)
    tematica = models.TextField()
    idAdministrador = models.ForeignKey(User, verbose_name='Administrador', related_name='abaco_administrador')
    idCoordinadores = models.ManyToManyField(User, verbose_name='Coordinadores', related_name='abaco_coordinadores_set')
    idExpertos = models.ManyToManyField(User, verbose_name='Expertos', related_name='abaco_expertos_set')
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField(default=now)
    estado = models.BooleanField(default=True)
    idEscala = models.ForeignKey(Escala, null=True)
    idProyecto = models.ForeignKey(Proyecto, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Estudio Abaco de Regnier'
        verbose_name_plural = 'Estudios Abaco de Regnier'
        unique_together = [('titulo', 'tipoTecnica', 'idProyecto')]

    def get_absolute_url(self):
        return reverse('proyecto:ver_estudios_proyecto', args={self.idProyecto.id})

    def __str__(self):
        return u'{0}'.format(self.titulo)


"""MODELO SESIONES-------------------------------------------------------------------------------------------"""


class Sesion(models.Model):

    numero_sesion = models.IntegerField()
    tipo = models.IntegerField(choices=TIPOS_SESION)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField(default=now)
    estado = models.BooleanField(default=True)
    idEstudio = models.ForeignKey(EstudioAbaco, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sesion de ábaco de Regnier'
        verbose_name_plural = 'Sesiones de ábaco de Regnier'
        unique_together = ('numero_sesion', 'idEstudio')

    def get_absolute_url(self):
        return reverse('abaco:sesiones', args={self.idEstudio.id})

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.numero_sesion, self.tipo, self.idEstudio)


"""MODELO IDEA-------------------------------------------------------------------------------------------"""


class Idea(models.Model):

    titulo = models.TextField()
    descripcion = models.TextField(null=True, blank=True)
    idCreador = models.ForeignKey(User, null=True)
    fecha = models.DateField(auto_now=True)
    estado = models.BooleanField(default=False) # el estado solo podra ser cambiado por el admin y los coordinadores
    idEstudio = models.ForeignKey(EstudioAbaco, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Idea'
        verbose_name_plural = 'Ideas'
        unique_together = ('titulo', 'idEstudio')

    def get_absolute_url(self):
        return reverse('abaco:ideas', args={self.idEstudio.id})

    def __str__(self):
        return u'{0}'.format(self.titulo)


"""MODELO REGLA-------------------------------------------------------------------------------------------"""


class Regla(models.Model):

    titulo = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    idEstudio = models.ForeignKey(EstudioAbaco, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Regla'
        verbose_name_plural = 'Reglas'
        unique_together = ('titulo', 'idEstudio')

    def get_absolute_url(self):
        return reverse('abaco:reglas', args={self.idEstudio.id})

    def __str__(self):
        return u'{0}'.format(self.titulo)


"""MODELO VALORACION IDEA------------------------------------------------------------------------------"""


class ValoracionIdea(models.Model):

    idIdea = models.ForeignKey(Idea, default=0, on_delete=models.CASCADE)
    valoracion = models.ForeignKey(OpcionEscala, null=True)
    justificacion = models.TextField()
    fechaHora = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)  # para manejos de cambios en el valor de las evaluaciones
    idExperto = models.ForeignKey(User, null=True)

    class Meta:
        verbose_name = 'Valoracion Idea'
        verbose_name_plural = 'Valoraciones Ideas registradas'

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idIdea, self.valoracion, self.estado)







