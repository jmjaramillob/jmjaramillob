from django.contrib.sitemaps.views import index
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import json
from django.template.loader import render_to_string

from apps.multipol.forms import AccionForm, CriterioForm, \
  PoliticaForm, EstudioMultipolForm
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, \
  DeleteView, DetailView
from apps.multipol.models import *
from apps.proyecto.models import Tecnica, Proyecto
from apps.proyecto.views import *


####### GESTIÓN DE ESTUDIOS MULTIPOL ########################################################

class DetalleEstudio(DetailView):
  model = EstudioMultipol
  template_name = 'multipol/detalle_estudio.html'
  context_object_name = 'estudio'

  def get_context_data(self, **kwargs):
    context = super(DetalleEstudio, self).get_context_data(**kwargs)
    estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
    context['proyecto'] = estudio.idProyecto
    context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 5)
    
    

    return context


# Crea un estudio para la tecnica multipol
class CreateEstudio(CreateView):
  model = EstudioMultipol
  form_class = EstudioMultipolForm
  template_name = 'multipol/crear_estudio.html'

  def get_context_data(self, **kwargs):
    context = super(CreateEstudio, self).get_context_data(**kwargs)
    tecnica = Tecnica.objects.get(codigo=5)
    proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
    context['proyecto'] = proyecto
    context['tecnica'] = tecnica.id
    return context

  def form_valid(self, form):
    proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
    form.instance.idAdministrador = proyecto.idAdministrador
    print(self.request.POST)
    messages.add_message(
      self.request, messages.SUCCESS, 'El Estudio fue agregado con éxito'
    )
    return super(CreateEstudio, self).form_valid(form)

  def form_invalid(self, form):
    proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
    response = super(CreateEstudio, self).form_invalid(form)
    titulo = form.cleaned_data['titulo']

    estudios_existentes = EstudioMultipol.objects.filter(
      idProyecto=proyecto).order_by('titulo')

    if estudios_existentes.filter(titulo=titulo).count() > 0:
      messages.error(self.request, 'Ya existe un estudio con este mismo titulo')
      print(self.request.POST)

    else:
      messages.error(self.request, 'ingrese correctamente los datos del '
                                  'formulario')
      print(self.request.POST)


    return response

class UpdateEstudio(UpdateView):
  model = EstudioMultipol
  template_name = 'multipol/edit_estudio.html'
  form_class = EstudioMultipolForm
  context_object_name = 'estudio'

  def form_valid(self, form):
    messages.add_message(self.request, messages.SUCCESS, 'El estudio se edito con éxito')
    return super(UpdateEstudio, self).form_valid(form)

  def form_invalid(self, form):
    proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])

    response = super(UpdateEstudio, self).form_invalid(form)
    titulo = form.cleaned_data['titulo']

    estudios_existentes = EstudioMultipol.objects.filter(
      idProyecto=proyecto).order_by('titulo')
    estudios_existentes = estudios_existentes.exclude(id=estudio.id)

    if estudios_existentes.filter(titulo=titulo).count() > 0:
      messages.error(self.request, 'Ya existe un estudio Multipol registrado con el nombre ' + titulo)
    else:
      messages.error(self.request, 'El estudio no pudo ser actualizado. Verifique los datos ingresados.')
    return response


class DeleteEstudio(DeleteView):
  model = EstudioMultipol

  def get_context_data(self, **kwargs):
    context = super(DetalleEstudio, self).get_context_data(**kwargs)
    
    estudio = get_object_or_404(EstudioMultipol, id=self.args[0])
    context['estudio'] = estudio
    context['usuario'] = obtener_tipo_usuario_estudio(self.request, estudio.id, 5)
    self.actualizar_informe(estudio)

    informe = InformeFinal.objects.get(idEstudio_id=estudio.id)
    context.update(contexto_mensajes(self.request))
    return context

### Gestion de acciones del estudio ############################################################

class CreateAccion(CreateView):
  model = Accion
  form_class = AccionForm
  template_name = 'multipol/acciones/add_accion.html'

  def get_context_data(self, **kwargs):
    context = super(CreateAccion, self).get_context_data(**kwargs)
    estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
    context['estudio'] = estudio
    #self.actualizar_informe(estudio)

    context.update(contexto_mensajes(self.request))
    return context

  def form_valid(self, form):
    acciones_creadas = Accion.objects.filter(estudio=estudio.id).order_by('')

  def form_invalid(self, form):
    acciones_creadas = Accion.objects.filter(estudio=estudio.id).order_by('')

class ListAccion(ListView):
  model = Accion
  template_name = 'multipol/acciones/accion_list.html'
  context_object_name = 'acciones'

  # def actualizar_informe(self, estudio):
  #   actualizar_informes(estudio)

  def get_context_data(self, **kwargs):
    
    context = super(ListAccion, self).get_context_data(**kwargs)
    print(self.kwargs['pk'])
    estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
    context['estudio'] = estudio
    context['acciones'] = Accion.objects.filter(estudio=estudio.id)
    #self.actualizar_informe(estudio)

    context.update(contexto_mensajes(self.request))
    return context

