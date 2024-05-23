from ..proyecto.models import Proyecto, Tecnica
from ..proyecto.views import contexto_mensajes, obtener_tipo_usuario_estudio
from .models import EstudioEntrevista, Pregunta, ValorEscalaLikert, RondaJuicio, Juicio, CoeficienteAlfa
from .forms import FormEstudioE, FormPregunta, FormValorEscala, FormRonda, FormJuicio
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, request
import statistics as stats
from datetime import date, timedelta
import json
import xlwt


"""------------------------------------VIEWS MODELO ESTUDIO ENTREVISTA-----------------------------------------"""


class CrearEstudio(CreateView):

    model = EstudioEntrevista
    form_class = FormEstudioE
    template_name = 'entrevista/estudio/crear_estudio_entrevista.html'

    def get_context_data(self, **kwargs):
        context = super(CrearEstudio, self).get_context_data(**kwargs)
        tipoTecnica = Tecnica.objects.get(codigo=2)
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        context['proyecto'] = proyecto
        context['tecnica'] = tipoTecnica.id
        context['hoy'] = date.today()
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Estudio Entrevista registrado.')
        return super(CrearEstudio, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearEstudio, self).form_invalid(form)

        titulo = form.cleaned_data["titulo"]
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        estudios_registrados = EstudioEntrevista.objects.filter(idProyecto=proyecto.id).order_by('titulo')

        if estudios_registrados.filter(titulo=titulo).count() > 0:
            messages.error(self.request, 'Ya existe un estudio Entrevista registrado con el nombre ' + titulo)
        else:
            messages.error(self.request, 'El estudio no pudo ser registrado. Verifique los datos ingresados.')
        return response


class EditarEstudio(UpdateView):

    model = EstudioEntrevista
    form_class = FormEstudioE
    template_name = 'entrevista/estudio/editar_estudio_entrevista.html'
    context_object_name = 'estudio'

    def get_context_data(self, **kwargs):
        context = super(EditarEstudio, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.kwargs['pk'])
        actualizar_rondas(estudio.id)
        rondas = RondaJuicio.objects.filter(idEstudio=estudio.id, estado=True)

        if rondas.count() > 0:
            context['ronda_abierta'] = rondas.last()
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Estudio Entrevista actualizado.')
        return super(EditarEstudio, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarEstudio, self).form_invalid(form)

        titulo = form.cleaned_data["titulo"]
        estudio = get_object_or_404(EstudioEntrevista, id=self.kwargs['pk'])
        estudios_registrados = EstudioEntrevista.objects.filter(idProyecto=estudio.idProyecto.id).order_by('titulo')
        estudios_registrados = estudios_registrados.exclude(id=estudio.id)

        if estudios_registrados.filter(titulo=titulo).count() > 0:
            messages.error(self.request, 'Ya existe un estudio Entrevista registrado con el nombre ' + titulo)
        else:
            messages.error(self.request, 'El estudio no pudo ser actualizado. Verifique los datos ingresados.')
        return response


class ConsultarEstudio(DetailView):

    model = EstudioEntrevista
    template_name = 'entrevista/estudio/consultar_estudio_entrevista.html'
    context_object_name = 'estudio'

    def get_context_data(self, **kwargs):
        context = super(ConsultarEstudio, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.kwargs['pk'])
        actualizar_rondas(estudio.id)
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        context['preguntas'] = Pregunta.objects.filter(idEstudio_id=estudio.id)
        context['escala'] = ValorEscalaLikert.objects.filter(idEstudio_id=estudio.id, estado=True)
        context['rondas'] = RondaJuicio.objects.filter(idEstudio_id=estudio.id).count()

        if context['rondas'] > 0:
            ultima_ronda_registrada = RondaJuicio.objects.filter(idEstudio_id=estudio.id).latest('numero_ronda')
            coeficientes = CoeficienteAlfa.objects.filter(idRonda__idEstudio_id=estudio.id).count()
            if coeficientes > 0:
                context['coeficiente_ultima_ronda'] = CoeficienteAlfa.objects.filter(idRonda__idEstudio_id=estudio.id).\
                    latest('id')
            if context['usuario'] == "EXPERTO":
                context['porcentaje'] = str(calcular_porcentaje_juicios(self, ultima_ronda_registrada)) + "%"
            else:
                context['cant_juicios'] = Juicio.objects.filter(idRonda=ultima_ronda_registrada.id).count()

        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


class EliminarEstudio(DeleteView):

    model = EstudioEntrevista
    template_name = 'entrevista/estudio/eliminar_estudio_entrevista.html'
    context_object_name = 'estudio'
    success_message = "Estudio Entrevista eliminado con exito."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarEstudio, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        estudio = get_object_or_404(EstudioEntrevista, id=self.kwargs['pk'])
        return reverse('proyecto:ver_estudios_proyecto', args={estudio.idProyecto.id})

"""------------------------------------VIEWS MODELO PREGUNTA-----------------------------------------------------"""


