from django.db import models
from ..proyecto.models import Proyecto, Tecnica
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.urlresolvers import reverse

"""MODELO ESTUDIO LLUVIA DE IDEAS-----------------------------------------------------------------------"""


class EstudioLluviaDeIdeas(models.Model):

    tipoTecnica = models.ForeignKey(Tecnica, null=True)
    titulo = models.CharField(max_length=200)
    tematica = models.TextField()
    idAdministrador = models.ForeignKey(User, verbose_name='Administrador', related_name='lluvia_administrador')
    idCoordinador = models.ForeignKey(User, verbose_name='coordinador', related_name='lluvia_coordinador', default=1)
    idExpertos = models.ManyToManyField(User, verbose_name='Participantes', related_name='lluvia_participantes_set')
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField(default=now)
    estado = models.BooleanField(default=True)
    idProyecto = models.ForeignKey(Proyecto, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Estudio Lluvia de Ideas'
        verbose_name_plural = 'Estudios Lluvia de ideas'
        unique_together = [('titulo', 'tipoTecnica', 'idProyecto')]

    def get_absolute_url(self):
        return reverse('proyecto:ver_estudios_proyecto', args={self.idProyecto.id})

    def __str__(self):
        return u'{0}'.format(self.titulo)


"""MODELO SESION ---------------------------------------------------------------------------------------"""


class Sesion(models.Model):

    numero_sesion = models.IntegerField()
    descripcion = models.TextField(null=True, blank=True)
    permitir_ideas = models.BooleanField(default=False, help_text='Indica si se puede llevar a cabo la creación de'
                                                                  ' ideas, si esta desactivado se puede votar por las'
                                                                  ' ideas ya creadas.')
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField(default=now)
    estado = models.BooleanField(default=True, help_text='Indica si se pueden votar o no las ideas.')
    idEstudio = models.ForeignKey(EstudioLluviaDeIdeas, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sesion de lluvia de ideas'
        verbose_name_plural = 'Sesiones de lluvia de ideas'
        unique_together = ('numero_sesion', 'idEstudio')

    def __str__(self):
        return u'{0} - {1}'.format(self.numero_sesion, self.idEstudio)


"""MODELO REGLA-------------------------------------------------------------------------------------------"""


class Regla(models.Model):

    titulo = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    idEstudio = models.ForeignKey(EstudioLluviaDeIdeas, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Regla'
        verbose_name_plural = 'Reglas'
        unique_together = ('titulo', 'idEstudio')

    def __str__(self):
        return u'{0}'.format(self.titulo)


"""MODELO IDEA-------------------------------------------------------------------------------------------"""


class Idea(models.Model):

    titulo = models.TextField()
    descripcion = models.TextField(null=True, blank=True)
    idCreador = models.ForeignKey(User, null=True,  related_name='creador_idea_set')
    fecha = models.DateField(auto_now=True)
    estado = models.BooleanField(default=False)  # el estado solo podra ser cambiado por el admin y los coordinadores
    idEstudio = models.ForeignKey(EstudioLluviaDeIdeas, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Idea'
        verbose_name_plural = 'Ideas'
        unique_together = ('titulo', 'idEstudio')

    def __str__(self):
        return u'{0}'.format(self.titulo)


"""MODELO VALORACION IDEA------------------------------------------------------------------------------"""


class ValoracionIdea(models.Model):

    idIdea = models.ForeignKey(Idea, default=0, on_delete=models.CASCADE)
    valoracion = models.BooleanField(default=False)
    justificacion = models.TextField()
    fechaHora = models.DateTimeField(auto_now_add=True)
    idParticipante = models.ForeignKey(User, null=True,  related_name='valoracion_participante_set')

    class Meta:
        verbose_name = 'Valoracion Idea'
        verbose_name_plural = 'Valoraciones Ideas registradas'

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idIdea, self.valoracion, self.estado)


"""MODELO ETAPA PLAN DE ACCION-------------------------------------------------------------------------------"""


class EtapaPlanAccion(models.Model):

    numero = models.PositiveIntegerField()
    titulo = models.TextField()
    descripcion = models.TextField(null=True, blank=True)
    idIdea = models.ForeignKey(Idea, default=0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Etapa del plan de acción'
        verbose_name_plural = 'Etapas del plan de acción'
        unique_together = ('numero', 'titulo', 'idIdea')

    def __str__(self):
        return u'{0}'.format(self.titulo)

#
