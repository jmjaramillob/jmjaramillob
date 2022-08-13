from django.db import models
from ..proyecto.models import Proyecto, Tecnica
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.urlresolvers import reverse

"""MODELO ESTUDIO MACTOR--------------------------------------------------------------------------------------------"""


class EstudioMactor(models.Model):

    tipoTecnica = models.ForeignKey(Tecnica, null=True) # el tipo se agrega mandando e objeto por contexto
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    idAdministrador = models.ForeignKey(User, verbose_name='administrador', related_name='mactor_administrador')
    idCoordinador = models.ForeignKey(User, verbose_name='coordinador', related_name='mactor_coordinador')
    idExpertos = models.ManyToManyField(User, verbose_name='Expertos', related_name='mactor_expertos_set')
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField(default=now)
    dias_finalizacion_informe = models.PositiveIntegerField(default=5)
    estado = models.BooleanField(default=True)
    idProyecto = models.ForeignKey(Proyecto, null=True, on_delete=models.CASCADE)

# Definicion de nombre singular y plural del modelo
    class Meta:
        verbose_name = 'Estudio Mactor'
        verbose_name_plural = 'Estudios Mactor'
        unique_together = [('titulo', 'tipoTecnica', 'idProyecto')]

    def get_absolute_url(self):
        return reverse('proyecto:ver_estudios_proyecto', args={self.idProyecto.id})

# Campo a mostrar del modelo Estudio_Mactor (tabla en admin y listas desplegables)
    def __str__(self):
        return u'{0}'.format(self.titulo)


"""MODELO ACTOR-----------------------------------------------------------------------------------------------------"""


class Actor(models.Model):

    nombreLargo = models.CharField(max_length=100)
    nombreCorto = models.CharField(max_length=5)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    idEstudio = models.ForeignKey(EstudioMactor, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actores'
        unique_together = [('nombreLargo', 'nombreCorto', 'idEstudio'),
                           ('nombreLargo', 'idEstudio'),
                           ('nombreCorto', 'idEstudio')]

    def get_absolute_url(self):
        return reverse('mactor:actores', args={self.idEstudio.id})

    def __str__(self):
        return u'{0} - {1}'.format(self.nombreCorto, self.nombreLargo)


"""MODELO FICHA DE ESTRATEGIAS--------------------------------------------------------------------------------------"""


class Ficha(models.Model):

    idActorY = models.ForeignKey(Actor, default=0, related_name='mactor_actorY_ficha', on_delete=models.CASCADE)
    idActorX = models.ForeignKey(Actor, default=0, related_name='mactor_actorX_ficha', on_delete=models.CASCADE)
    estrategia = models.TextField(default="", blank=False)

    class Meta:
        verbose_name = 'Ficha de estrategias'
        verbose_name_plural = 'Fichas de estrategia'
        unique_together = ('idActorY', 'idActorX')

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idActorX, self.idActorY, self.estrategia)


"""MODELO OBJETIVO--------------------------------------------------------------------------------------------------"""


class Objetivo(models.Model):

    nombreLargo = models.CharField(max_length=100)
    nombreCorto = models.CharField(max_length=5)
    descripcion = models.TextField(max_length=500, null=True, blank=True)
    idEstudio = models.ForeignKey(EstudioMactor, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'
        unique_together = [('nombreLargo', 'nombreCorto', 'idEstudio'),
                           ('nombreLargo', 'idEstudio'),
                           ('nombreCorto', 'idEstudio')]

    def get_absolute_url(self):
        return reverse('mactor:objetivos', args={self.idEstudio.id})

    def __str__(self):
        return u'{0} - {1}'.format(self.nombreCorto, self.nombreLargo)


"""MODELO RELACIONES DE INFLUENCIA DIRECTA---------------------------------------------------------------------------"""


class RelacionMID(models.Model):

    idActorX = models.ForeignKey(Actor, default=0, related_name='mactor_actorX_set', on_delete=models.CASCADE)
    idActorY = models.ForeignKey(Actor, default=0, blank=False, related_name='mactor_actorY_set', on_delete=models.CASCADE)
    valor = models.IntegerField()
    justificacion = models.TextField(default="Justificación de la relación entre los actores")
    idExperto = models.ForeignKey(User, null=True)

    class Meta:
        verbose_name = 'Relacion de Influencia'
        verbose_name_plural = 'Relaciones de influencia'
        unique_together = ('idActorX', 'idActorY', 'idExperto')

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idActorY, self.idActorX, self.valor)


"""MODELO RELACIONES DE ACTOR x OBJETIVO---------------------------------------------------------------------------"""


class RelacionMAO(models.Model):

    tipo = models.IntegerField(null=True, blank=True)
    idActorY = models.ForeignKey(Actor, default=0, on_delete=models.CASCADE)
    idObjetivoX = models.ForeignKey(Objetivo, default=0, on_delete=models.CASCADE)
    valor = models.IntegerField()
    justificacion = models.TextField(default="Justificación de la relación entre el actor y el objetivo")
    idExperto = models.ForeignKey(User, null=True)

    class Meta:
        verbose_name = 'Relacion MAO'
        verbose_name_plural = 'Relaciones MAO'
        unique_together = ('tipo', 'idActorY', 'idObjetivoX', 'idExperto')

    def __str__(self):
        return u'{0} - {1} - {2} - {3} - {4}'.format(self.tipo, self.idActorY, self.idObjetivoX, self.valor, self.idExperto)


"""MODELO INFORME FINAL---------------------------------------------------------------------------------------------"""


class InformeFinal(models.Model):

    fecha = models.DateTimeField(auto_now=True)
    informe = models.TextField()
    estado = models.BooleanField(default=False)
    idEstudio = models.ForeignKey(EstudioMactor, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Informe final'
        verbose_name_plural = 'Informes finales'

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idEstudio, self.fecha, self.informe, self.estado)


# Sobreescritura del modelo usuario


def get_name(self):
    if self.first_name != '':
        return '{} {}'.format(self.first_name, self.last_name)
    else:
        return '{}'.format(self.username)

User.add_to_class("__str__", get_name)


