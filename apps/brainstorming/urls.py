from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import CrearEstudio, ConsultarEstudio, EditarEstudio, EliminarEstudio, \
    ListaIdeas

"""
CrearIdea, ConsultarIdea, EditarIdea, EliminarIdea, \
ListaReglas, CrearRegla, ConsultarRegla, EditarRegla, EliminarRegla, \
"""

urlpatterns = [

    # Urls modelo Estudio Lluvia de ideas

    url(r'^agregar_estudio/(?P<pk>\d+)/$', login_required(CrearEstudio.as_view()), name='nuevo_estudio'),
    url(r'^consultar_estudio/(?P<pk>\d+)/$', login_required(ConsultarEstudio.as_view()), name='consultar_estudio'),
    url(r'^editar_estudio/(?P<pk>\d+)/$', login_required(EditarEstudio.as_view()), name='editar_estudio'),
    url(r'^eliminar_estudio/(?P<pk>\d+)/$', login_required(EliminarEstudio.as_view()), name='eliminar_estudio'),

    # Urls modelo Ideas

    url(r'^ideas/(?P<pk>\d+)/$', login_required(ListaIdeas.as_view()), name='ideas'),
    # url(r'^nueva_idea/(\d+)/$', login_required(CrearIdea.as_view()), name='nueva_idea'),
    # url(r'^consultar_idea/(?P<pk>\d+)/$', login_required(ConsultarIdea.as_view()), name='consultar_idea'),
    # url(r'^editar_idea/(?P<pk>\d+)/$', login_required(EditarIdea.as_view()), name='editar_idea'),
    # url(r'^eliminar_idea/(?P<pk>\d+)/$', login_required(EliminarIdea.as_view()), name='eliminar_idea'),
    
]
