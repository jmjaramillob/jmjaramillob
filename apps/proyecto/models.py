from django.db import models
from .choices import TIPOS_TECNICA
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.urlresolvers import reverse


# Modelo de Proyecto prospectivo


class Proyecto(models.Model):
  nombre = models.CharField(max_length=200)
  objetivo = models.TextField()
  fecha_inicio = models.DateField(default=now)
  fecha_final = models.DateField(default=now)
  estado = models.BooleanField(default=True)
  idAdministrador = models.ForeignKey(User, verbose_name='administrador',
                                      related_name='proyecto_administrador')
  idCoordinadores = models.ManyToManyField(User, verbose_name='coordinadores',
                                           related_name='proyecto_coordinadores_set')
  idExpertos = models.ManyToManyField(User, verbose_name='expertos',
                                      related_name='proyecto_expertos_set',
                                      blank=True)

  """el campo idExpertos se llenaria con los expertos agregados al registrar cada estudio"""

  class Meta:
    verbose_name = 'Proyecto prospectivo'
    verbose_name_plural = 'Proyectos prospectivos'
    unique_together = [('nombre', 'idAdministrador')]

  def get_absolute_url(self):
    return reverse('proyecto:proyectos_prospectivos')

  def __str__(self):
    return u'{0}'.format(self.nombre)


class FaseProspectiva(models.Model):
  nombre = models.CharField(max_length=50)
  objetivo = models.TextField()

  class Meta:
    verbose_name = 'Fase Prospectiva'
    verbose_name_plural = 'Fases Prospectivas'

  def __str__(self):
    return u'{0}'.format(self.nombre)


# Modelo de tecnica prospectiva


class Tecnica(models.Model):
  codigo = models.PositiveIntegerField(unique=True)
  nombre = models.CharField(max_length=50)
  tipo = models.CharField(max_length=20, null=True, choices=TIPOS_TECNICA)
  objetivo = models.TextField()
  descripcion = models.TextField()

  class Meta:
    verbose_name = 'Tecnica Prospectiva'
    verbose_name_plural = 'Tecnicas Prospectivas'

  def __str__(self):
    return u'{0}'.format(self.nombre)


class Mensaje(models.Model):
  idEmisor = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
  idDestinatarios = models.ManyToManyField(User, verbose_name='idDestinatarios',
                                           related_name='mensaje_dest')
  mensaje = models.TextField()
  fechaHora = models.DateTimeField(default=now)
  estado = models.BooleanField(default=False)  # sin leer o leido
  multiples = models.BooleanField(
    default=False)  # para verif si el mensaje tiene multiples destinatarios
  hijoMultiple = models.BooleanField(
    default=False)  # para saber si es hijo de un mensaje con multiples destinatarios
  enviadoMultiples = models.BooleanField(
    default=False)  # para saber si se enviaron los mensajes individuales
  idProyecto = models.ForeignKey(Proyecto, null=True, on_delete=models.CASCADE)
  idEstudio = models.PositiveIntegerField(null=True, default=0)
  tipoEstudio = models.PositiveIntegerField(null=True, default=0)
  tituloEstudio = models.TextField(default='Sin estudio')

  class Meta:
    verbose_name = 'Mensaje'
    verbose_name_plural = 'Mensajes del proyecto'

  def __str__(self):
    return u'{0}'.format(self.idProyecto)


#
# Sobreescritura del modelo usuario


def get_name(self):
  if self.first_name != '':
    return '{} {}'.format(self.first_name, self.last_name)
  else:
    return '{}'.format(self.username)


User.add_to_class("__str__", get_name)
