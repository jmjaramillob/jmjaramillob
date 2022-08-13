from ..proyecto.views import obtener_tipo_usuario_estudio, contexto_mensajes
from ..proyecto.models import Proyecto, Tecnica
from ..brainstorming.models import EstudioLluviaDeIdeas, Idea as IdeaBrainstorming
from .models import *
from .forms import *
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json
from django.http import JsonResponse, HttpResponse, request, Http404
from datetime import date, timedelta
import xlwt


class CrearEstudio(CreateView):

    model = EstudioAbaco
    form_class = FormEstudio
    template_name = 'abaco/estudio/crear_estudio_abaco.html'

    def get_context_data(self, **kwargs):
        context = super(CrearEstudio, self).get_context_data(**kwargs)
        tipoTecnica = Tecnica.objects.get(codigo=3)
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        context['proyecto'] = proyecto
        context['tecnica'] = tipoTecnica.id
        return context

    def form_valid(self, form):
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        form.instance.idAdministrador = proyecto.idAdministrador

        messages.add_message(self.request, messages.SUCCESS, 'Estudio Abaco de Regnier registrado con exito.')
        return super(CrearEstudio, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearEstudio, self).form_invalid(form)

        titulo = form.cleaned_data["titulo"]
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        estudios_registrados = EstudioAbaco.objects.filter(idProyecto=proyecto.id).order_by('titulo')

        if estudios_registrados.filter(titulo=titulo).count() > 0:
            messages.error(self.request, 'Ya existe un estudio Abaco de Regnier registrado con el nombre ' + titulo)
        else:
            messages.error(self.request, 'El estudio no pudo ser registrado. Verifique los datos ingresados.')
        return response


