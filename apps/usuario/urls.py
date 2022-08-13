from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import RegistrarUsuarioProyecto, RegistrarUsuarioEstudio

urlpatterns = [
    # si id = 0, se esta agregando un usuario desde la vista de creacion
    # si id != 0 se esta agregando un usuario desde la vista de edicion
    url(r'^registrar_usuario_proyecto/(?P<id>\d+)/$', login_required(RegistrarUsuarioProyecto.as_view()), name='registrar_usuario_proyecto'),
    url(r'^registrar_usuario_estudio/(?P<idProyecto>\d+)/(?P<tipoEstudio>\d+)/(?P<idEstudio>\d+)/$', login_required(RegistrarUsuarioEstudio.as_view()), name='registrar_usuario_estudio'),
    ]