class EditAccion(UpdateView):
  model = Accion
  form_class = AccionForm
  template_name = 'multipol/acciones/edit_accion.html'
  #success_url = reverse_lazy('multipol:lista_accion')

  def get_context_data(self, **kwargs):
    context = super(EditAccion, self).get_context_data(**kwargs)
    #estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk_estudio'])
    #context['estudio'] = estudio
    #self.actualizar_informe(estudio)

    context.update(contexto_mensajes(self.request))
    return context

class DeleteAccion(DeleteView):
  model = Accion
  #success_url = reverse_lazy('multipol:list_estudio')

  def post(self, request, *args, **kwargs):
    data = dict()
    if request.is_ajax():

      accion = json.loads(request.POST['content'])
      for i in accion:
        accion_delete = get_object_or_404(Accion, pk=i['id_accion'])
        accion_delete.delete()
        acciones = Accion.objects.all()
        data['html_data'] = render_to_string(
          'multipol/includes/accion_list_table.html', {'acciones': acciones})
    else:

      context = {}
      data['html_form'] = render_to_string(
        'multipol/includes/accion_confirm_delete.html', context,
        request=request)
    return JsonResponse(data)


### Gestion de criterios del estudio ############################################################

class CreateCriterio(CreateView):
  model = Criterio
  form_class = CriterioForm
  template_name = 'multipol/criterios/add_criterio.html'

  def get_context_data(self, **kwargs):
    context = super(CreateCriterio, self).get_context_data(**kwargs)
    estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
    context['estudio'] = estudio
    #self.actualizar_informe(estudio)

    context.update(contexto_mensajes(self.request))
    return context

class ListCriterio(ListView):
  model = Criterio
  template_name = 'multipol/criterios/criterio_list.html'
  context_object_name = 'criterios'

  def get_context_data(self, **kwargs):
    context = super(ListCriterio, self).get_context_data(**kwargs)
    estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
    context['estudio'] = estudio
    context['criterios'] = Criterio.objects.filter(estudio=estudio.id)
    #self.actualizar_informe(estudio)

    context.update(contexto_mensajes(self.request))
    return context

class EditCriterio(UpdateView):
  model = Criterio
  form_class = CriterioForm
  template_name = 'multipol/criterios/edit_criterio.html'

  def get_context_data(self, **kwargs):
    context = super(EditCriterio, self).get_context_data(**kwargs)
    print(self.request)
    #estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk_estudio'])
    #context['estudio'] = estudio
    #self.actualizar_informe(estudio)

    context.update(contexto_mensajes(self.request))
    return context

class DeleteCriterio(DeleteView):
  model = Criterio
  success_url = reverse_lazy('multipol:lista_criterio')

  def post(self, request, *args, **kwargs):
    data = dict()
    if request.is_ajax():

      criterio = json.loads(request.POST['content'])
      for i in criterio:
        criterio_delete = get_object_or_404(Criterio, pk=i['id_criterio'])
        criterio_delete.delete()
        criterios = Criterio.objects.all()
        data['html_data'] = render_to_string(
          'multipol/includes/criterio_list_table.html',
          {'criterios': criterios}
        )
    else:

      context = {}
      data['html_form'] = render_to_string(
        'multipol/includes/criterio_confirm_delete.html', context,
        request=request)
    return JsonResponse(data)

### Gestion de políticas del estudio ############################################################

class CreatePolitica(CreateView):
  model = Politica
  form_class = PoliticaForm
  template_name = 'multipol/politicas/add_politica.html'

  def get_context_data(self, **kwargs):
    context = super(CreatePolitica, self).get_context_data(**kwargs)
    estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
    context['estudio'] = estudio
    #self.actualizar_informe(estudio)

    context.update(contexto_mensajes(self.request))
    return context

class ListPolitica(ListView):
  model = Politica
  template_name = 'multipol/politicas/politica_list.html'
  context_object_name = 'politicas'

  def get_context_data(self, **kwargs):
    context = super(ListPolitica, self).get_context_data(**kwargs)
    estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
    context['estudio'] = estudio
    context['politicas'] = Politica.objects.filter(estudio=estudio.id)
    #self.actualizar_informe(estudio)

    context.update(contexto_mensajes(self.request))
    return context

class EditPolitica(UpdateView):
  model = Politica
  form_class = PoliticaForm
  template_name = 'multipol/politicas/edit_politica.html'

  def get_context_data(self, **kwargs):
    context = super(EditPolitica, self).get_context_data(**kwargs)
    #estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
    #context['estudio'] = estudio
    #self.actualizar_informe(estudio)

    context.update(contexto_mensajes(self.request))
    return context