class ConsultarEstudio(DetailView):

    model = EstudioAbaco
    template_name = 'abaco/estudio/consultar_estudio_abaco.html'
    context_object_name = 'estudio'

    def get_context_data(self, **kwargs):
        context = super(ConsultarEstudio, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        context['ideas'] = Idea.objects.filter(idEstudio=estudio.id, estado=True).count()
        context['reglas'] = Regla.objects.filter(idEstudio=estudio.id, estado=True).count()
        context['sesiones'] = Sesion.objects.filter(idEstudio=estudio.id).order_by('id')

        valoraciones = 0
        if context['usuario'] == 'EXPERTO':
            valoraciones = str(calcular_porcentaje_valoraciones(self.request, estudio.id)) + '%'
        elif self.request.user in estudio.idCoordinadores.all():
            valoraciones = ValoracionIdea.objects.filter(idIdea__idEstudio=estudio.id, estado=True).count()

        context['valoraciones'] = valoraciones

        # control de mensajes
        context.update(contexto_mensajes(self.request))

        return context


class EditarEstudio(UpdateView):

    model = EstudioAbaco
    form_class = FormEstudio
    template_name = 'abaco/estudio/editar_estudio_abaco.html'
    context_object_name = 'estudio'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Estudio Abaco de Regnier actualizado con exito.')
        return super(EditarEstudio, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarEstudio, self).form_invalid(form)

        titulo = form.cleaned_data["titulo"]
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        estudios_registrados = EstudioAbaco.objects.filter(idProyecto=estudio.idProyecto.id).order_by('titulo')
        estudios_registrados = estudios_registrados.exclude(id=estudio.id)

        if estudios_registrados.filter(titulo=titulo).count() > 0:
            messages.error(self.request, 'Ya existe un estudio Abaco de Regnier registrado con el nombre ' + titulo)
        else:
            messages.error(self.request, 'El estudio no pudo ser actualizado. Verifique los datos ingresados.')
        return response


class EliminarEstudio(DeleteView):

    model = EstudioAbaco
    template_name = 'abaco/estudio/eliminar_estudio_abaco.html'
    context_object_name = 'estudio'
    success_message = "Estudio Abaco de Regnier eliminado con exito."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarEstudio, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        return reverse('proyecto:ver_estudios_proyecto', args={estudio.idProyecto.id})


"""-------------------------------------------VIEWS MODELO SESIONES---------------------------------------"""


class ListaSesiones(ListView):

    model = Sesion
    template_name = 'abaco/sesion/lista_sesiones.html'
    context_object_name = 'sesiones'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        sesiones = Sesion.objects.filter(idEstudio_id=estudio.id).order_by('-estado', '-numero_sesion')
        sesiones_abiertas = sesiones.filter(estado=True)
        if sesiones_abiertas.count() > 0:
            actualizar_sesiones(sesiones_abiertas)
        return sesiones

    def get_context_data(self, **kwargs):
        context = super(ListaSesiones, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        context['ultima_sesion'] = Sesion.objects.filter(idEstudio=estudio.id).order_by('id').last()
        context['hoy'] = date.today()

        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


class CrearSesion(CreateView):

    model = Sesion
    form_class = FormSesion
    template_name = 'abaco/sesion/nueva_sesion.html'

    def get_context_data(self, **kwargs):
        context = super(CrearSesion, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.args[0])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        sesiones = Sesion.objects.filter(idEstudio_id=estudio.id).order_by('id')
        if sesiones.count() > 0:
            ultima_sesion = sesiones.last()
            context['estado_ultima_sesion'] = ultima_sesion.estado
            context['numero'] = ultima_sesion.numero_sesion + 1
        else:
            context['estado_ultima_sesion'] = False
            context['numero'] = 1

        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Sesión registrada con exito.')
        return super(CrearSesion, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearSesion, self).form_invalid(form)
        messages.error(self.request, 'La sesión no pudo ser registrada. Verifique los datos ingresados.')
        return response


class ConsultarSesion(DetailView):

    model = Sesion
    template_name = 'abaco/sesion/consultar_sesion.html'
    context_object_name = 'sesion'

    def get_context_data(self, **kwargs):
        context = super(ConsultarSesion, self).get_context_data(**kwargs)
        sesion = get_object_or_404(Sesion, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, sesion.idEstudio.id, 3)
        return context


class EditarSesion(UpdateView):

    model = Sesion
    form_class = FormSesion
    template_name = 'abaco/sesion/editar_sesion.html'
    context_object_name = 'sesion'

    def get_context_data(self, **kwargs):
        context = super(EditarSesion, self).get_context_data(**kwargs)
        sesion = get_object_or_404(Sesion, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, sesion.idEstudio_id, 3)
        context['ultima_sesion'] = Sesion.objects.filter(idEstudio=sesion.idEstudio_id).last()
        context['hoy'] = date.today()
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Sesión actualizada con exito.')
        return super(EditarSesion, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarSesion, self).form_invalid(form)
        messages.error(self.request, 'La sesión no pudo ser actualizada. Verifique los datos ingresados')
        return response


"""-------------------------------------------VIEWS MODELO IDEA---------------------------------------"""


class ListaIdeas(ListView):

    model = Idea
    template_name = 'abaco/idea/lista_ideas.html'
    context_object_name = 'ideas'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        sesiones_abiertas = Sesion.objects.filter(idEstudio_id=estudio.id, estado=True)
        if sesiones_abiertas.count() > 0:
            actualizar_sesiones(sesiones_abiertas)
        return Idea.objects.filter(idEstudio_id=estudio.id).order_by('-estado', 'titulo')

    def get_context_data(self, **kwargs):
        context = super(ListaIdeas, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        context['ultima_sesion'] = Sesion.objects.filter(idEstudio=estudio.id).last()

        todas_ideas = Idea.objects.filter(idEstudio_id=estudio.id).order_by('titulo')
        context['ideas_evaluacion'] = todas_ideas.filter(estado=True)
        context['mis_ideas'] = todas_ideas.filter(idCreador_id=self.request.user.id)
        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


class CrearIdea(CreateView):

    model = Idea
    form_class = FormIdea
    template_name = 'abaco/idea/crear_idea.html'

    def get_context_data(self, **kwargs):
        context = super(CrearIdea, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.args[0])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        context['ultima_sesion'] = Sesion.objects.filter(idEstudio=estudio.id).last()
        if context['usuario'] != 'EXPERTO':
            banco = banco_estudios(self.request)
            context['banco_estudios_abaco'] = banco['abaco']
            context['banco_estudios_brain'] = banco['brainstorming']
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
            messages.error(self.request, 'La idea no pudo ser registrada. Verifique los datos ingresados.')
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
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, idea.idEstudio_id, 3)
        context['valoracionesIdea'] = ValoracionIdea.objects.filter(idIdea=idea.id).count()
        context['ultima_sesion'] = Sesion.objects.filter(idEstudio=idea.idEstudio_id).last()
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
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, idea.idEstudio_id, 3)
        context['valoracionesIdea'] = ValoracionIdea.objects.filter(idIdea=idea.id).count()
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarIdea, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        idea = get_object_or_404(Idea, id=self.kwargs['pk'])
        return reverse('abaco:ideas', kwargs={'pk': idea.idEstudio.id})


"""-------------------------------------------VIEWS MODELO REGLA---------------------------------------"""


class ListaReglas(ListView):

    model = Regla
    template_name = 'abaco/regla/lista_reglas.html'
    context_object_name = 'reglas'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        sesiones_abiertas = Sesion.objects.filter(idEstudio_id=estudio.id, estado=True)
        if sesiones_abiertas.count() > 0:
            actualizar_sesiones(sesiones_abiertas)
        reglas = Regla.objects.filter(idEstudio=estudio.id).order_by('titulo')
        return reglas

    def get_context_data(self, **kwargs):
        context = super(ListaReglas, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


class CrearRegla(CreateView):

    model = Regla
    form_class = FormRegla
    template_name = 'abaco/regla/crear_regla.html'

    def get_context_data(self, **kwargs):
        context = super(CrearRegla, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.args[0])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        # context['banco_actores'] = obtener_actores_en_plataforma(self.request, estudio)
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Regla registrada con exito.')
        return super(CrearRegla, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearRegla, self).form_invalid(form)

        titulo = form.cleaned_data["titulo"]
        estudio = get_object_or_404(EstudioAbaco, id=self.args[0])
        reglas_registradas = Regla.objects.filter(idEstudio=estudio.id).order_by('titulo')
        if reglas_registradas.filter(titulo=titulo).count() > 0:
            messages.error(self.request, 'Ya existe una regla registrada con este título')
        else:
            messages.error(self.request, 'La regla no pudo ser registrada. Verifique los datos ingresados.')
        return response


class ConsultarRegla(DetailView):

    model = Regla
    template_name = 'abaco/regla/consultar_regla.html'
    context_object_name = 'regla'

    def get_context_data(self, **kwargs):
        context = super(ConsultarRegla, self).get_context_data(**kwargs)
        regla = get_object_or_404(Regla, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, regla.idEstudio.id, 3)
        return context


class EditarRegla(UpdateView):

    model = Regla
    form_class = FormRegla
    template_name = 'abaco/regla/editar_regla.html'
    context_object_name = 'regla'

    def get_context_data(self, **kwargs):
        context = super(EditarRegla, self).get_context_data(**kwargs)
        regla = get_object_or_404(Regla, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, regla.idEstudio.id, 3)
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Regla actualizada con exito.')
        return super(EditarRegla, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarRegla, self).form_invalid(form)
        messages.error(self.request, 'La regla no pudo ser actualizada. Verifique los datos ingresados')
        return response


class EliminarRegla(DeleteView):

    model = Regla
    template_name = 'abaco/regla/eliminar_regla.html'
    context_object_name = 'regla'
    success_message = "Regla eliminada con exito."

    def get_context_data(self, **kwargs):
        context = super(EliminarRegla, self).get_context_data(**kwargs)
        regla = get_object_or_404(Regla, id=self.kwargs['pk'])
        estudio = get_object_or_404(EstudioAbaco, id=regla.idEstudio.id)
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarRegla, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        regla = get_object_or_404(Regla, id=self.kwargs['pk'])
        return reverse('abaco:reglas', kwargs={'pk': regla.idEstudio.id})


"""-------------------------------------------VIEWS MODELO VALORACION DE LAS IDEAS---------------------------------"""


class ListaValoraciones(ListView):

    model = ValoracionIdea
    template_name = 'abaco/valoracion/lista_valoraciones.html'
    context_object_name = 'valoraciones'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])

        sesiones_abiertas = Sesion.objects.filter(idEstudio_id=estudio.id, estado=True)
        if sesiones_abiertas.count() > 0:
            actualizar_sesiones(sesiones_abiertas)

        valoraciones = []
        usuario = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)

        if usuario == 'EXPERTO':
            valoraciones = ValoracionIdea.objects.filter(idIdea__idEstudio=estudio.id, estado=True,
                                                         idExperto_id=self.request.user.id).order_by('idIdea__titulo')
        elif self.request.user in estudio.idCoordinadores.all():
            valoraciones = ValoracionIdea.objects.filter(idIdea__idEstudio=estudio.id, estado=True,).order_by('idIdea__titulo')

        return valoraciones

    def get_context_data(self, **kwargs):
        context = super(ListaValoraciones, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        context['ideas'] = Idea.objects.filter(idEstudio_id=estudio.id, estado=True).count()
        context['ultima_sesion'] = Sesion.objects.filter(idEstudio=estudio.id).last()

        if self.request.user in estudio.idExpertos.all():
            context['mis_valoraciones'] = ValoracionIdea.objects.filter(idIdea__idEstudio=estudio.id,
                                                                        estado=True,
                                                                        idExperto_id=self.request.user.id).order_by(
                'idIdea__titulo')
            context['porcentaje'] = calcular_porcentaje_valoraciones(self.request, estudio.id)

        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


class CrearValoracion(CreateView):

    model = ValoracionIdea
    form_class = FormValoracion
    template_name = 'abaco/valoracion/crear_valoracion.html'

    def get_context_data(self, **kwargs):
        context = super(CrearValoracion, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['idEstudio'])

        valoracion = int(self.kwargs['idValoracion'])
        if valoracion > 0:
            valoracion = get_object_or_404(ValoracionIdea, id=valoracion)

        context['valoracion'] = valoracion
        context['estudio'] = estudio
        context['escala'] = OpcionEscala.objects.filter(idEscala_id=estudio.idEscala_id).order_by('id')
        context['reglas'] = Regla.objects.filter(idEstudio_id=estudio.id, estado=True).order_by('titulo')
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)
        context['porcentaje'] = calcular_porcentaje_valoraciones(self.request, estudio.id)
        context['valoraciones_registradas'] = ValoracionIdea.objects.filter(idIdea__idEstudio=estudio.id, estado=True,
                                                                            idExperto_id=self.request.user.id)
        # filtrando ideas ya evaluadas
        ideas = Idea.objects.filter(idEstudio_id=estudio.id, estado=True).order_by('titulo')
        for v in context['valoraciones_registradas']:
            aux = ideas.exclude(id=v.idIdea.id)
            ideas = aux
        context['ideas'] = ideas

        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Valoracion registrada con exito.')

        valoracion = int(self.kwargs['idValoracion'])
        if valoracion > 0:
            valoracion = get_object_or_404(ValoracionIdea, id=valoracion)
            valoracion.estado = False
            valoracion.save()

        return super(CrearValoracion, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearValoracion, self).form_invalid(form)
        messages.error(self.request, 'La valoracion no pudo ser registrada. Verifique los datos ingresados.')
        return response

    def get_success_url(self):
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['idEstudio'])

        valoracion = int(self.kwargs['idValoracion'])
        if valoracion > 0:
            return reverse('abaco:valoraciones', kwargs={'pk': estudio.id})
        else:
            return reverse('abaco:nueva_valoracion', kwargs={'idEstudio': estudio.id, 'idValoracion': 0})


