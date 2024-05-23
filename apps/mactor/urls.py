from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import CrearEstudio, ConsultarEstudio, EditarEstudio, EliminarEstudio, \
    ListaActores, CrearActor, EditarActor, EliminarActor, consultar_actor, importar_actores_fichas, \
    ListaFichas, CrearFicha, EditarFicha, EliminarFicha, ConsultarFicha, \
    ListaObjetivos, CrearObjetivo, EditarObjetivo, EliminarObjetivo, consultar_objetivo, importar_objetivos, \
    ListaInfluenciasMID, CrearInfluenciaMID, EditarInfluenciaMID, ConsultarInfluenciaMID, \
    generar_matriz_mid, generar_matriz_midi, generar_matriz_maxima, generar_matriz_ri, \
    generar_matriz_balance, generar_indicador_estabilidad,\
    ListaRelacionesMAO, CrearRelacionMAO, EditarRelacionMAO, \
    ConsultarRelacionMAO, generar_matriz_mao, generar_matrices_caa_daa, generar_lista_descendiente,\
    consultar_actores_faltantes, \
    EditarInformeFinal, exportar_estudio_xls, \
    histograma_mid, datos_histograma_mid, histograma_ri, datos_histograma_ri, \
    histograma_implicacion, histograma_movilizacion, datos_histogramas_mao,  \
    datos_histograma_caa_daa, histograma_caa_daa, \
    generar_mapa_midi, datos_mapa_midi, generar_mapa_caa_daa, datos_mapa_caa_daa, \
    generar_grafo_caa, datos_grafo_caa, generar_grafo_daa, datos_grafo_daa, \
    activar_consenso_mid, activar_consenso_mao, activar_consenso_caa_daa

