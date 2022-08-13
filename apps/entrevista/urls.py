from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import CrearEstudio, EditarEstudio, ConsultarEstudio, EliminarEstudio, \
    ListaPreguntas, CrearPregunta, EditarPregunta, ConsultarPregunta, EliminarPregunta,\
    ListaValoresEscala, CrearValorEscala, EditarValorEscala, ConsultarValorEscala, EliminarValorEscala, \
    ListaRondas, CrearRonda, EditarRonda, ConsultarRonda, \
    ListaJuicios, CrearJuicio, ConsultarJuicio, EditarJuicio, MatrizJuicios, \
    ListaCoeficientes, GraficoCoeficiente, datos_grafico, exportar_estudio_xls, cambiar_estado_pregunta_escala_ronda

urlpatterns = [

    # Urls modelo Estudio_entrevista
    url(r'^agregar_estudio/(?P<pk>\d+)/$', CrearEstudio.as_view(), name='nuevo_estudio'),
    url(r'^editar_estudio/(?P<pk>\d+)/$', login_required(EditarEstudio.as_view()), name='editar_estudio'),
    url(r'^consultar_estudio/(?P<pk>\d+)/$', login_required(ConsultarEstudio.as_view()), name='consultar_estudio'),
    url(r'^eliminar_estudio/(?P<pk>\d+)/$', login_required(EliminarEstudio.as_view()), name='eliminar_estudio'),


    # Urls modelo Pregunta
    url(r'^lista_preguntas/(\d+)/$', login_required(ListaPreguntas.as_view()), name='preguntas'),
    url(r'^nueva_pregunta/(\d+)/$', login_required(CrearPregunta.as_view()), name='nueva_pregunta'),
    url(r'^editar_pregunta/(?P<pk>\d+)/$', login_required(EditarPregunta.as_view()), name='editar_pregunta'),
    url(r'^consultar_pregunta/(?P<pk>\d+)/$', login_required(ConsultarPregunta.as_view()), name='consultar_pregunta'),
    url(r'^eliminar_pregunta/(?P<pk>\d+)/$', login_required(EliminarPregunta.as_view()), name='eliminar_pregunta'),

    # Urls modelo Valor escala
    url(r'^escala_likert/(\d+)/$', login_required(ListaValoresEscala.as_view()), name='escala'),
    url(r'^nuevo_valor/(\d+)$', login_required(CrearValorEscala.as_view()), name='nuevo_valor'),
    url(r'^editar_valor/(?P<pk>\d+)/$', login_required(EditarValorEscala.as_view()), name='editar_valor'),
    url(r'^consultar_valor/(?P<pk>\d+)/$', login_required(ConsultarValorEscala.as_view()), name='consultar_valor'),
    url(r'^eliminar_valor/(?P<pk>\d+)/$', login_required(EliminarValorEscala.as_view()), name='eliminar_valor'),

    # Urls modelo Ronda Juicio
    url(r'^lista_rondas/(\d+)/$', login_required(ListaRondas.as_view()), name='rondas'),
    url(r'^registrar_ronda/(\d+)/$', login_required(CrearRonda.as_view()), name='nueva_ronda'),
    url(r'^editar_ronda/(?P<pk>\d+)/$', login_required(EditarRonda.as_view()), name='editar_ronda'),
    url(r'^consultar_ronda/(?P<pk>\d+)/$', login_required(ConsultarRonda.as_view()), name='consultar_ronda'),

    # Urls modelo Juicio
    url(r'^lista_juicios/(\d+)/$', login_required(ListaJuicios.as_view()), name='juicios'),
    url(r'^registrar_juicio/(\d+)/$', login_required(CrearJuicio.as_view()), name='nuevo_juicio'),
    url(r'^consultar_juicio/(?P<pk>\d+)/(?P<tipoAcceso>\w+)/$', login_required(ConsultarJuicio.as_view()),
        name='consultar_juicio'),
    url(r'^editar_juicio/(?P<pk>\d+)/$', login_required(EditarJuicio.as_view()), name='editar_juicio'),
    url(r'^matriz_juicios/(\d+)/$', login_required(MatrizJuicios.as_view()), name='matriz_juicios'),

    # Urls modelo coeficiente
    url(r'^historial_coeficientes/(\d+)/$', login_required(ListaCoeficientes.as_view()), name='historial_coeficientes'),
    url(r'^grafico_coeficiente/(\d+)/$', login_required(GraficoCoeficiente.as_view()), name='grafico'),
    url(r'datos_grafico_coef', login_required(datos_grafico)),

    # Urls exportar a excel
    url(r'exportar_estudio/xls/(?P<idEstudio>\d+)/$', login_required(exportar_estudio_xls), name='exportar_excel'),

    # cambiar por ajax el estado de una pregunta, opcion de la escala o ronda (solo si esta abierta)
    url(r'cambiar_estado', login_required(cambiar_estado_pregunta_escala_ronda)),

]