class ConsultarValoracion(DetailView):

    model = ValoracionIdea
    template_name = 'abaco/valoracion/consultar_valoracion.html'
    context_object_name = 'valoracion'

    def get_context_data(self, **kwargs):
        context = super(ConsultarValoracion, self).get_context_data(**kwargs)
        valoracion = get_object_or_404(ValoracionIdea, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, valoracion.idIdea.idEstudio_id, 3)

        if context['usuario'] != 'EXPERTO':
            context['otras_valoraciones'] = ValoracionIdea.objects.filter(idIdea_id=valoracion.idIdea_id, estado=True)\
                .exclude(id=valoracion.id)

            context['cambios'] = ValoracionIdea.objects.filter(idIdea_id=valoracion.idIdea_id,
                                                               idExperto_id=valoracion.idExperto.id,
                                                               estado=False).order_by('-fechaHora')
        else:
            context['cambios'] = ValoracionIdea.objects.filter(idIdea_id=valoracion.idIdea_id,
                                                               idExperto_id=self.request.user.id,
                                                               estado=False).order_by('-fechaHora')

        context['tipoAcceso'] = self.kwargs['tipoAcceso']

        return context


class Resultados(TemplateView):

    template_name = 'abaco/valoracion/resultados.html'

    def get_context_data(self, **kwargs):
        context = super(Resultados, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioAbaco, id=self.kwargs['pk'])
        context['estudio'] = estudio
        context['escala'] = OpcionEscala.objects.filter(idEscala_id=estudio.idEscala_id)
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 3)

        resultados = crear_matriz_resultados(estudio)
        if len(resultados['matriz']) > 0:
            context['matriz'] = resultados['matriz']
        context['lista'] = resultados['lista']
        context['totales'] = resultados['totales']
        context['expertos'] = resultados['expertos']

        return context


