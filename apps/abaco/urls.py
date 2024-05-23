from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import CrearEstudio, ConsultarEstudio, EditarEstudio, EliminarEstudio,\
    ListaSesiones, CrearSesion, ConsultarSesion, EditarSesion, \
    ListaIdeas, CrearIdea, ConsultarIdea, EditarIdea, EliminarIdea, importar_ideas, \
    ListaReglas, CrearRegla, ConsultarRegla, EditarRegla, EliminarRegla, \
    ListaValoraciones, CrearValoracion, ConsultarValoracion, Resultados, grafico_totales_ideas,\
    datos_grafico_totales_ideas, exportar_estudio_xls, cambiar_estado

urlpatterns = [

    # Urls modelo Estudio Abaco de Regnier

    url(r'^agregar_estudio/(?P<pk>\d+)/$', login_required(CrearEstudio.as_view()), name='nuevo_estudio'),
    url(r'^consultar_estudio/(?P<pk>\d+)/$', login_required(ConsultarEstudio.as_view()), name='consultar_estudio'),
    url(r'^editar_estudio/(?P<pk>\d+)/$', login_required(EditarEstudio.as_view()), name='editar_estudio'),
    url(r'^eliminar_estudio/(?P<pk>\d+)/$', login_required(EliminarEstudio.as_view()), name='eliminar_estudio'),

    # Urls modelo Sesiones

    url(r'^sesiones/(?P<pk>\d+)/$', login_required(ListaSesiones.as_view()), name='sesiones'),
    url(r'^nueva_sesion/(\d+)/$', login_required(CrearSesion.as_view()), name='nueva_sesion'),
    url(r'^consultar_sesion/(?P<pk>\d+)/$', login_required(ConsultarSesion.as_view()), name='consultar_sesion'),
    url(r'^editar_sesion/(?P<pk>\d+)/$', login_required(EditarSesion.as_view()), name='editar_sesion'),

    # Urls modelo Ideas

    url(r'^ideas/(?P<pk>\d+)/$', login_required(ListaIdeas.as_view()), name='ideas'),
    url(r'^nueva_idea/(\d+)/$', login_required(CrearIdea.as_view()), name='nueva_idea'),
    url(r'^consultar_idea/(?P<pk>\d+)/$', login_required(ConsultarIdea.as_view()), name='consultar_idea'),
    url(r'^editar_idea/(?P<pk>\d+)/$', login_required(EditarIdea.as_view()), name='editar_idea'),
    url(r'^eliminar_idea/(?P<pk>\d+)/$', login_required(EliminarIdea.as_view()), name='eliminar_idea'),
    url(r'importar_ideas', login_required(importar_ideas)),

    # Urls modelo Reglas

    url(r'^reglas/(?P<pk>\d+)/$', login_required(ListaReglas.as_view()), name='reglas'),
    url(r'^nueva_regla/(\d+)/$', login_required(CrearRegla.as_view()), name='nueva_regla'),
    url(r'^consultar_regla/(?P<pk>\d+)/$', login_required(ConsultarRegla.as_view()), name='consultar_regla'),
    url(r'^editar_regla/(?P<pk>\d+)/$', login_required(EditarRegla.as_view()), name='editar_regla'),
    url(r'^eliminar_regla/(?P<pk>\d+)/$', login_required(EliminarRegla.as_view()), name='eliminar_regla'),

    # Urls modelo Valoraciones

    url(r'^valoraciones/(?P<pk>\d+)/$', login_required(ListaValoraciones.as_view()), name='valoraciones'),
    url(r'^nueva_valoracion/(?P<idEstudio>\d+)/(?P<idValoracion>\d+)/$', login_required(CrearValoracion.as_view()),
        name='nueva_valoracion'),
    url(r'^consultar_valoracion/(?P<pk>\d+)/(?P<tipoAcceso>\w+)/$', login_required(ConsultarValoracion.as_view()),
        name='consultar_valoracion'),
    url(r'^resultados/(?P<pk>\d+)/$', login_required(Resultados.as_view()), name='resultados'),
    url(r'^grafico_totales/(?P<idIdea>\d+)/$', login_required(grafico_totales_ideas), name='grafico_totales'),
    url(r'datos_grafico_totales', login_required(datos_grafico_totales_ideas)),

    # Urls exportar a excel
    url(r'exportar_estudio/xls/(?P<idEstudio>\d+)/$', login_required(exportar_estudio_xls), name='exportar_excel'),

    # cambiar estado por ajax de una idea, regla o sesion (solo si esta abierta)
    url(r'cambiar_estado', login_required(cambiar_estado)),

]
