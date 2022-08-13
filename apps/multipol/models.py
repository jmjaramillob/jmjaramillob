from datetime import date

from django.urls import reverse
from django.utils.timezone import now

from apps.proyecto.models import Tecnica, Proyecto
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.


# clase para definir los metadatos del estudio de multipol
class EstudioMultipol(models.Model):
  titulo = models.CharField(max_length=25, default="", verbose_name="Título")
  descripcion = models.TextField(max_length=200, default="",
                                 verbose_name="Descripción")
  idProyecto = models.ForeignKey(Proyecto, null=True, on_delete=models.CASCADE)
  tipoTecnica = models.ForeignKey(Tecnica, null=True)
  fecha_inicio = models.DateField(default=now)
  fecha_final = models.DateField(default=now)
  estado = models.BooleanField(default=True)
  idAdministrador = models.ForeignKey(User, null=True,
                                    related_name='Administrador')
  idCoordinador = models.ForeignKey(User,
                                       null=True, related_name='Coordinadores')
  idExpertos = models.ManyToManyField(User, related_name='Expertos')
  dias_finalizacion_informe = models.PositiveIntegerField(default=5)

  class Meta:
    verbose_name = "Estudio Multipol"
    verbose_name_plural = "Estudios Multipol"
    unique_together = [('titulo', 'tipoTecnica', 'idProyecto')]

  def get_absolute_url(self):
    return reverse('proyecto:ver_estudios_proyecto', args={self.idProyecto.id})

  def __str__(self):
    return u'{0}{1}'.format(self.id, self.titulo)


# clase para las acciones del proyecto
class Accion(models.Model):
  estudio = models.ForeignKey(EstudioMultipol, null=True,
                              on_delete=models.CASCADE)
  shortNameA = models.CharField(
    max_length=10,
    verbose_name='Nombre Corto Acción',
    default=""
  )
  longNameA = models.CharField(
    max_length=50,
    verbose_name='Nombre Largo Acción',
    default=""
  )
  descriptionA = models.TextField(
    max_length=100,
    verbose_name='Descripción Acción',
    default=""
  )

  class Meta:
    verbose_name = 'Acción'
    verbose_name_plural = 'Acciones'

  def get_absolute_url(self):
    return reverse(
      'multipol:lista_accion', args={self.estudio.id}
    )

  def __str__(self):
    return self.shortNameA


# clase para las políticas defifidas del proyecto
class Politica(models.Model):
  estudio = models.ForeignKey(EstudioMultipol, null=True,
                              on_delete=models.CASCADE)
  shortNameP = models.CharField(
    max_length=10,
    verbose_name='Nombre Corto Política',
    default=""
  )
  longNameP = models.CharField(
    max_length=50,
    verbose_name='Nombre Largo Política', default=""
  )
  pesoP = models.IntegerField(default=0, verbose_name='Peso Política')
  descriptionP = models.TextField(
    max_length=100,
    verbose_name='Descripción Política',
    default=""
  )

  class Meta:
    verbose_name = 'Política'
    verbose_name_plural = 'Políticas'

  def get_absolute_url(self):
    return reverse('multipol:lista_politica',
                   args={self.estudio.id})

  def __str__(self):
    return self.shortNameP


# clase para los criterios establecidos del proyecto
class Criterio(models.Model):
  estudio = models.ForeignKey(EstudioMultipol, null=True,
                              on_delete=models.CASCADE)
  shortNameC = models.CharField(
    max_length=10,
    verbose_name='Nombre Corto Critetio',
    default=""
  )
  longNameC = models.CharField(
    max_length=50,
    verbose_name='Nombre Largo Criterio',
    default=""
  )
  pesoC = models.IntegerField(default=0, verbose_name='Peso Criterio') #validator min =1
  descriptionC = models.TextField(
    max_length=100,
    verbose_name='Descripción Criterio',
    default=""
  )

  class Meta:
    verbose_name = 'Criterio'
    verbose_name_plural = 'Criterios'

  def get_absolute_url(self):
    return reverse('multipol:lista_criterio', args={self.estudio.id})

  def __str__(self):
    return self.shortNameC


# clase para las evaluaciones de criterios respecto a políticas
class EvaluacionCP(models.Model):
  estudio = models.ForeignKey(EstudioMultipol, null=True,
                              on_delete=models.CASCADE)
  criterio = models.ForeignKey(Criterio, null=True)
  politica = models.ForeignKey(Politica, null=True)
  valoracionCP = models.PositiveIntegerField(default=0, verbose_name='Valoración')
  opinion = models.CharField(default="", null=True, verbose_name='Opinión', max_length=200)
  idExperto = models.ForeignKey(User, on_delete=models.CASCADE)

  def getPolitica(self):
    return self.politica.id

  def getCriterios(self):
    return self.criterio.id

  class Meta:
    verbose_name = 'Evaluación Criterio/Política'

  def get_absolute_url(self):
    return reverse('multipol:detalle_estudio', args={self.estudio.id})

  def __str__(self):
    return str(self.valoracionCP)

#class EvaluacionTotalCA(models.Model):
  '''
    Aqui van todas las evaluaciones CA
  '''
#  estudio = models.ForeignKey(EstudioMultipol, null=True, on_delete=models.CASCADE)
#  fecha = models.DateTimeField(auto_now_add=True)
#  fecha_editado = models.DateTimeField(auto_now=True)



# clase para las evaluaciones de criterios respecto a acciones
class EvaluacionCA(models.Model):
  '''
    esta es una calificación entre los criterios y las acciones
  '''
  estudio = models.ForeignKey(EstudioMultipol, null=True,
                              on_delete=models.CASCADE)
  #Evaluacion_total = models.ForeignKey(EvaluavionTotalCA, on_delete=models.CASCADE)

  criterio = models.ForeignKey(Criterio, null=True)
  accion = models.ForeignKey(Accion, null=True)
  valoracionCA = models.PositiveIntegerField(verbose_name='Valoración', null=True, blank=True)
  opinion = models.CharField(verbose_name='Opinión', max_length=200, null=True, blank=True)
  idExperto = models.ForeignKey(User, on_delete=models.CASCADE)

  def tiene_valoracion(self):
    return self.valoracionCA != null #toca cambiar si vamos a poner predeterminado valor 0

  class Meta:
    verbose_name = 'Evaluación Criterio/Acción'
    verbose_name_plural = 'Evaluaciones Criterio/Acción'

  def get_absolute_url(self):
    return reverse('multipol:detalle_estudio',
                   args={self.estudio.id})

  def __str__(self):
    return f'estudio: {self.estudio} - eval: {self.valoracionCA}'

# Clase para los informes del estudio multipol #########################################################
class InformeFinal(models.Model):
  fecha = models.DateTimeField(auto_now=True)
  informe = models.TextField()
  estado = models.BooleanField(default=False)
  idEstudio = models.ForeignKey(EstudioMultipol, default=0, on_delete=models.CASCADE)

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