# Genera el grafico de barras que muestra los totales alcanzados por cada idea

def grafico_totales_ideas(request, idIdea):

    idea = get_object_or_404(Idea, id=int(idIdea))
    usuario = obtener_tipo_usuario_estudio(request, idea.idEstudio.id, 3)

    contexto = {'idea': idea, 'usuario': usuario}

    return render(request, 'abaco/valoracion/graficos/grafico_barras_totales_ideas.html', contexto)


# Devuelve los datos a representar en el grafico de los totales
def datos_grafico_totales_ideas(request):

    if request.is_ajax():
        idea = get_object_or_404(Idea, id=int(request.GET['idea']))
        ideas_evaluadas = Idea.objects.filter(idEstudio_id=idea.idEstudio.id, estado=True).count()
        escala = OpcionEscala.objects.filter(idEscala_id=idea.idEstudio.idEscala_id).order_by('id')
        valoraciones_registradas = ValoracionIdea.objects.filter(idIdea__idEstudio_id=idea.idEstudio.id,
                                                                 estado=True,
                                                                 idIdea__estado=True).order_by('idExperto__id')

        lista_opciones = []
        lista_valores = []

        for experto in idea.idEstudio.idExpertos.all():
            valoraciones_experto = valoraciones_registradas.filter(idExperto_id=experto.id)
            if valoraciones_experto.count() != ideas_evaluadas:
                valoraciones_registradas = valoraciones_registradas.exclude(idExperto_id=experto.id)

        valoraciones_idea = valoraciones_registradas.filter(idIdea_id=idea.id)

        if len(valoraciones_idea) > 0:
            for opcion in escala:
                lista_opciones.append(opcion.nombre)
                lista_valores.append(valoraciones_idea.filter(valoracion__nombre=opcion.nombre).count())

        data = {'labels': lista_opciones, 'valores': lista_valores}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


