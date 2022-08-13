from django.db import models
from django.template import defaultfilters
from django.utils.timezone import now
# Create your models here.


class Delphi(models.Model):
    proyecto = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    objetivos = models.TextField()
    expertos = models.ManyToManyField('auth.User', related_name='Delphi_expertos')
    coordinadores = models.ManyToManyField('auth.User', related_name='Delphi_coordinadores')
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField()
    estado = models.BooleanField()
    slug = models.SlugField(unique=True)


    class Meta:
        verbose_name_plural = 'Delphi'
        verbose_name = 'Delphi'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.titulo)
        super(Delphi, self).save(*args, **kwargs)



class Cuestionario(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField()
    delphi = models.ForeignKey('Delphi', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='cuestionario_delphi')
    expertos = models.ManyToManyField('auth.User', related_name='cuestionario_expertos')
    coordinadores = models.ManyToManyField('auth.User', related_name='cuestionario_cordinadores')

    class Meta:
        verbose_name_plural = 'Cuestionarios'
        verbose_name = 'Cuestionario'

    def __str__(self):
        return self.nombre



class RondasDelphi(models.Model):
    delphi = models.ForeignKey('Delphi', null=True, blank=True, on_delete=models.CASCADE, related_name='ronda_delphi')
    numero = models.PositiveIntegerField()
    cuestionario = models.ForeignKey('Cuestionario', verbose_name='Cuestionario')
    abierto = models.BooleanField(default=True, help_text='Dice si se pueden votar o no las preguntas.')
    expertos = models.ManyToManyField('auth.User', related_name='ronda_expertos')
    coordinadores = models.ManyToManyField('auth.User', related_name='ronda_cordinadores')
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField(default=now)
