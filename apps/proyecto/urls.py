from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import Listaproyectos, CrearProyecto, ConsultarProyecto, \
  EditarProyecto, EliminarProyecto, \
  ConsultarEstudiosProyecto, \
  EnviarMensaje, ConsultarMensaje, obtener_destinatarios, \
  cambiar_estado_mensaje, \
  EnviarMensajeEstudio, ConsultarMensajeEstudio, obtener_destinatarios_estudios

urlpatterns = [

  url(r'^proyectos_prospectivos', login_required(Listaproyectos.as_view()),
      name='proyectos_prospectivos'),
  url(r'^agregar_proyecto/$', login_required(CrearProyecto.as_view()),
      name='nuevo_proyecto'),
  url(r'^detalle_proyecto/(?P<pk>\d+)/$',
      login_required(ConsultarProyecto.as_view()), name='ver_proyecto'),
  url(r'^estudios_proyecto/(?P<pk>\d+)/$',
      login_required(ConsultarEstudiosProyecto.as_view()),
      name='ver_estudios_proyecto'),
  url(r'^editar_proyecto/(?P<pk>\d+)/$',
      login_required(EditarProyecto.as_view()), name='editar_proyecto'),
  url(r'^eliminar_proyecto/(?P<pk>\d+)/$',
      login_required(EliminarProyecto.as_view()), name='eliminar_proyecto'),

  # urls de mensajes
  url(r'obtener_destinatarios', login_required(obtener_destinatarios)),
  url(r'^mensajes_proyecto/(?P<pk>\d+)/$',
      login_required(EnviarMensaje.as_view()), name='mensajes'),
  url(r'^ver_mensaje/(?P<pk>\d+)/$', login_required(ConsultarMensaje.as_view()),
      name='ver_mensaje'),

  url(r'destinatarios_estudios',
      login_required(obtener_destinatarios_estudios)),
  url(r'^mensajes_estudios/(?P<pk>\d+)/(?P<tipoEstudio>\d+)/$',
      login_required(EnviarMensajeEstudio.as_view()), name='mensajes_estudio'),
  url(r'^ver_mensaje_estudio/(?P<pk>\d+)/$',
      login_required(ConsultarMensajeEstudio.as_view()),
      name='ver_mensaje_estudio'),
  url(r'cambiar_estado_mensaje', login_required(cambiar_estado_mensaje)),

]