def crear_matriz_resultados(estudio):

    # Clase auxiliar para la generacion de la matriz
    class Celda:
        def __init__(self, tipo, objeto=""):
            self.tipo = tipo
            self.objeto = objeto

    expertos_estudio = estudio.idExpertos.all()
    ideas_evaluadas = Idea.objects.filter(idEstudio_id=estudio.id, estado=True).order_by('titulo')
    valoraciones_registradas = ValoracionIdea.objects.filter(idIdea__idEstudio_id=estudio.id,
                                                             estado=True, idIdea__estado=True).order_by('idExperto__id')

    encabezado = []
    # excluyo las valorizaciones de los expertos que no han finalizado
    contador = 0
    for experto in expertos_estudio:
        valoraciones_experto = valoraciones_registradas.filter(idExperto_id=experto.id)
        if valoraciones_experto.count() != ideas_evaluadas.count():
            valoraciones_registradas = valoraciones_registradas.exclude(idExperto_id=experto.id)
        else:
            contador += 1
            encabezado.append(Celda(tipo="ENCABEZADO", objeto="EXP."+str(contador)))

    escala = OpcionEscala.objects.filter(idEscala_id=estudio.idEscala_id)
    matriz = []
    lista_totales = []

    if len(valoraciones_registradas) > 0:
        matriz.append(encabezado)
        for idea in ideas_evaluadas:
            valoraciones_idea = valoraciones_registradas.filter(idIdea_id=idea.id)

            fila = [Celda(tipo="IDEA", objeto=idea)]
            for valoracion in valoraciones_idea:
                fila.append(Celda(tipo="VALORACION", objeto=valoracion))

            # creacion de fila de la lista de totales
            fila_totales = [idea]
            for opcion in escala:
                fila_totales.append(valoraciones_idea.filter(valoracion__nombre=opcion.nombre).count())

            lista_totales.append(fila_totales)

            matriz.append(fila)

    resultados = {'matriz': matriz, 'lista': valoraciones_registradas.order_by('idIdea__titulo'),
                  'totales': lista_totales, 'expertos': contador}

    return resultados


