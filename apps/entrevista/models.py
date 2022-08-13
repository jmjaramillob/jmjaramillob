from django.db import models
from ..proyecto.models import Proyecto, Tecnica
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.urlresolvers import reverse

"""MODELO ESTUDIO ENTREVISTA---------------------------------------------------------------------------------"""


class EstudioEntrevista(models.Model):

    tipoTecnica = models.ForeignKey(Tecnica, null=True)  # el tipo se agrega mandando e objeto por contexto
    titulo = models.CharField(max_length=200)
    objetivo = models.TextField()
    entrevistador = models.CharField(max_length=50, null=True, blank=True)
    entrevistado = models.CharField(max_length=50)
    idAdministrador = models.ForeignKey(User, verbose_name='Administrador', related_name='ent_administrador')
    idCoordinador = models.ForeignKey(User, verbose_name='Coordinador', related_name='ent_coordinador')
    idExpertos = models.ManyToManyField(User, verbose_name='Expertos', related_name='ent_expertos_set')
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField(default=now)
    estado = models.BooleanField(default=True)
    idProyecto = models.ForeignKey(Proyecto, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Estudio entrevista'
        verbose_name_plural = 'Estudios entrevista'
        unique_together = [('titulo', 'tipoTecnica', 'idProyecto')]

    def get_absolute_url(self):
        return reverse('proyecto:ver_estudios_proyecto', args={self.idProyecto.id})

    def __str__(self):
        return u'{0}'.format(self.titulo)

"""MODELO PREGUNTA-------------------------------------------------------------------------------------------"""


class Pregunta(models.Model):

    texto_pregunta = models.TextField()
    texto_respuesta = models.TextField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    idEstudio = models.ForeignKey(EstudioEntrevista, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        unique_together = ('texto_pregunta', 'idEstudio')

    def get_absolute_url(self):
        return reverse('entrevista:preguntas', args={self.idEstudio.id})

    def __str__(self):
        return u'{0}'.format(self.texto_pregunta)


"""MODELO VALOR ESCALA LIKERT----------------------------------------------------------------------------------"""


class ValorEscalaLikert(models.Model):

    nombre = models.TextField()
    valor = models.IntegerField()
    estado = models.BooleanField(default=True)
    descripcion = models.TextField(null=True, blank=True)
    idEstudio = models.ForeignKey(EstudioEntrevista, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Escala de Likert'
        verbose_name_plural = 'Escala de Likert'
        unique_together = [('nombre', 'valor', 'estado', 'idEstudio')]

    def get_absolute_url(self):
        return reverse('entrevista:escala', args={self.idEstudio.id})

    def __str__(self):
        return u'{0}'.format(self.nombre)


"""MODELO RONDA JUICIO---------------------------------------------------------------------------------------"""


class RondaJuicio(models.Model):

    numero_ronda = models.IntegerField()
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField()
    estado = models.BooleanField(default=True)
    numero_preguntas = models.IntegerField(default=1)
    idEstudio = models.ForeignKey(EstudioEntrevista, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ronda de juicio'
        verbose_name_plural = 'Rondas de juicio'
        unique_together = ('numero_ronda', 'idEstudio')

    def get_absolute_url(self):
        return reverse('entrevista:rondas', args={self.idEstudio.id})

    def __str__(self):
        return u'{0} - {1}'.format(self.numero_ronda, self.idEstudio)


"""MODELO JUICIO DE EXPERTOS----------------------------------------------------------------------------------------"""


class Juicio(models.Model):

    texto_pregunta = models.TextField()
    idValorEscala = models.ForeignKey(ValorEscalaLikert, default=0, on_delete=models.CASCADE)
    justificacion = models.TextField(null=True, blank=True)
    idExperto = models.ForeignKey(User, null=True)
    idRonda = models.ForeignKey(RondaJuicio, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Juicio de expertos'
        verbose_name_plural = 'Juicios de los expertos'
        unique_together = ('texto_pregunta', 'idExperto', 'idRonda')

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.texto_pregunta, self.idValorEscala, self.idRonda)


"""MODELO COEFICIENTE ALFA DE CRONBACH------------------------------------------------------------------------------"""


class CoeficienteAlfa(models.Model):

    valor = models.FloatField()
    idRonda = models.ForeignKey(RondaJuicio, default=0, on_delete=models.CASCADE)
    num_expertos = models.IntegerField()

    class Meta:
        verbose_name = 'Coeficiente Alfa de Cronbach'
        verbose_name_plural = 'Coeficiente Alfa de Cronbach'

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idRonda, self.valor, self.num_expertos)


# Sobreescritura del modelo usuario


def get_name(self):
    if self.first_name != '':
        return '{} {}'.format(self.first_name, self.last_name)
    else:
        return '{}'.format(self.username)

User.add_to_class("__str__", get_name)

