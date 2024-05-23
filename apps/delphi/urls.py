from django.conf.urls import url
from apps.delphi.views import \
    (Nuevo_estudio_Delphi, ListaDelphi, EditarDelphi, EditarCuestionario, DetalleEstudio,
    CrearRonda, DetalleCuestionario, Crear_Cuestionario, EditarRonda)
urlpatterns = [
    url(r'^estudios_delphi', ListaDelphi.as_view(), name='estudios_delphi'),
    url(r'^detalle_estudio/(?P<pk>\d+)', DetalleEstudio.as_view(), name='Detalle_estudio'),
    url(r'^detalle_cuestionario/(?P<pk>\d+)', DetalleCuestionario.as_view(), name='detalle_cuestionario'),
    url(r'^nuevo_estudio', Nuevo_estudio_Delphi.as_view(), name='nuevo_estudio'),
    url(r'^editar_delphi/(?P<pk>\d+)/$', EditarDelphi.as_view(), name='editar_delphi'),
    url(r'^editar_cuestionario/(?P<pk>\d+)/$', EditarCuestionario.as_view(), name='editar_cuestionario'),
    url(r'^editar_ronda/(?P<pk>\d+)/$', EditarRonda.as_view(), name='editar_ronda'),
    url(r'^crear_cuestionario/(?P<pk>\d+)/$', Crear_Cuestionario.as_view(), name='crear_cuestionario'),
    url(r'^crear_ronda/(?P<pk>\d+)$', CrearRonda.as_view(), name='crear_ronda'),

]