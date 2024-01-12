from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from apps.proyecto.models import Tecnica, Proyecto
from django.contrib.auth.models import User
# Create your models here.

class EstudioMultipol(models.Model):
  titulo = models.CharField(max_length=25, verbose_name="Título")
  descripcion = models.TextField(max_length=200, verbose_name="Descripción")
  idProyecto = models.ForeignKey(Proyecto, null=True, on_delete=models.CASCADE, related_name="proyecto_estudio_multipol")
  tipoTecnica = models.ForeignKey(Tecnica, null=True, related_name='tecnica_estudio_multipol')
  fecha_inicio = models.DateField(default=now)
  fecha_final = models.DateField(default=now)
  estado = models.BooleanField(default=True)
  idAdministrador = models.ForeignKey(User, null=True, related_name='administrador_estudio_multipol')
  idCoordinador = models.ForeignKey(User, null=True, related_name='coordinador_estudio_multipol')
  idExpertos = models.ManyToManyField(User, related_name='expertos_estudio_multipol')
  dias_finalizacion_informe = models.PositiveIntegerField(default=5)

  class Meta:
    verbose_name = "Multipol"
    verbose_name_plural = "Multipols"
    unique_together = [('titulo', 'tipoTecnica', 'idProyecto')]

  def get_absolute_url(self):
    return reverse('proyecto:ver_estudios_proyecto', args={self.idProyecto.id})

  def __str__(self):
    return u'{0} - {1}'.format(self.id, self.titulo)


# clase para las acciones del proyecto
class Accion(models.Model):
  estudio = models.ForeignKey(EstudioMultipol, null=True, on_delete=models.CASCADE, related_name="accions")
  short_name = models.CharField(max_length=10, verbose_name='Nombre Corto Acción',)
  long_name = models.CharField(max_length=50, verbose_name='Nombre Largo Acción',)
  description = models.TextField(max_length=100, verbose_name='Descripción Acción',)

  class Meta:
    verbose_name = 'Acción'
    verbose_name_plural = 'Acciones'

  def get_absolute_url(self):
    return reverse('multipol:lista_accion', args={self.estudio.id})

  def __str__(self):
    return self.short_name


# clase para las políticas defifidas del proyecto
class Politica(models.Model):
  estudio = models.ForeignKey(EstudioMultipol, null=True, on_delete=models.CASCADE, related_name="politicas")
  short_name = models.CharField(max_length=10, verbose_name='Nombre Corto Política',)
  long_name = models.CharField(max_length=50, verbose_name='Nombre Largo Política',)
  peso = models.IntegerField(default=1, verbose_name='Peso Política')
  description = models.TextField(max_length=100, verbose_name='Descripción Política', )

  class Meta:
    verbose_name = 'Política'
    verbose_name_plural = 'Políticas'

  def get_absolute_url(self):
    return reverse('multipol:lista_politica', args={self.estudio.id})

  def __str__(self):
    return self.short_name
  
  
# clase para los criterios establecidos del proyecto
class Criterio(models.Model):
  estudio = models.ForeignKey(EstudioMultipol, null=True, on_delete=models.CASCADE, related_name="criterios")
  short_name = models.CharField(max_length=10, verbose_name='Nombre Corto Critetio',)
  long_name = models.CharField(max_length=50, verbose_name='Nombre Largo Criterio',)
  peso = models.IntegerField(default=1, verbose_name='Peso Criterio') 
  description = models.TextField(max_length=100, verbose_name='Descripción Criterio',)

  class Meta:
    verbose_name = 'Criterio'
    verbose_name_plural = 'Criterios'

  def get_absolute_url(self):
    return reverse('multipol:lista_criterio', args={self.estudio.id})

  def __str__(self):
    return self.short_name
  

  # clase para las evaluaciones de criterios respecto a políticas
class EvaluacionCriterioPolitica(models.Model):
  estudio = models.ForeignKey(EstudioMultipol, null=True, on_delete=models.CASCADE, )
  criterio = models.ForeignKey(Criterio, null=True, )
  politica = models.ForeignKey(Politica, null=True, )
  puntuacion = models.PositiveIntegerField(default=0, verbose_name='Valoración')
  opinion = models.CharField(verbose_name='evaluaciones', max_length=200)
  experto = models.ForeignKey(User, on_delete=models.CASCADE,)

  class Meta:
    verbose_name = 'Evaluación Criterio/Política'

  def get_absolute_url(self):
    return reverse('multipol:detalle_estudio', args={self.estudio.id})
  
  def tiene_valoracion(self):
    return bool(self.puntuacion)

  def __str__(self):
    return str(self.puntuacion)
  

# clase para las evaluaciones de criterios respecto a acciones
class EvaluacionCriterioAccion(models.Model):
  estudio = models.ForeignKey(EstudioMultipol, null=True, on_delete=models.CASCADE,)
  criterio = models.ForeignKey(Criterio, null=True, )
  accion = models.ForeignKey(Accion, null=True, )
  puntuacion = models.PositiveIntegerField(verbose_name='Valoración', null=True, blank=True)
  opinion = models.CharField(verbose_name='Opinión', max_length=200, blank=True)
  experto = models.ForeignKey(User, on_delete=models.CASCADE, )

  def tiene_valoracion(self):
    return bool(self.puntuacion)

  class Meta:
    verbose_name = 'Evaluación Criterio Acción'
    verbose_name_plural = 'Evaluaciones Criterio Acción'

  def get_absolute_url(self):
    return reverse('multipol:detalle_estudio', args={self.estudio.id})

  def __str__(self):
    return f'estudio: {self.estudio} - eval: {self.puntuacion}'