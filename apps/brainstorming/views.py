from ..proyecto.views import obtener_tipo_usuario_estudio, contexto_mensajes
from .models import *
from .forms import *
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json
from django.http import JsonResponse, HttpResponse, request, Http404
import xlwt


class CrearEstudio(CreateView):

    model = EstudioLluviaDeIdeas
    form_class = FormEstudio
    template_name = 'brainstorming/estudio/crear_estudio_lluvia_ideas.html'

    def get_context_data(self, **kwargs):
        context = super(CrearEstudio, self).get_context_data(**kwargs)
        tipoTecnica = Tecnica.objects.get(codigo=4)
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        context['proyecto'] = proyecto
        context['tecnica'] = tipoTecnica.id
        return context

    def form_valid(self, form):
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        form.instance.idAdministrador = proyecto.idAdministrador
        messages.add_message(self.request, messages.SUCCESS, 'Estudio Lluvia de ideas registrado con exito.')
        return super(CrearEstudio, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearEstudio, self).form_invalid(form)

        titulo = form.cleaned_data["titulo"]
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        estudios_registrados = EstudioLluviaDeIdeas.objects.filter(idProyecto=proyecto.id).order_by('titulo')

        if estudios_registrados.filter(titulo=titulo).count() > 0:
            messages.error(self.request, 'Ya existe un estudio Lluvia de ideas registrado con el nombre ' + titulo)
        else:
            messages.error(self.request, 'El estudio no pudo ser registrado. Verifique los datos ingresados.')
        return response


class ConsultarEstudio(DetailView):

    model = EstudioLluviaDeIdeas
    template_name = 'brainstorming/estudio/consultar_estudio.html'
    context_object_name = 'estudio'

    def get_context_data(self, **kwargs):
        context = super(ConsultarEstudio, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioLluviaDeIdeas, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 4)
        context['ideas'] = Idea.objects.filter(idEstudio=estudio.id, estado=True).count()
        context['reglas'] = Regla.objects.filter(idEstudio=estudio.id, estado=True).count()

        valoraciones = 0
        """
        if context['usuario'] == 'EXPERTO':
            valoraciones = str(calcular_porcentaje_valoraciones(self.request, estudio.id)) + '%'
        elif self.request.user in estudio.idCoordinadores.all():
            valoraciones = ValoracionIdea.objects.filter(idIdea__idEstudio=estudio.id, estado=True).count()
        """

        context['valoraciones'] = valoraciones

        # control de mensajes
        context.update(contexto_mensajes(self.request))

        return context


class EditarEstudio(UpdateView):

    model = EstudioLluviaDeIdeas
    form_class = FormEstudio
    template_name = 'brainstorming/estudio/editar_estudio.html'
    context_object_name = 'estudio'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Estudio Lluvia de Ideas actualizado con exito.')
        return super(EditarEstudio, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarEstudio, self).form_invalid(form)

        titulo = form.cleaned_data["titulo"]
        estudio = get_object_or_404(EstudioLluviaDeIdeas, id=self.kwargs['pk'])
        estudios_registrados = EstudioLluviaDeIdeas.objects.filter(idProyecto=estudio.idProyecto.id).order_by('titulo')
        estudios_registrados = estudios_registrados.exclude(id=estudio.id)

        if estudios_registrados.filter(titulo=titulo).count() > 0:
            messages.error(self.request, 'Ya existe un estudio Lluvia de Ideas registrado con el nombre ' + titulo)
        else:
            messages.error(self.request, 'El estudio no pudo ser actualizado. Verifique los datos ingresados.')
        return response


class EliminarEstudio(DeleteView):

    model = EstudioLluviaDeIdeas
    template_name = 'brainstorming/estudio/eliminar_estudio.html'
    context_object_name = 'estudio'
    success_message = "Estudio Lluvia de ideas eliminado con exito."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarEstudio, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        estudio = get_object_or_404(EstudioLluviaDeIdeas, id=self.kwargs['pk'])
        return reverse('proyecto:ver_estudios_proyecto', args={estudio.idProyecto.id})