class ListaPreguntas(ListView):

    model = Pregunta
    template_name = 'entrevista/pregunta/lista_preguntas.html'
    context_object_name = 'preguntas'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        actualizar_rondas(estudio.id)
        return Pregunta.objects.filter(idEstudio=estudio.id).order_by('texto_pregunta')

    def get_context_data(self, **kwargs):
        context = super(ListaPreguntas, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        rondas_activas = RondaJuicio.objects.filter(idEstudio=estudio.id, estado=True).count()
        context['estudio'] = estudio
        context['rondas_activa'] = rondas_activas
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


class CrearPregunta(CreateView):

    model = Pregunta
    form_class = FormPregunta
    template_name = 'entrevista/pregunta/crear_pregunta.html'

    def get_context_data(self, **kwargs):
        context = super(CrearPregunta, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        context['rondas_activas'] = RondaJuicio.objects.filter(idEstudio=estudio.id, estado=True).count()
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Pregunta registrada con exito.')
        return super(CrearPregunta, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearPregunta, self).form_invalid(form)
        messages.error(self.request, 'La pregunta no pudo ser registrada. Ingrese datos válidos. Tenga en cuenta que la'
                                     ' pregunta a ingresar no debe estar registrada en el cuestionario del estudio.')
        return response


class EditarPregunta(UpdateView):

    model = Pregunta
    form_class = FormPregunta
    template_name = 'entrevista/pregunta/editar_pregunta.html'
    context_object_name = 'pregunta'

    def get_context_data(self, **kwargs):
        context = super(EditarPregunta, self).get_context_data(**kwargs)
        pregunta = get_object_or_404(Pregunta, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, pregunta.idEstudio.id, 2)
        context['rondas_activas'] = RondaJuicio.objects.filter(idEstudio=pregunta.idEstudio.id, estado=True).count()
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Pregunta actualizada con exito.')
        return super(EditarPregunta, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarPregunta, self).form_invalid(form)
        messages.error(self.request, 'La pregunta no pudo ser actualizada. Verifique los datos ingresados')
        return response


class ConsultarPregunta(DetailView):

    model = Pregunta
    template_name = 'entrevista/pregunta/consultar_pregunta.html'
    context_object_name = 'pregunta'

    def get_context_data(self, **kwargs):
        context = super(ConsultarPregunta, self).get_context_data(**kwargs)
        pregunta = get_object_or_404(Pregunta, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, pregunta.idEstudio.id, 2)
        context['juicios'] = Juicio.objects.filter(idRonda__idEstudio=pregunta.idEstudio.id,
                                                   texto_pregunta=pregunta.texto_pregunta)
        return context


class EliminarPregunta(DeleteView):

    model = Pregunta
    template_name = 'entrevista/pregunta/eliminar_pregunta.html'
    context_object_name = 'pregunta'
    success_message = "Pregunta eliminada del cuestionario."

    def get_context_data(self, **kwargs):
        context = super(EliminarPregunta, self).get_context_data(**kwargs)
        pregunta = get_object_or_404(Pregunta, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, pregunta.idEstudio.id, 2)
        context['rondas_activas'] = RondaJuicio.objects.filter(idEstudio=pregunta.idEstudio.id, estado=True).count()
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarPregunta, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        pregunta = get_object_or_404(Pregunta, id=self.kwargs['pk'])
        return reverse('entrevista:preguntas', args={pregunta.idEstudio.id})


"""------------------------------------VIEWS MODELO ESCALA DE LIKERT---------------------------------------------"""


class ListaValoresEscala(ListView):

    model = ValorEscalaLikert
    template_name = 'entrevista/escala/escala_likert.html'
    context_object_name = 'valoresLikert'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        actualizar_rondas(estudio.id)
        return ValorEscalaLikert.objects.filter(idEstudio=estudio.id).order_by('-estado', '-valor')

    def get_context_data(self, **kwargs):
        context = super(ListaValoresEscala, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        context['estudio'] = estudio
        context['ronda_activa'] = RondaJuicio.objects.filter(estado=True, idEstudio=estudio.id).count()
        context['juicios'] = Juicio.objects.filter(idRonda__idEstudio=estudio.id).count()
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


class CrearValorEscala(CreateView):

    model = ValorEscalaLikert
    form_class = FormValorEscala
    template_name = 'entrevista/escala/nuevo_valor_escala.html'

    def get_context_data(self, **kwargs):
        context = super(CrearValorEscala, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        valores_rango = [5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5]
        valores_registrados = ValorEscalaLikert.objects.filter(idEstudio=estudio.id, estado=True).order_by('-valor')

        # Se eliminan los puntajes que estan en la escala con estado= True (en uso).
        for i in valores_registrados:
            valores_rango.remove(i.valor)

        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        context['valores'] = valores_rango
        context['rondas_activas'] = RondaJuicio.objects.filter(idEstudio=estudio.id, estado=True).count()
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Alternativa de respuesta registrada en la escala.')
        return super(CrearValorEscala, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearValorEscala, self).form_invalid(form)
        messages.error(self.request, 'La alternativa de respuesta no pudo ser registrada. Ingrese datos válidos. Verifique'
                                     ' que la alternativa que desea registrar no exista en la escala actual. ')
        return response


class EditarValorEscala(UpdateView):

    model = ValorEscalaLikert
    form_class = FormValorEscala
    template_name = 'entrevista/escala/editar_valor_escala.html'
    context_object_name = 'valorEscala'

    def get_context_data(self, **kwargs):
        context = super(EditarValorEscala, self).get_context_data(**kwargs)
        valor = get_object_or_404(ValorEscalaLikert, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, valor.idEstudio.id, 2)
        context['rondas_activas'] = RondaJuicio.objects.filter(idEstudio=valor.idEstudio.id, estado=True).count()
        context['juicios'] = Juicio.objects.filter(idRonda__idEstudio=valor.idEstudio.id).count()

        valores_rango = [5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5]
        valores_registrados = ValorEscalaLikert.objects.filter(idEstudio=valor.idEstudio.id).order_by('-valor')

        # Se eliminan los puntajes que estan registrados en la escala exceptuando el del registro actual.
        for i in valores_registrados:
            if i.id != valor.id:
                valores_rango.remove(i.valor)
        context['valores'] = valores_rango
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Escala de Likert actualizada con exito.')
        return super(EditarValorEscala, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarValorEscala, self).form_invalid(form)
        messages.error(self.request, 'La escala no pudo ser actualizada. Verifique los datos ingresados')
        return response


class ConsultarValorEscala(DetailView):

    model = ValorEscalaLikert
    template_name = 'entrevista/escala/consultar_valor.html'
    context_object_name = 'valorEscala'

    def get_context_data(self, **kwargs):
        context = super(ConsultarValorEscala, self).get_context_data(**kwargs)
        valor = get_object_or_404(ValorEscalaLikert, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, valor.idEstudio.id, 2)
        return context


class EliminarValorEscala(DeleteView):

    model = ValorEscalaLikert
    template_name = 'entrevista/escala/eliminar_valor.html'
    context_object_name = 'valor'
    success_message = "Alternativa de respuesta eliminada de la escala."

    def get_context_data(self, **kwargs):
        context = super(EliminarValorEscala, self).get_context_data(**kwargs)
        valor = get_object_or_404(ValorEscalaLikert, id=self.kwargs['pk'])
        rondas = RondaJuicio.objects.filter(idEstudio=valor.idEstudio.id).order_by('numero_ronda')
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, valor.idEstudio.id, 2)
        context['rondas_registradas'] = rondas.count()
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarValorEscala, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        valor = get_object_or_404(ValorEscalaLikert, id=self.kwargs['pk'])
        return reverse('entrevista:escala', args={valor.idEstudio.id})


"""------------------------------------VIEWS MODELO RONDA--------------------------------------------------------"""


class ListaRondas(ListView):

    model = RondaJuicio
    template_name = 'entrevista/ronda/lista_rondas.html'
    context_object_name = 'rondas'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        actualizar_rondas(estudio.id)
        return RondaJuicio.objects.filter(idEstudio=estudio.id).order_by('-numero_ronda')

    def get_context_data(self, **kwargs):
        context = super(ListaRondas, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        context['hoy'] = date.today()
        context['rondas_activas'] = RondaJuicio.objects.filter(idEstudio=estudio.id, estado=True).count()
        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


class CrearRonda(CreateView):

    model = ValorEscalaLikert
    form_class = FormRonda
    template_name = 'entrevista/ronda/nueva_ronda.html'

    def get_context_data(self, **kwargs):
        context = super(CrearRonda, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        rondas = RondaJuicio.objects.filter(idEstudio=estudio.id).order_by('numero_ronda')
        preguntas = Pregunta.objects.filter(estado=True, idEstudio=estudio.id).count()
        escala = ValorEscalaLikert.objects.filter(idEstudio=estudio.id).count()

        if rondas.count() > 0:
            context['cant_rondas_activa'] = rondas.filter(estado=True).count()
            context['num_ronda'] = rondas.last().numero_ronda + 1
        else:
            context['cant_rondas_registradas'] = 0
            context['num_ronda'] = 1

        # Se verifica que existan preguntas registradas y una escala de likert que permita evaluarlas
        context['entradas_estudio'] = False
        if preguntas > 0 and escala > 1:
            context['entradas_estudio'] = True

        context['estudio'] = estudio
        context['num_preguntas'] = preguntas
        context['hoy'] = date.today()
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Ronda registrada con exito.')
        return super(CrearRonda, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearRonda, self).form_invalid(form)
        messages.error(self.request, 'La ronda no pudo ser registrada. Ingrese datos válidos')
        return response


class EditarRonda(UpdateView):

    model = RondaJuicio
    form_class = FormRonda
    template_name = 'entrevista/ronda/editar_ronda.html'
    context_object_name = 'ronda'

    def get_context_data(self, **kwargs):
        context = super(EditarRonda, self).get_context_data(**kwargs)
        ronda = get_object_or_404(RondaJuicio, id=self.kwargs['pk'])
        rondas = RondaJuicio.objects.filter(idEstudio=ronda.idEstudio_id).order_by('id')
        context['ultima_ronda'] = rondas.last()
        context['hoy'] = date.today()
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, ronda.idEstudio.id, 2)
        context['num_preguntas'] = Pregunta.objects.filter(estado=True, idEstudio=ronda.idEstudio_id).count()
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Ronda actualizada con exito.')
        return super(EditarRonda, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarRonda, self).form_invalid(form)
        messages.error(self.request, 'La ronda no pudo ser actualizada.')
        return response


class ConsultarRonda(DetailView):

    model = RondaJuicio
    template_name = 'entrevista/ronda/consultar_ronda.html'
    context_object_name = 'ronda'

    def get_context_data(self, **kwargs):
        context = super(ConsultarRonda, self).get_context_data(**kwargs)
        ronda = get_object_or_404(RondaJuicio, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, ronda.idEstudio.id, 2)
        return context

"""------------------------------------VIEWS MODELO JUICIO------------------------------------------------------"""


class ListaJuicios(ListView):

    model = Juicio
    template_name = 'entrevista/juicio/lista_juicios.html'
    context_object_name = 'juicios'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        actualizar_rondas(estudio.id)
        usuario = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        if usuario == "EXPERTO":
            return Juicio.objects.filter(idRonda__idEstudio=estudio.id, idExperto=self.request.user).\
                    order_by('-idRonda', 'texto_pregunta')
        else:
            return Juicio.objects.filter(idRonda__idEstudio=estudio.id).order_by('-idRonda', 'texto_pregunta')

    def get_context_data(self, **kwargs):
        context = super(ListaJuicios, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        rondas_activas = RondaJuicio.objects.filter(idEstudio=estudio.id, estado=True).order_by('id')
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)

        if rondas_activas.count() > 0:
            context['ronda_activa'] = rondas_activas.last()
            if context['usuario'] == 'EXPERTO':
                context['porcentaje'] = calcular_porcentaje_juicios(self, rondas_activas.last())

        # control de mensajes
        context.update(contexto_mensajes(self.request))
        return context


class CrearJuicio(CreateView):

    model = Juicio
    form_class = FormJuicio
    template_name = 'entrevista/juicio/nuevo_juicio.html'

    def get_context_data(self, **kwargs):
        context = super(CrearJuicio, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        preguntas = Pregunta.objects.filter(estado=True, idEstudio=estudio.id).order_by('id')
        valores = ValorEscalaLikert.objects.filter(estado=True, idEstudio=estudio.id).order_by('-valor')
        rondas = RondaJuicio.objects.filter(idEstudio=estudio.id)

        ronda_activa = []
        if rondas.count() > 0:
            ronda_activa = rondas.filter(idEstudio=estudio.id, estado=True).order_by('numero_ronda')

        juiciosUsuario = []
        if len(ronda_activa) > 0:
            ronda_activa = ronda_activa.last()
            juiciosUsuario = Juicio.objects.filter(idRonda__idEstudio=estudio.id, idExperto=self.request.user,
                                                   idRonda=ronda_activa.id)

        # obtengo porcentaje de juicios realizados por el usuario
        porcentaje = 0
        if len(juiciosUsuario) > 0:
            porcentaje = calcular_porcentaje_juicios(self, ronda_activa)

        # filtro de preguntas en juicios para que solo aparezcan en el select las que aun no se evaluan
        for juicio in juiciosUsuario:
            aux = preguntas.exclude(texto_pregunta=juicio.texto_pregunta)
            preguntas = aux

        context['estudio'] = estudio
        context['preguntas'] = preguntas
        context['valores'] = valores
        context['ronda'] = ronda_activa
        context['porcentaje'] = porcentaje
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        context['juicios'] = Juicio.objects.filter(idRonda__idEstudio=estudio.id,
                                                   idExperto=self.request.user).order_by('-idRonda__numero_ronda')

        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Juicio registrado con exito.')
        return super(CrearJuicio, self).form_valid(form)

    def form_invalid(self, form):
        response = super(CrearJuicio, self).form_invalid(form)
        messages.error(self.request, 'El juicio no pudo ser registrado. Verifique los datos ingresados.')
        return response

    def get_success_url(self):
        return reverse('entrevista:nuevo_juicio', args={self.args[0]})


class ConsultarJuicio(DetailView):

    model = Juicio
    template_name = 'entrevista/juicio/consultar_juicio.html'
    context_object_name = 'juicio'

    def get_context_data(self, **kwargs):
        context = super(ConsultarJuicio, self).get_context_data(**kwargs)
        juicio = get_object_or_404(Juicio, id=self.kwargs['pk'])
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, juicio.idRonda.idEstudio.id, 2)

        if context['usuario'] != 'EXPERTO':
            context['otros_juicios'] = Juicio.objects.filter(texto_pregunta=juicio.texto_pregunta)\
                .exclude(id=juicio.id).order_by('-idRonda__numero_ronda', 'idValorEscala__valor')
        elif context['usuario'] == 'EXPERTO':
            context['otros_juicios'] = Juicio.objects.filter(idExperto=self.request.user,
                                                             texto_pregunta=juicio.texto_pregunta)\
                .exclude(id=juicio.id).order_by('-idRonda__numero_ronda', 'idValorEscala__valor')

        context['tipoAcceso'] = self.kwargs['tipoAcceso']

        return context


class EditarJuicio(UpdateView):

    model = Juicio
    form_class = FormJuicio
    template_name = 'entrevista/juicio/editar_juicio.html'
    context_object_name = 'juicio'

    def get_context_data(self, **kwargs):
        context = super(EditarJuicio, self).get_context_data(**kwargs)
        juicio = get_object_or_404(Juicio, id=self.kwargs['pk'])
        estudio = get_object_or_404(EstudioEntrevista, id=juicio.idRonda.idEstudio.id)
        valores = ValorEscalaLikert.objects.filter(idEstudio=estudio.id).order_by('-valor')
        context['valores'] = valores
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, juicio.idRonda.idEstudio.id, 2)
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Juicio actualizado con exito.')
        return super(EditarJuicio, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EditarJuicio, self).form_invalid(form)
        messages.error(self.request, 'El juicio no pudo ser actualizado.')
        return response

    def get_success_url(self):
        juicio = get_object_or_404(Juicio, id=self.kwargs['pk'])
        estudio = get_object_or_404(EstudioEntrevista, id=juicio.idRonda.idEstudio.id)
        return reverse('entrevista:juicios', args={estudio.id})


class MatrizJuicios(TemplateView):

    template_name = 'entrevista/juicio/matriz_juicios.html'

    def get_context_data(self, **kwargs):
        context = super(MatrizJuicios, self).get_context_data(**kwargs)
        ronda = get_object_or_404(RondaJuicio, id=self.args[0])
        estudio = EstudioEntrevista.objects.get(id=ronda.idEstudio.id)
        context['estudio'] = estudio
        context['ronda'] = ronda
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        context['juicios_ronda'] = Juicio.objects.filter(idRonda_id=ronda.id).order_by('texto_pregunta')
        context['promedios'] = construirTablaPromedios(estudio, ronda)

        matriz = calcular_matriz_juicios(estudio, ronda, "")
        if len(matriz) > 1:
            context['cant_expertos'] = str(len(matriz) - 4) + "/" + str(len(estudio.idExpertos.all()))
            context['matriz'] = matriz
        else:
            context['matriz'] = 0
            context['cant_expertos'] = "0/" + str(len(estudio.idExpertos.all()))

        return context

"""------------------------------------VIEWS MODELO COEFICIENTE--------------------------------------------------"""


class ListaCoeficientes(ListView):

    model = CoeficienteAlfa
    template_name = 'entrevista/coeficiente/lista_coeficientes.html'
    context_object_name = 'coeficientes'

    def get_queryset(self):
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        ronda_activa = RondaJuicio.objects.filter(idEstudio_id=estudio.id, estado=True)

        if ronda_activa.count() > 0:
            ronda_activa = ronda_activa.last()
            registrar_coeficiente(ronda_activa)

        actualizar_rondas(estudio.id)
        coeficientes = CoeficienteAlfa.objects.filter(idRonda__idEstudio=estudio.id).order_by('idRonda__numero_ronda')
        return coeficientes

    def get_context_data(self, **kwargs):
        context = super(ListaCoeficientes, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)

        return context


# Genera el grafico de lineas que representa el coeficiente alcanzo en cada ronda
class GraficoCoeficiente(TemplateView):

    template_name = 'entrevista/coeficiente/grafico_coeficiente.html'

    def get_context_data(self, **kwargs):
        context = super(GraficoCoeficiente, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        context['estudio'] = estudio
        context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 2)
        actualizar_rondas(estudio.id)
        return context

"""--------------------------------------AUXILIARES--------------------------------------------------------------"""


# Clase auxiliar para la generacion de matrices
class Celda:
    def __init__(self, columna, valor, descripcion, pk=''):
        self.pk = pk
        self.columna = columna
        self.valor = valor
        self.descripcion = descripcion


# Calcula y construye la matriz de juicios de la ronda
def calcular_matriz_juicios(estudio, ronda, pregunta_excluida):

    juicios = Juicio.objects.filter(idRonda__id=ronda.id).order_by('idExperto', 'texto_pregunta')
    matriz = []

    if juicios.count() > 0:
        # exclusion de expertos que no han finalizado los juicios
        for experto in estudio.idExpertos.all():
            juicios_experto = Juicio.objects.filter(idRonda__id=ronda.id, idExperto=experto).count()
            if juicios_experto != ronda.numero_preguntas:
                aux = juicios.exclude(idExperto=experto)
                juicios = aux

        numero_preguntas = ronda.numero_preguntas
        if pregunta_excluida != "":
            numero_preguntas -= 1
            juicios = juicios.exclude(texto_pregunta=pregunta_excluida)

        fila = []
        valores = []
        suma_fila = 0
        suma_columna = [0] * (numero_preguntas + 1)
        cont = 0

        # se procede a crear la matriz
        try:
            for i in juicios:
                fila.append(Celda(len(fila) + 1, i.idValorEscala.valor, i.idValorEscala.nombre, i.id))
                suma_fila += i.idValorEscala.valor
                valores.append(i.idValorEscala.valor)
                if len(fila) == numero_preguntas:
                    fila.append(Celda(len(fila) + 1, suma_fila, suma_fila))   # columna suma fila
                    fila.insert(0, Celda(0, 'E' + str(cont + 1), "Experto"))  # columna expertos
                    matriz.append(fila)
                    valores.append(suma_fila)
                    suma_columna = map(sum, zip(suma_columna, valores))       # calculo del la suma por columna
                    valores = []
                    fila = []
                    cont += 1
                    suma_fila = 0

            # agregado de fila suma columnas y fila promedios
            fila_suma_columna = [Celda(0, "SUMA", "SUMA COLUMNA")]
            fila_promedios = [Celda(0, "PROM.", "PROMEDIO")]

            for valor in suma_columna:
                fila_suma_columna.append(Celda("", valor, valor))
                promedio = round(valor/len(matriz), 2)
                fila_promedios.append(Celda("", promedio, promedio))
            matriz.append(fila_suma_columna)
            matriz.append(fila_promedios)

            # agregado fila desviacion estandar por columna
            cont = 1
            desviacion = 0
            valores_columna = []
            fila_desviacion = [Celda(0, "DESV.", "DESVIACIÓN ESTANDAR")]
            while cont <= (numero_preguntas + 1):
                for lista in matriz:
                    for celda in lista:
                        if celda.columna == cont:
                            valores_columna.append(celda.valor)
                # Porque se necesitan por lo menos dos valores para calcular la desviacion de una muestra
                if len(valores_columna) > 1:
                    desviacion = round(stats.stdev(valores_columna), 2)
                fila_desviacion.append(Celda("", desviacion, desviacion))
                valores_columna = []
                cont += 1
            matriz.append(fila_desviacion)

            # se agregan los encabezados de cada columna
            fila_encabezados = [Celda(1, "Exp.", "EXPERTOS")]
            preguntas = []
            cont = 1

            for juicio in juicios:
                if juicio.texto_pregunta not in preguntas:
                    preguntas.append(juicio.texto_pregunta)
                    fila_encabezados.append(Celda(0, 'P' + str(cont), juicio.texto_pregunta))
                    cont += 1
            fila_encabezados.append(Celda(0, "SUMA", "SUMA FILA"))

            matriz.insert(0, fila_encabezados)
        except:
            print("La matriz de juicios no pudo ser creada")

    return matriz


# Calcula el coeficiente Alfa de Cronbach de la ronda
def calcular_coeficiente(ronda, matriz_juicios, pregunta_excluida):

    cant_preguntas = ronda.numero_preguntas
    if pregunta_excluida != "":  # si esta calculando el coeficiente simulando la exclusión de una pregunta
        cant_preguntas -= 1
    valores_desviacion = []
    coeficiente = 0

    if len(matriz_juicios) > 1:
        try:
            # seleccion de la fila desviacion estandar
            for fila in matriz_juicios:
                for celda in fila:
                    if celda.valor == "DESV.":
                        valores_desviacion = fila
                        fila.pop(0)

            desviacion_total = valores_desviacion[len(valores_desviacion) - 1]
            valores_desviacion.pop()

            suma_cuadrados = 0
            for celda in valores_desviacion:
                suma_cuadrados += celda.valor ** 2

            cuadrado_desviacion_total = desviacion_total.valor ** 2

            if cuadrado_desviacion_total > 0:
                a = cant_preguntas / (cant_preguntas - 1)
                b = 1 - (suma_cuadrados / cuadrado_desviacion_total)
                coeficiente = round(a * b, 2)
        except:
            print("No se pudo calcular el coeficiente")

    return coeficiente


# Calcula el porcentaje de diligenciamiento de juicios de una ronda
def calcular_porcentaje_juicios(self, ronda):

    preguntas = ronda.numero_preguntas
    juiciosUsuario = Juicio.objects.filter(idRonda__idEstudio=ronda.idEstudio.id, idExperto=self.request.user,
                                           idRonda=ronda.id).count()
    porcentaje = 0
    if juiciosUsuario > 0:
        porcentaje = round((100 / preguntas) * juiciosUsuario, 2)
    return porcentaje


# Crea las filas visualizadas en la tabla de promedios
def construirTablaPromedios(estudio, ronda):

    matriz_juicios_total = calcular_matriz_juicios(estudio, ronda, "")
    lista_promedios = []

    if len(matriz_juicios_total) > 0:
        try:
            fila_preguntas = matriz_juicios_total[0]  # Obtengo fila de encabezados que contiene las preguntas
            fila_preguntas.pop(0)                     # elimino encabezado columna 'Exp.'
            fila_preguntas.pop()                      # elimino encabezado columna 'SUMA'

            # Obtengo fila promedios
            fila_promedios = matriz_juicios_total[(len(matriz_juicios_total) - 2)]
            fila_promedios.pop(0)  # Elimino encabezado fila 'PROM'
            celda_promedio_total = fila_promedios.pop()  # Elimino valor sumatoria fila promedios

            # Obtengo el coeficiente alcanzado si se excluyen los juicios de la pregunta pasada como parametro
            for i in range(len(fila_preguntas)):
                matriz_juicios = calcular_matriz_juicios(estudio, ronda, fila_preguntas[i].descripcion)
                coeficiente = calcular_coeficiente(ronda, matriz_juicios, fila_preguntas[i].descripcion)
                lista_promedios.append(Celda(fila_preguntas[i].descripcion, fila_promedios[i].valor, coeficiente))

            coeficiente_total = calcular_coeficiente(ronda, matriz_juicios_total, "")
            fila_inicial = Celda("Todas las preguntas", celda_promedio_total.valor, coeficiente_total)
            lista_promedios.insert(0, fila_inicial)
        except:
            print("No se pudo crear la tabla promedios de juicios")

    return lista_promedios


# Actualiza el estado de las rondas, segun la fecha actual, el estado de la ronda, y el estado del estudio
def actualizar_rondas(idEstudio):

    estudio = get_object_or_404(EstudioEntrevista, id=idEstudio)
    rondas = RondaJuicio.objects.filter(idEstudio=estudio.id).order_by('numero_ronda')
    ultima_ronda = rondas.last()

    for ronda in rondas:
        # si se cumplio el tiempo de la ronda o el estado del estudio es cerrado
        if ronda.estado and date.today() > ronda.fecha_final or estudio.estado is False:
            ronda.estado = False
            ronda.save()
            registrar_coeficiente(ronda)
        # si el estudio esta cerrado o se desactiva la ronda y se crea otra, se cierra la anterior
        if estudio.estado is False or ronda.estado is False\
                and rondas.exclude(id=ronda.id).filter(estado=True).count() > 0:
            if ronda.fecha_final >= date.today():
                ronda.fecha_final = date.today() - timedelta(days=1)
                ronda.estado = False
                ronda.save()
                registrar_coeficiente(ronda)
        # si hay mas de una ronda abierta(posible por el admin)
        if len(rondas) > 1 and len(rondas.filter(estado=True)) > 1:
            if ronda.id != ultima_ronda.id:
                ronda.estado = False
                ronda.fecha_final = date.today() - timedelta(days=1)
                ronda.save()
                registrar_coeficiente(ronda)

# Registra o actualiza el coeficiente Alfa de Cronbach de la ronda.


def registrar_coeficiente(ronda):

    estudio = get_object_or_404(EstudioEntrevista, id=ronda.idEstudio.id)
    cant_preguntas = ronda.numero_preguntas
    matriz_juicios = calcular_matriz_juicios(estudio, ronda, "")
    valor = calcular_coeficiente(ronda, matriz_juicios, "")
    ver_coeficiente = CoeficienteAlfa.objects.filter(idRonda=ronda.id).exists()

    # cantidad de expertos que finalizaron la ronda
    cont = 0
    for experto in estudio.idExpertos.all():
        juicios_experto = Juicio.objects.filter(idRonda=ronda.id, idExperto=experto).count()
        if juicios_experto == cant_preguntas:
            cont += 1

    # si se se encuentra un coeficientre previo registrado para la ronda, se actualiza
    if ver_coeficiente:
        coef = CoeficienteAlfa.objects.get(idRonda=ronda.id)
        coef.valor = valor
        coef.num_expertos = cont
        coef.save()
    # si es primera vez
    else:
        coef = CoeficienteAlfa()
        coef.valor = valor
        coef.idRonda = ronda
        coef.num_expertos = cont
        coef.save()


# Retorna los datos que del gráfico de lineas
def datos_grafico(request):

    if request.is_ajax():
        estudio = get_object_or_404(EstudioEntrevista, id=int(request.GET['estudio']))
        coeficientes = CoeficienteAlfa.objects.filter(idRonda__idEstudio=estudio.id).order_by('idRonda__numero_ronda')
        labels = []
        valores = []

        cont = 0
        for coef in coeficientes:
            labels.append("R"+str(cont+1))
            valores.append(coef.valor)
            cont += 1

        data = {'labels': labels, 'coeficientes': valores}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


# Exporta a excel los datos del estudio
def exportar_estudio_xls(request, idEstudio):

    estudio = get_object_or_404(EstudioEntrevista, id=int(idEstudio))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+estudio.titulo+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    hoja_preguntas = wb.add_sheet('Preguntas')
    hoja_escala = wb.add_sheet('Escala de Likert')
    hoja_juicios = wb.add_sheet('Juicios')
    if request.user not in estudio.idExpertos.all():
        hoja_coeficientes = wb.add_sheet('Coeficientes')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns1 = ['Pregunta', 'Respuesta', 'Observación']
    columns2 = ['Nombre', 'Valor', 'Descripción']
    columns4 = ['Ronda', 'Pregunta', 'Valorización', 'Justificación']
    columns5 = ['Ronda', 'Coeficiente', 'Número de expertos', 'Preguntas']

    for col_num in range(len(columns1)):
        hoja_preguntas.write(row_num, col_num, columns1[col_num], font_style)

    for col_num in range(len(columns2)):
        hoja_escala.write(row_num, col_num, columns2[col_num], font_style)

    for col_num in range(len(columns4)):
        hoja_juicios.write(row_num, col_num, columns4[col_num], font_style)

    if request.user not in estudio.idExpertos.all():
        for col_num in range(len(columns5)):
            hoja_coeficientes.write(row_num, col_num, columns5[col_num], font_style)

    font_style = xlwt.XFStyle()
    filas = obtener_datos_estudio(request, estudio)

    for row in filas['preguntas']:
        row_num += 1
        for col_num in range(len(row)):
            hoja_preguntas.write(row_num, col_num, row[col_num], font_style)

    row_num = 0
    for row in filas['escala']:
        row_num += 1
        for col_num in range(len(row)):
            hoja_escala.write(row_num, col_num, row[col_num], font_style)

    row_num = 0
    for row in filas['juicios']:
        row_num += 1
        for col_num in range(len(row)):
            hoja_juicios.write(row_num, col_num, row[col_num], font_style)

    if request.user not in estudio.idExpertos.all():
        row_num = 0
        for row in filas['coeficientes']:
            row_num += 1
            for col_num in range(len(row)):
                hoja_coeficientes.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# Devuelve los datos a exportar a excel
def obtener_datos_estudio(request, estudio):

    filas_coeficientes = []

    filas_preguntas = Pregunta.objects.filter(idEstudio=estudio.id, estado=True).values_list(
                        'texto_pregunta', 'texto_respuesta', 'observacion').order_by('id')

    filas_escala = ValorEscalaLikert.objects.filter(idEstudio=estudio.id, estado=True).values_list(
                    'nombre', 'valor', 'descripcion').order_by('-valor')

    if request.user not in estudio.idExpertos.all():
        filas_juicios = Juicio.objects.filter(idRonda__idEstudio=estudio.id).values_list(
                        'idRonda__numero_ronda', 'texto_pregunta', 'idValorEscala__valor', 'justificacion').order_by(
                        'idRonda__numero_ronda')

        filas_coeficientes = CoeficienteAlfa.objects.filter(idRonda__idEstudio=estudio.id).values_list(
            'idRonda__numero_ronda', 'valor', 'num_expertos', 'idRonda__numero_preguntas')
    else:
        filas_juicios = Juicio.objects.filter(
                        idRonda__idEstudio=estudio.id, idExperto=request.user.id).values_list(
                        'idRonda__numero_ronda', 'texto_pregunta', 'idValorEscala__valor', 'justificacion').order_by(
                        'idRonda__numero_ronda')

    filas = {'preguntas': filas_preguntas, 'escala': filas_escala, 'juicios': filas_juicios,
             'coeficientes': filas_coeficientes}

    return filas


# para cambiar el estado de una pregunta, opcion de la escala o ronda (solo si esta abierta)
def cambiar_estado_pregunta_escala_ronda(request):

    if request.is_ajax():
        tipo = request.GET.get('tipo')
        error = True

        if tipo == 'pregunta':

            pregunta = get_object_or_404(Pregunta, id=int(request.GET.get('id')))
            pregunta.estado = not pregunta.estado

            try:
                pregunta.save()
                error = False
            except:
                print("No fue posible actualizar el estado de la pregunta")

        elif tipo == 'escala':

            opcion = get_object_or_404(ValorEscalaLikert, id=int(request.GET.get('id')))
            opcion.estado = not opcion.estado

            try:
                opcion.save()
                error = False
            except:
                print("No fue posible actualizar el estado de la opción")

        elif tipo == 'ronda':

            ronda = get_object_or_404(RondaJuicio, id=int(request.GET.get('id')))
            ronda.estado = not ronda.estado

            try:
                ronda.save()
                error = False
            except:
                print("No fue posible actualizar el estado de la ronda")

        response = JsonResponse({'error': error})
        return HttpResponse(response.content)
    else:
        return redirect('/')