class DeletePolitica(DeleteView):
  model = Politica
  success_url = reverse_lazy('multipol:lista_politica')

  def post(self, request, *args, **kwargs):
    data = dict()
    estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
    if request.is_ajax():

      politica = json.loads(request.POST['content'])
      for i in politica:
        politica_delete = get_object_or_404(Politica, pk=i['id_politica'])
        politica_delete.delete()
        politicas = Politica.objects.all()
        data['html_data'] = render_to_string(
          'multipol/includes/politica_list_table.html',
          {'politicas': politicas})
    else:

      context = {}
      data['html_form'] = render_to_string(
        'multipol/includes/politica_confirm_delete.html', context,
        request=request)
    return JsonResponse(data)

###### Gestión de las evaluaciones para los resultados de estudio #####################################################

def evaluacion_criterio_accion(request, pk):
  estudio = get_object_or_404(EstudioMultipol, id=pk)
  #evalt = EvaluacionTotalCA.objects.filter(estudio=estudio.id)
  #if evalt.exist():
  #  evalt = EvaluacionTotalCA(estudio=estudio)
  acciones = Accion.objects.filter(estudio=estudio.id)
  criterios = Criterio.objects.filter(estudio=estudio.id)
  experto = request.user
  if request.method == 'POST' or request.is_ajax():
    data = json.loads(request.POST['content'])
    for i in data:
      accion = Accion.objects.get(pk=i['accion'])
      criterio = Criterio.objects.get(pk=i['criterio'])
      valoracion = i['valoracionCA']
      evaluacionCA = EvaluacionCA(estudio=estudio, accion=accion, criterio=criterio,
                                  valoracionCA=valoracion, idExperto=experto)

      evaluacionCA.save()
    return index(request)


    self.actualizar_informe(estudio)

  context = {'acciones': acciones, 'criterios': criterios, 'estudio': estudio}
  return render(request, 'multipol/evaluaciones/evaluacion_criterio_accion.html', context)


def evaluacion_criterio_politica(request, pk):
  estudio = get_object_or_404(EstudioMultipol, id=pk)
  politicas = Politica.objects.filter(estudio=estudio.id)
  criterios = Criterio.objects.filter(estudio=estudio.id)
  experto = request.user
  #self.actualizar_informe(estudio)

  context = {'politicas': politicas, 'criterios': criterios, 'estudio': estudio}
  # evaluacionCP = EvaluacionCP
  # if EvaluacionCP.objects.exists():
  #   evaluacionCP = EvaluacionCP.objects.get(0)
  #   valueCP = evaluacionCP.valoracionCP
  #   context = {'politicas': politicas, 'criterios': criterios,
  #              'Valoraciones': valueCP}
  if request.method == 'POST' or request.is_ajax():
    data = json.loads(request.POST['content'])
    for i in data:
      politica = Politica.objects.get(pk=i['politica'])
      criterio = Criterio.objects.get(pk=i['criterio'])
      valoracionCP = i['valoracionCP']
      evaluacionCP = EvaluacionCP(
        estudio=estudio,
        politica=politica,
        criterio=criterio,
        valoracionCP=valoracionCP,
        opinion="aabc",
        idExperto=experto
      )
      evaluacionCP.save()
    return index(request)

  return render(request, 'multipol/evaluaciones/evaluacion_criterio_politica.html', context)


def evaluacion_accion_politica(request):
  estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
  evalCA = EvaluacionCA.objects.filter(estudio=estudio.id)
  evalCP = EvaluacionCP.objects.filter(estudio=estudio.id)

  self.actualizar_informe(estudio)
  # Cálculo para las evaluaciones de los criterios respecto a las acciones
  politicas = Politica.objects.all()
  acciones = Accion.objects.all()
  resultados = list()
  evaluaciones = list()
  evalAP = dict()
  for evalCA in EvaluacionCA.objects.all():
    for evalCP in EvaluacionCP.objects.all():
      if evalCA.criterio.id == evalCP.criterio.id:
        resultados.append((
          evalCA.accion.id, evalCP.politica.id,
          evalCA.valoracionCA * evalCP.valoracionCP
        ))
  for a, p, val in resultados:
    evalAP['variables'] = str(a) + str(p)
    evalAP['valoracion'] = val
    print(evalAP)
    evaluaciones.append(evalAP)
  print(evaluaciones)

  # print(list(EvaluacionCA.objects.all().values()))
  context = {
    'evaluacionAP': resultados,
    'acciones': acciones,
    'politicas': politicas,
    'idEstudio': estudio
  }
  return render(request, 'multipol/chart_evaluacion_accion_politica.html',
                context)

def llenar_matriz_evaluacionCA(request, pk):
    #consenso = verificar_consenso(request, idEstudio)
    evaluacionesCA = EvaluacionCA.objects.filter(estudio=pk).values()
    evaluacionesCA = list(evaluacionesCA)
    print(evaluacionesCA)
    return JsonResponse({'evaluacionesCA': evaluacionesCA})