"""-------------------------------------------VIEWS MODELO IDEA---------------------------------------"""


class ListaIdeas(ListView):

    model = Idea
    template_name = 'brainstorming/idea/lista_ideas.html'
    context_object_name = 'ideas'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioLluviaDeIdeas, id=self.kwargs['pk'])
        return Idea.objects.filter(idEstudio_id=estudio.id).order_by('-estado', 'titulo')

    def get_context_data(self, **kwargs):
        context = super(ListaIdeas, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioLluviaDeIdeas, id=self.kwargs['pk'])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 4)
        context['valoraciones'] = ValoracionIdea.objects.filter(idIdea__idEstudio=estudio.id).count()

        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


"""
class CrearIdea(CreateView):

    model = Idea
    form_class = FormIdea
    template_name = 'abaco/idea/crear_idea.html'

    def get_context_data(self, **kwargs):
        context = super(CrearIdea, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.args[0])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        # context['banco_actores'] = obtener_actores_en_plataforma(self.request, estudio)
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Idea registrada con exito.')
        return super(CrearIdea, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearIdea, self).form_invalid(form)

        titulo = form.cleaned_data["titulo"]
        estudio = get_object_or_404(EstudioAbaco, id=self.args[0])
        ideas_registradas = Idea.objects.filter(idEstudio=estudio.id).order_by('titulo')
        if ideas_registradas.filter(titulo=titulo).count() > 0:
            messages.error(self.request, 'Ya existe una idea registrada con este título')
        else:
            messages.error(self.request, 'La idea no pudo ser registrado. Verifique los datos ingresados.')
        return response


class ConsultarIdea(DetailView):

    model = Idea
    template_name = 'abaco/idea/consultar_idea.html'
    context_object_name = 'idea'

    def get_context_data(self, **kwargs):
        context = super(ConsultarIdea, self).get_context_data(**kwargs)
        idea = get_object_or_404(Idea, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, idea.idEstudio.id, 3)

        if context['usuario'] != 'EXPERTO':
            context['valoraciones'] = ValoracionIdea.objects.filter(idIdea_id=idea.id, estado=True)
        else:
            context['valoraciones'] = ValoracionIdea.objects.filter(idIdea_id=idea.id,
                                                                    idExperto_id=self.request.user.id)\
                                                                    .order_by('-estado', '-fechaHora')

        return context


class EditarIdea(UpdateView):

    model = Idea
    form_class = FormIdea
    template_name = 'abaco/idea/editar_idea.html'
    context_object_name = 'idea'

    def get_context_data(self, **kwargs):
        context = super(EditarIdea, self).get_context_data(**kwargs)
        idea = get_object_or_404(Idea, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, idea.idEstudio.id, 3)
        context['valoracionesIdea'] = ValoracionIdea.objects.filter(idIdea=idea.id).count()
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Idea actualizada con exito.')
        return super(EditarIdea, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarIdea, self).form_invalid(form)
        messages.error(self.request, 'La idea no pudo ser actualizada. Verifique los datos ingresados')
        return response


class EliminarIdea(DeleteView):

    model = Idea
    template_name = 'abaco/idea/eliminar_idea.html'
    context_object_name = 'idea'
    success_message = "Idea eliminada con exito."

    def get_context_data(self, **kwargs):
        context = super(EliminarIdea, self).get_context_data(**kwargs)
        idea = get_object_or_404(Idea, id=self.kwargs['pk'])
        estudio = get_object_or_404(EstudioAbaco, id=idea.idEstudio.id)
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        context['valoracionesIdea'] = ValoracionIdea.objects.filter(idIdea=idea.id).count()
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarIdea, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        idea = get_object_or_404(Idea, id=self.kwargs['pk'])
        return reverse('abaco:ideas', kwargs={'pk': idea.idEstudio.id})
"""
