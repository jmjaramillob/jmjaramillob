from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.multipolv1.views import (
    CrearEstudio,
    delete_estudio,
    UpdateEstudio,
    CreateAccion,
    CreateCriterio,
    CreatePolitica,
    EditAccion,
    EditCriterio,
    EditPolitica,
    DeleteAccion,
    DeleteCriterio,
    DeletePolitica,
    ListAccion,
    ListCriterio,
    ListPolitica,
    evaluacion_accion_politica,
)
from apps.multipolv1.views import (
    DetalleEstudio,
    evaluacion_criterio_accion,
    evaluacion_criterio_politica,
)


app_name = "multipolv1"
urlpatterns = [
    # URL para operaciones con los estudios
    url(
        r"^detalle_estudio/(?P<pk>\d+)/$",
        login_required(DetalleEstudio.as_view()),
        name="detalle_estudio",
    ),
    url(
        r"^create_estudio/(?P<pk>\d+)/$",
        login_required(CrearEstudio.as_view()),
        name="crear_estudio",
    ),
    url(r"^delete_estudio/$", login_required(delete_estudio), name="eliminar_estudio"),
    url(
        r"^edit_estudio/(?P<pk>\d+)/$",
        login_required(UpdateEstudio.as_view()),
        name="editar_estudio",
    ),
    # URL para operaciones con las acciones
    url(
        r"^add_accion/(?P<pk>\d+)/$",
        login_required(CreateAccion.as_view()),
        name="add_accion",
    ),
    url(
        r"^edit_accion/(?P<pk>\d+)/$",
        login_required(EditAccion.as_view()),
        name="editar_accion",
    ),
    url(
        r"^delete_accion/(?P<pk>\d+)/$",
        login_required(DeleteAccion.as_view()),
        name="borrar_accion",
    ),
    url(
        r"^lista_accion/(?P<pk>\d+)/$",
        login_required(ListAccion.as_view()),
        name="lista_accion",
    ),
    # URL para operaciones con los criterios
    url(
        r"^add_criterio/(?P<pk>\d+)/$",
        login_required(CreateCriterio.as_view()),
        name="add_criterio",
    ),
    url(
        r"^edit_criterio/(?P<pk>\d+)/$",
        login_required(EditCriterio.as_view()),
        name="editar_criterio",
    ),
    url(
        r"^delete_criterio/(?P<pk>\d+)/$",
        login_required(DeleteCriterio.as_view()),
        name="borrar_criterio",
    ),
    url(
        r"^lista_criterio/(?P<pk>\d+)/$",
        login_required(ListCriterio.as_view()),
        name="lista_criterio",
    ),
    # URL para operaciones con las políticas
    url(
        r"^add_politica/(?P<pk>\d+)/$",
        login_required(CreatePolitica.as_view()),
        name="add_politica",
    ),
    url(
        r"^edit_politica/(?P<pk>\d+)/$",
        login_required(EditPolitica.as_view()),
        name="editar_politica",
    ),
    url(
        r"^delete_politica/(?P<pk>\d+)/$",
        login_required(DeletePolitica.as_view()),
        name="borrar_politica",
    ),
    url(
        r"^lista_politicas/(?P<pk>\d+)/$",
        login_required(ListPolitica.as_view()),
        name="lista_politica",
    ),
    #
    ## URL para operaciones con las evaluaciones
    url(
        r"^evaluacion_criterio_accion/(?P<pk>\d+)/$",
        login_required(evaluacion_criterio_accion),
        name="evaluacion_criterio_accion",
    ),
    url(
        r"^evaluacion_criterio_politica/(?P<pk>\d+)/$",
        login_required(evaluacion_criterio_politica),
        name="evaluacion_criterio_politica",
    ),
    # url(r'^evaluacion_accion_politica/(?P<pk>\d+)/$', login_required(views.evaluacion_accion_politica), name='evaluacion_accion_politica'),
    #
    ## URL para la gestion de matrices
    url(
        r"^evaluacion_accion_politica/(?P<pk>\d+)/$",
        login_required(evaluacion_accion_politica),
        name="evaluacion_accion_politica",
    ),
    # url(r'^agregar_valoración/(?P<pk_accion>.+)/(?P<pk_criterio>.+)/$', views.agregar_evaluacion_criterio_accion, name='agregar_evaluación_CA')
]