def calcular_porcentaje_valoraciones(request, idEstudio):

    ideas = Idea.objects.filter(idEstudio_id=idEstudio, estado=True).count()
    valoracionesExperto = ValoracionIdea.objects.filter(idIdea__idEstudio=idEstudio, estado=True,
                                                        idExperto_id=request.user.id, idIdea__estado=True).count()
    return round((100 / ideas) * valoracionesExperto, 2)


# Actualiza el estado de las sesiones
def actualizar_sesiones(sesiones_abiertas):

    ultima_sesion = sesiones_abiertas.order_by('id').last()

    for sesion in sesiones_abiertas:
        # si la sesion ha alcanzo la fecha limite o el estudio se cierra
        if date.today() > sesion.fecha_final or ultima_sesion.idEstudio.estado is False:
            sesion.estado = False
            sesion.save()
        # si la sesion esta abierta pero no corresponde a la ultima registrada
        if sesion.id != ultima_sesion.id:
            sesion.fecha_final = date.today() - timedelta(days=1)
            sesion.estado = False
            sesion.save()


"""EXPORTAR A EXCEL"""


# Exporta a excel los datos del estudio
def exportar_estudio_xls(request, idEstudio):

    estudio = get_object_or_404(EstudioAbaco, id=int(idEstudio))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+estudio.titulo+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    hoja_ideas = wb.add_sheet('Ideas')
    hoja_reglas = wb.add_sheet('Reglas')
    hoja_valoraciones = wb.add_sheet('Valoraciones')
    hoja_resultados = wb.add_sheet('Resultados')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns1 = ['Título', 'Descripción', 'Estado']
    columns2 = ['Título', 'Descripción', 'Estado']
    columns3 = ['Idea', 'Valoracion', 'Justificación']
    columns4 = ['Idea']

    opciones_escala = OpcionEscala.objects.filter(idEscala_id=estudio.idEscala_id).order_by('id')

    for opcion in opciones_escala:
        columns4.append(opcion.nombre)

    for col_num in range(len(columns1)):
        hoja_ideas.write(row_num, col_num, columns1[col_num], font_style)

    for col_num in range(len(columns2)):
        hoja_reglas.write(row_num, col_num, columns2[col_num], font_style)

    for col_num in range(len(columns3)):
        hoja_valoraciones.write(row_num, col_num, columns3[col_num], font_style)

    for col_num in range(len(columns4)):
        hoja_resultados.write(row_num, col_num, columns4[col_num], font_style)

    font_style = xlwt.XFStyle()
    filas = obtener_datos_estudio(request, estudio)

    for row in filas['ideas']:
        row_num += 1
        for col_num in range(len(row)):
            hoja_ideas.write(row_num, col_num, row[col_num], font_style)

    row_num = 0
    for row in filas['reglas']:
        row_num += 1
        for col_num in range(len(row)):
            hoja_reglas.write(row_num, col_num, row[col_num], font_style)

    row_num = 0
    for row in filas['valoraciones']:
        row_num += 1
        hoja_valoraciones.write(row_num, 0, row['idea'], font_style)
        hoja_valoraciones.write(row_num, 1, row['valoracion'], font_style)
        hoja_valoraciones.write(row_num, 2, row['justificacion'], font_style)

    resultados = crear_matriz_resultados(estudio)['totales']

    row_num = 0
    for row in resultados:
        row_num += 1
        hoja_resultados.write(row_num, 0, row[0].titulo, font_style)
        hoja_resultados.write(row_num, 1, row[1], font_style)
        hoja_resultados.write(row_num, 2, row[2], font_style)
        hoja_resultados.write(row_num, 3, row[3], font_style)
        hoja_resultados.write(row_num, 4, row[4], font_style)
        hoja_resultados.write(row_num, 5, row[5], font_style)
        hoja_resultados.write(row_num, 6, row[6], font_style)
        hoja_resultados.write(row_num, 7, row[7], font_style)

    wb.save(response)
    return response