urlpatterns = [

    # Urls modelo Estudio_mactor

    url(r'^agregar_estudio/(?P<pk>\d+)/$', login_required(CrearEstudio.as_view()), name='nuevo_estudio'),
    url(r'^consultar_estudio/(?P<pk>\d+)/$', login_required(ConsultarEstudio.as_view()), name='consultar_estudio'),
    url(r'^editar_estudio/(?P<pk>\d+)/$', login_required(EditarEstudio.as_view()), name='editar_estudio'),
    url(r'^eliminar_estudio/(?P<pk>\d+)/$', login_required(EliminarEstudio.as_view()), name='eliminar_estudio'),

    # Urls modelo Actor
    url(r'^actores/(\d+)/$', login_required(ListaActores.as_view()), name='actores'),
    url(r'^nuevo_actor/(\d+)/$', login_required(CrearActor.as_view()), name='nuevo_actor'),
    url(r'^editar_actor/(?P<pk>\d+)/$', login_required(EditarActor.as_view()), name='editar_actor'),
    url(r'^eliminar_actor/(?P<pk>\d+)/$', login_required(EliminarActor.as_view()), name='eliminar_actor'),
    url(r'consultar_actor', login_required(consultar_actor)),
    url(r'importar_actores_fichas', login_required(importar_actores_fichas)),

    # Urls modelo Ficha
    url(r'^fichas/(\d+)/$', login_required(ListaFichas.as_view()), name='fichas'),
    url(r'^nueva_ficha/(\d+)/$', login_required(CrearFicha.as_view()), name='nueva_ficha'),
    url(r'^editar_ficha/(?P<pk>\d+)/$', login_required(EditarFicha.as_view()), name='editar_ficha'),
    url(r'^consultar_ficha/(?P<pk>\d+)/$', login_required(ConsultarFicha.as_view()), name='consultar_ficha'),
    url(r'^eliminar_ficha/(?P<pk>\d+)/$', login_required(EliminarFicha.as_view()), name='eliminar_ficha'),

    # Urls modelo Objetivo
    url(r'^objetivos/(\d+)/$', login_required(ListaObjetivos.as_view()), name='objetivos'),
    url(r'^nuevo_objetivo/(\d+)/$', login_required(CrearObjetivo.as_view()), name='nuevo_objetivo'),
    url(r'^editar_objetivo/(?P<pk>\d+)/$', login_required(EditarObjetivo.as_view()), name='editar_objetivo'),
    url(r'^eliminar_objetivo/(?P<pk>\d+)/$', login_required(EliminarObjetivo.as_view()), name='eliminar_objetivo'),
    url(r'consultar_objetivo', login_required(consultar_objetivo)),
    url(r'importar_objetivos', login_required(importar_objetivos)),

    # Urls modelo RelacionMID
    url(r'^influenciasMID/(\d+)/$', login_required(ListaInfluenciasMID.as_view()), name='influenciasMID'),
    url(r'^nueva_influencia/(?P<actorY>\d+)/(?P<actorX>\d+)/$', login_required(CrearInfluenciaMID.as_view()),
        name='nueva_mid_matriz'),
    url(r'^consultar_mid/(?P<pk>\d+)/(?P<tipoAcceso>\w+)/$', login_required(ConsultarInfluenciaMID.as_view()),
        name='consultar_mid'),
    url(r'^editar_mid/(?P<pk>\d+)/(?P<tipoAcceso>\w+)/$', login_required(EditarInfluenciaMID.as_view()),
        name='editar_mid'),
    url(r'^matriz_mid/(?P<idEstudio>\d+)/$', login_required(generar_matriz_mid), name='matriz_mid'),
    url(r'^matriz_midi/(?P<idEstudio>\d+)/$', login_required(generar_matriz_midi), name='matriz_midi'),
    url(r'^matriz_maxima/(?P<idEstudio>\d+)/$', login_required(generar_matriz_maxima), name='matriz_maxima'),
    url(r'^matriz_ri/(?P<idEstudio>\d+)/$', login_required(generar_matriz_ri), name='matriz_ri'),
    url(r'^matriz_balance/(?P<idEstudio>\d+)/$', login_required(generar_matriz_balance), name='matriz_balance'),
    url(r'^estabilidad/(?P<idEstudio>\d+)/$', login_required(generar_indicador_estabilidad), name='estabilidad'),

    # Urls modelo RelacionMAO
    url(r'^relacionesMAO/(\d+)/$', login_required(ListaRelacionesMAO.as_view()), name='relacionesMAO'),
    url(r'^nueva_MAO/(?P<actor>\d+)/(?P<objetivo>\d+)/$', login_required(CrearRelacionMAO.as_view()),
        name='nueva_MAO'),
    url(r'^consultar_mao/(?P<pk>\d+)/(?P<tipoAcceso>\w+)/$', login_required(ConsultarRelacionMAO.as_view()),
        name='consultar_mao'),
    url(r'^editar_mao/(?P<pk>\d+)/(?P<tipoAcceso>\w+)/$', login_required(EditarRelacionMAO.as_view()),
        name='editar_mao'),
    url(r'^matriz_mao/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/', login_required(generar_matriz_mao),
        name='matriz_mao'),
    url(r'^matriz_caa_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(generar_matrices_caa_daa),
        name='caa_daa'),
    url(r'^lista_descendientes/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(generar_lista_descendiente),
        name='descendientes'),

    # Urls modelo informe final
    url(r'^editar_informe/(?P<pk>\d+)/$', login_required(EditarInformeFinal.as_view()), name='editar_informe'),

    # Urls consultas ajax
    url(r'ficha-ajax/$', login_required(consultar_actores_faltantes)), # obtiene lista actores X registrados en la ficha

    # Urls consensos
    url(r'^consenso_mid/(?P<idEstudio>\d+)/(?P<matriz>\d)', login_required(activar_consenso_mid), name='consenso_mid'),
    url(r'^consenso_mao/(?P<idEstudio>\d+)/(?P<matriz>\d)/(?P<tipo>\d)', login_required(activar_consenso_mao),
        name='consenso_mao'),
    url(r'^consenso_caa_daa/(?P<idEstudio>\d+)/(?P<matriz>\d)/(?P<tipo>\d)', login_required(activar_consenso_caa_daa),
        name='consenso_caa_daa'),

    # Urls histogramas mid
    url(r'^histograma_mid/(?P<idEstudio>\d+)/$', login_required(histograma_mid), name='histograma_mid'),
    url(r'datos_histograma_mid', login_required(datos_histograma_mid)),
    url(r'^histograma_ri/(?P<idEstudio>\d+)/$', login_required(histograma_ri), name='histograma_ri'),
    url(r'datos_histograma_ri', login_required(datos_histograma_ri)),

    # Urls histogramas mao
    url(r'^histograma_implicacion/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(histograma_implicacion),
        name='implicacion'),
    url(r'^histograma_movilizacion/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(histograma_movilizacion),
        name='movilizacion'),
    url(r'datos_histograma', login_required(datos_histogramas_mao)),

    # Urls mapa actores
    url(r'^mapa_actores/(?P<idEstudio>\d+)/$', login_required(generar_mapa_midi), name='mapa_actores'),
    url(r'datos_plano_midi', login_required(datos_mapa_midi)),

    # Urls graficos caa y daa
    url(r'^mapa_caa_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(generar_mapa_caa_daa),
        name='mapa_caa_daa'),
    url(r'datos_mapa_caa_daa', login_required(datos_mapa_caa_daa)),
    url(r'^histograma_caa_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(histograma_caa_daa),
        name='hist_caa_daa'),
    url(r'datos_caa_daa', login_required(datos_histograma_caa_daa)),
    url(r'^grafo_caa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)$', login_required(generar_grafo_caa), name='grafo_caa'),
    url(r'datos_grafo_caa', login_required(datos_grafo_caa)),
    url(r'^grafo_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)$', login_required(generar_grafo_daa), name='grafo_daa'),
    url(r'datos_grafo_daa', login_required(datos_grafo_daa)),

    # Urls exportar a excel
    url(r'exportar_estudios/xls/(?P<idEstudio>\d+)/$', login_required(exportar_estudio_xls), name='exportar_excel'),

]