# Devuelve los datos a exportar a excel
def obtener_datos_estudio(request, estudio):

    usuario = obtener_tipo_usuario_estudio(request, estudio.id, 3)

    filas_ideas = Idea.objects.filter(idEstudio_id=estudio.id).values_list('titulo', 'descripcion',
                                                                           'estado').order_by('-estado', 'titulo')

    filas_reglas = Regla.objects.filter(idEstudio_id=estudio.id).values_list('titulo', 'descripcion',
                                                                             'estado').order_by('titulo')

    if usuario != 'EXPERTO':
        valoraciones = ValoracionIdea.objects.filter(idIdea__idEstudio_id=estudio.id, estado=True)\
            .order_by('idExperto', 'idIdea__titulo')

    else:
        valoraciones = ValoracionIdea.objects.\
            filter(idIdea__idEstudio_id=estudio.id, idExperto=request.user.id, estado=True).order_by('idIdea__titulo')

    filas_valoraciones = []

    for v in valoraciones:
        filas_valoraciones.append({'idea': v.idIdea.titulo, 'valoracion': v.valoracion.nombre,
                                   'justificacion': v.justificacion})

    filas = {'ideas': filas_ideas, 'reglas': filas_reglas, 'valoraciones': filas_valoraciones}

    return filas


# para cambiar el estado de una idea, regla o sesion (solo si la sesion esta abierta)
def cambiar_estado(request):

    if request.is_ajax():
        tipo = request.GET.get('tipo')
        error = True

        if tipo == 'idea':
            idea = get_object_or_404(Idea, id=int(request.GET.get('id')))
            idea.estado = not idea.estado

            try:
                idea.save()
                error = False
            except:
                print("No fue posible actualizar el estado de la idea")

        elif tipo == 'regla':
            regla = get_object_or_404(Regla, id=int(request.GET.get('id')))
            regla.estado = not regla.estado

            try:
                regla.save()
                error = False
            except:
                print("No fue posible actualizar el estado de la regla")

        elif tipo == 'sesion':

            sesion = get_object_or_404(Sesion, id=int(request.GET.get('id')))
            sesion.estado = not sesion.estado

            try:
                sesion.save()
                error = False
            except:
                print("No fue posible actualizar el estado de la sesión")

        response = JsonResponse({'error': error})
        return HttpResponse(response.content)
    else:
        return redirect('/')


"""----------------------FUNCIONES AUXILIARES IMPORTACION DE IDEAS----------------------------"""


# devuelve los estudios abaco y brainstorming donde el usuario es administrador o coordinador

def banco_estudios(request):

    usuario = User.objects.filter(id=request.user.id)
    abaco_admin = EstudioAbaco.objects.filter(idAdministrador__id=request.user.id)
    abaco_coordinador = EstudioAbaco.objects.filter(idCoordinadores__in=usuario)
    todos_abaco = abaco_admin | abaco_coordinador
    todos_abaco = todos_abaco.distinct()

    brain_admin = EstudioLluviaDeIdeas.objects.filter(idAdministrador__id=request.user.id)
    brain_coordinador = EstudioLluviaDeIdeas.objects.filter(idCoordinador__id=request.user.id)
    todos_brain = brain_admin | brain_coordinador
    todos_brain = todos_brain.distinct()

    todos_estudios = {'abaco': todos_abaco, 'brainstorming': todos_brain}
    return todos_estudios


# importa las ideas del estudio seleccionado (abaco de regnier o lluvia de ideas)

def importar_ideas(request):

    if request.is_ajax():
        error = True
        tipo = request.GET.get('id')[:5]
        id = int(request.GET.get('id')[5:])

        estudio = get_object_or_404(EstudioAbaco, id=int(request.GET.get('idEstudio')))
        ideas_estudio = Idea.objects.filter(idEstudio_id=estudio.id)

        estudioBanco = []
        ideasBanco = []
        if tipo == 'abaco':
            estudioBanco = get_object_or_404(EstudioAbaco, id=id)
            ideasBanco = Idea.objects.filter(idEstudio_id=estudioBanco.id)
        elif tipo == 'brain':
            estudioBanco = get_object_or_404(EstudioLluviaDeIdeas, id=id)
            ideasBanco = IdeaBrainstorming.objects.filter(idEstudio_id=estudioBanco.id)

        if len(ideasBanco) > 0:
            try:
                registrados = 0
                excluidos = 0
                # importacion de las ideas
                for idea in ideasBanco:
                        # se comprueba que no exista un idea con el mismo titulo ya registrada
                        comprobar_idea = ideas_estudio.filter(titulo=idea.titulo).count()
                        if comprobar_idea == 0:
                            a = Idea()
                            a.titulo = idea.titulo
                            a.descripcion = idea.descripcion
                            a.idCreador = request.user
                            a.estado = idea.estado
                            a.idEstudio = estudio
                            a.save()
                            registrados += 1
                            error = False
                        else:
                            excluidos += 1

                if registrados > 0:
                    messages.add_message(request,
                                         messages.SUCCESS,
                                         str(registrados) + ' ideas importadas con exito.' +
                                         str(excluidos) + ' ideas excluidas.')
                elif excluidos > 0:
                    messages.error(request,
                                   str(excluidos) + ' ideas fueron excluidas porque su título coincide con las ya' +
                                                    ' registradas.')
            except:
                print("No fue posible importar las ideas del estudio seleccionado.")
                messages.error(request, 'No fue posible importar las ideas del estudio seleccionado.')
        else:
            messages.error(request, 'El estudio seleccionado no cuenta con ideas registradas.')

        response = JsonResponse({'error': error})
        return HttpResponse(response.content)
    else:
        return redirect('/')






