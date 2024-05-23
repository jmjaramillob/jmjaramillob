from audioop import mul
from django.contrib.auth.models import User
from .models import Proyecto, Mensaje
from ..mactor.models import EstudioMactor
from ..entrevista.models import EstudioEntrevista
from ..abaco.models import EstudioAbaco
from ..brainstorming.models import EstudioLluviaDeIdeas
from ..multipolv1.models import EstudioMultipol
from .forms import FormProyecto, FormNotificacion
from django.views.generic import ListView, CreateView, DetailView, UpdateView, \
  DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from datetime import date, datetime
from django.contrib import messages
from django.db.models import Count

from django.http import HttpResponse, JsonResponse


# ---- VISTAS MODELO PROYECTO


class Listaproyectos(ListView):
  model = Proyecto
  template_name = 'proyecto/lista_proyectos.html'
  context_object_name = 'proyectos'

  def get_queryset(self):
    self.proyectos = obtener_proyectos_usuario(self.request)
    return self.proyectos

  def get_context_data(self, **kwargs):
    context = super(Listaproyectos, self).get_context_data(**kwargs)
    context.update(contexto_mensajes(self.request))
    return context


# Registrar un nuevo proyecto prospectivo


class CrearProyecto(CreateView):
  model = Proyecto
  form_class = FormProyecto
  template_name = 'proyecto/crear_proyecto.html'

  def form_valid(self, form):
    messages.add_message(self.request, messages.SUCCESS,
                         'Proyecto registrado con exito.')
    return super(CrearProyecto, self).form_valid(form)

  def form_invalid(self, form):
    response = super(CrearProyecto, self).form_invalid(form)

    nombre = form.cleaned_data["nombre"]
    proyectos_registrados = obtener_proyectos_usuario(self.request)

    for proyecto in proyectos_registrados:
      if proyecto.nombre == nombre:
        messages.error(self.request,
                       'Ya existe un proyecto prospectivo registrado con el nombre ' + nombre)

    messages.error(self.request,
                   'El proyecto no pudo ser registrado. Verifique los datos ingresados.')
    return response

  @method_decorator(permission_required('proyecto.add_proyecto',
                                        reverse_lazy('proyecto:proyectos')))
  def dispatch(self, *args, **kwargs):
    return super(CrearProyecto, self).dispatch(*args, **kwargs)


# Muestra el detalle del proyecto


class ConsultarProyecto(DetailView):
  model = Proyecto
  template_name = 'proyecto/consultar_proyecto.html'
  context_object_name = 'proyecto'

  def get_context_data(self, **kwargs):
    context = super(ConsultarProyecto, self).get_context_data(**kwargs)
    proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
    context['usuario'] = obtener_tipo_usuario_proyecto(self.request,
                                                       proyecto.id)
    datos_estudios = obtener_estudios_proyecto(self.request, proyecto.id)
    context['estudios'] = datos_estudios['estudios']
    context['tecnicas'] = datos_estudios['tecnicas_aplicadas']
    context['cant_estudios'] = len(context['estudios'])
    context['cant_tecnicas'] = len(context['tecnicas'])
    # mensajes sin leer y de hoy
    context.update(contexto_mensajes(self.request))
    return context


# Editar los datos de un proyecto

class EditarProyecto(UpdateView):
  model = Proyecto
  form_class = FormProyecto
  template_name = 'proyecto/editar_proyecto.html'
  context_object_name = "proyecto"

  def form_valid(self, form):
    messages.add_message(self.request, messages.SUCCESS,
                         'Proyecto actualizado con exito.')
    return super(EditarProyecto, self).form_valid(form)

  def form_invalid(self, form):
    response = super(EditarProyecto, self).form_invalid(form)

    nombre = form.cleaned_data["nombre"]
    proyectos_registrados = obtener_proyectos_usuario(self.request)

    for proyecto in proyectos_registrados:
      if proyecto.nombre == nombre:
        messages.error(self.request,
                       'Ya existe un proyecto prospectivo registrado con el nombre ' + nombre)

    messages.error(self.request,
                   'El proyecto no pudo ser actualizado. Verifique los datos ingresados.')
    return response

  @method_decorator(permission_required('proyecto.change_proyecto',
                                        reverse_lazy('proyecto:proyectos')))
  def dispatch(self, *args, **kwargs):
    return super(EditarProyecto, self).dispatch(*args, **kwargs)


# Eliminar un proyecto


class EliminarProyecto(DeleteView):
  model = Proyecto
  template_name = 'proyecto/eliminar_proyecto.html'
  context_object_name = 'proyecto'
  success_message = "Proyecto eliminado con exito."

  def delete(self, request, *args, **kwargs):
    messages.success(self.request, self.success_message)
    return super(EliminarProyecto, self).delete(request, *args, **kwargs)

  def get_success_url(self):
    return reverse('proyecto:proyectos_prospectivos')


# Retorna los estudios registrados en el proyecto


class ConsultarEstudiosProyecto(DetailView):
  model = Proyecto
  template_name = 'proyecto/tabla_estudios_proyecto.html'

  def get_context_data(self, **kwargs):
    context = super(ConsultarEstudiosProyecto, self).get_context_data(**kwargs)
    proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])

    datos_estudios = obtener_estudios_proyecto(self.request, proyecto.id)
    context['estudios'] = datos_estudios['estudios']

    # mensajes sin leer y de hoy
    context.update(contexto_mensajes(self.request))
    return context


"""----GESTION DE PROYECTOS DEL USUARIO Y ROLES----"""


# Retorna la lista de proyectos del usuario en sesion


def obtener_proyectos_usuario(request):
  proyectos = Proyecto.objects.all().order_by('-estado', 'nombre')
  proyectos_usuario = []

  for proyecto in proyectos:
    if proyecto.estado:
      actualizar_roles_proyecto(
        proyecto.id)  # porque los expertos no se agregan al crear el proyecto
    if request.user in proyecto.idExpertos.all() \
      or request.user in proyecto.idCoordinadores.all() \
      or proyecto.idAdministrador == request.user:
      proyectos_usuario.append(proyecto)

  actualizar_proyectos(proyectos_usuario)
  return proyectos_usuario


# Actualiza el estado de los proyectos de acuerdo a su fecha de cierre

def actualizar_proyectos(proyectos_usuario):
  for proyecto in proyectos_usuario:
    if proyecto.estado:
      if date.today() > proyecto.fecha_final:
        proyecto.estado = False
        proyecto.save()


# Obtiene los expertos de cada estudio y los agrega al proyecto

def actualizar_roles_proyecto(idProyecto):
  proyecto = get_object_or_404(Proyecto, id=idProyecto)
  abaco = EstudioAbaco.objects.filter(idProyecto_id=idProyecto)
  mactor = EstudioMactor.objects.filter(idProyecto_id=idProyecto)
  entrevista = EstudioEntrevista.objects.filter(idProyecto_id=idProyecto)
  lluvia = EstudioLluviaDeIdeas.objects.filter(idProyecto_id=idProyecto)
  multipol = EstudioMultipol.objects.filter(idProyecto_id = idProyecto)

  def agregar_expertos(estudios):

    for est in estudios:
      for exp in est.idExpertos.all():
        if not (exp in proyecto.idExpertos.all()):
          proyecto.idExpertos.add(exp)

  # Estudios abaco
  if abaco.count() > 0:
    agregar_expertos(abaco)

  # Estudios mactor
  if mactor.count() > 0:
    agregar_expertos(mactor)

  # Estudios entrevista
  if entrevista.count() > 0:
    agregar_expertos(entrevista)

  # Estudios lluvia de ideas
  if lluvia.count() > 0:
    agregar_expertos(lluvia)

  # Estudios lluvia de ideas
  if multipol.count() > 0:
    agregar_expertos(multipol)

# Determina el tipo de rol que ocupa el usuario actual dentro del proyecto

def obtener_tipo_usuario_proyecto(request, idProyecto):
  proyecto = Proyecto.objects.get(id=idProyecto)
  lista_coordinadores = proyecto.idCoordinadores.all()
  lista_expertos = proyecto.idExpertos.all()
  tipo = ""

  if request.user == proyecto.idAdministrador:
    tipo = "ADMINISTRADOR_PROY"
  elif request.user in lista_coordinadores:
    tipo = "COORDINADOR_PROY"
  elif request.user in lista_expertos:
    tipo = "EXPERTO_PROY"
  return tipo


"""----GESTION DE LOS ESTUDIOS DEL PROYECTO----"""


# Obtener estudios del proyecto

def obtener_estudios_proyecto(request, idProyecto):
  estudios = []
  tecnicas_aplicadas = []

  class EstudioProspectivo:
    def __init__(self, prosp, rol):
      self.prosp = prosp
      self.rol = rol

  # estudios mactor
  mactor = EstudioMactor.objects.filter(idProyecto_id=idProyecto).order_by(
    '-estado', 'titulo')

  # estudios entrevista
  entrevista = EstudioEntrevista.objects.filter(
    idProyecto_id=idProyecto).order_by('-estado', 'titulo')

  # estudios abaco
  abaco = EstudioAbaco.objects.filter(idProyecto_id=idProyecto).order_by(
    '-estado', 'titulo')

  # estudios lluvia de ideas
  lluvia = EstudioLluviaDeIdeas.objects.filter(
    idProyecto_id=idProyecto).order_by('-estado', 'titulo')

  # estudios mulipol
  multipol = EstudioMultipol.objects.filter(
    idProyecto_id=idProyecto).order_by('-estado', 'titulo')

  if mactor.count() > 0:
    actualizar_estudios(mactor)
    tecnicas_aplicadas.append("MACTOR")

    for est in mactor:
      if request.user == est.idAdministrador \
        or request.user == est.idCoordinador \
        or request.user in est.idExpertos.all():
        rol = obtener_tipo_usuario_estudio(request, est.id, 1)
        a = EstudioProspectivo(est, rol)
        estudios.append(a)

  if entrevista.count() > 0:
    actualizar_estudios(entrevista)
    tecnicas_aplicadas.append("Entrevista")

    for est in entrevista:
      if request.user == est.idAdministrador \
        or request.user == est.idCoordinador \
        or request.user in est.idExpertos.all():
        rol = obtener_tipo_usuario_estudio(request, est.id, 2)
        a = EstudioProspectivo(est, rol)
        estudios.append(a)

  if abaco.count() > 0:
    actualizar_estudios(abaco)
    tecnicas_aplicadas.append("Abaco de Regnier")

    for est in abaco:
      if request.user == est.idAdministrador \
        or request.user in est.idCoordinadores.all() \
        or request.user in est.idExpertos.all():
        rol = obtener_tipo_usuario_estudio(request, est.id, 3)
        a = EstudioProspectivo(est, rol)
        estudios.append(a)

  if lluvia.count() > 0:
    actualizar_estudios(lluvia)
    tecnicas_aplicadas.append("Lluvia de Ideas")

    for est in lluvia:
      if request.user == est.idAdministrador \
        or request.user == est.idCoordinador \
        or request.user in est.idExpertos.all():
        rol = obtener_tipo_usuario_estudio(request, est.id, 4)
        a = EstudioProspectivo(est, rol)
        estudios.append(a)

  if multipol.count() > 0:
    actualizar_estudios(multipol)
    tecnicas_aplicadas.append("Multipol")

    for est in multipol:
      if request.user == est.idAdministrador \
        or request.user == est.idCoordinador \
        or request.user in est.idExpertos.all():
        rol = obtener_tipo_usuario_estudio(request, est.id, 5)
        a = EstudioProspectivo(est, rol)
        estudios.append(a)

  datos_estudios = {'estudios': estudios,
                    'tecnicas_aplicadas': tecnicas_aplicadas}

  return datos_estudios


# Obtiene un estudio segun su tipo usado en el envio y listado de los mensajes

def obtener_estudio(idEstudio, tipoEstudio):
  idEstudio = int(idEstudio)
  estudio = ''
  if tipoEstudio == 1:
    estudio = get_object_or_404(EstudioMactor, id=idEstudio)
  elif tipoEstudio == 2:
    estudio = get_object_or_404(EstudioEntrevista, id=idEstudio)
  elif tipoEstudio == 3:
    estudio = get_object_or_404(EstudioAbaco, id=idEstudio)
  elif tipoEstudio == 4:
    estudio = get_object_or_404(EstudioLluviaDeIdeas, id=idEstudio)
  elif tipoEstudio == 5:
    estudio = get_object_or_404(EstudioMultipol, id=idEstudio)

  return estudio


# Determina el rol que ocupa el usuario en sesión en el estudio
def obtener_tipo_usuario_estudio(request, idEstudio, tipoEstudio):
  tipo = ""
  tipoEstudio = int(tipoEstudio)
  if tipoEstudio == 1:

    estudio = get_object_or_404(EstudioMactor, id=idEstudio)
    lista_expertos = estudio.idExpertos.all()

    if request.user == estudio.idAdministrador or request.user == estudio.idCoordinador:
      tipo = "COORDINADOR"
    if request.user in lista_expertos and tipo == "COORDINADOR":
      tipo = "COORDINADOR_EXPERTO"
    elif request.user in lista_expertos:
      tipo = "EXPERTO"

  elif tipoEstudio == 2:

    estudio = get_object_or_404(EstudioEntrevista, id=idEstudio)
    lista_expertos = estudio.idExpertos.all()

    if request.user == estudio.idAdministrador or request.user == estudio.idCoordinador:
      tipo = "COORDINADOR"
    elif request.user in lista_expertos:
      tipo = "EXPERTO"

  elif tipoEstudio == 3:

    estudio = get_object_or_404(EstudioAbaco, id=idEstudio)
    lista_expertos = estudio.idExpertos.all()
    lista_coordinadores = estudio.idCoordinadores.all()

    if request.user == estudio.idAdministrador or request.user in lista_coordinadores:
      tipo = "COORDINADOR"
    if request.user in lista_expertos and tipo == "COORDINADOR":
      tipo = "COORDINADOR_EXPERTO"
    elif request.user in lista_expertos:
      tipo = "EXPERTO"

  elif tipoEstudio == 4:

    estudio = get_object_or_404(EstudioLluviaDeIdeas, id=idEstudio)
    lista_expertos = estudio.idExpertos.all()

    if request.user == estudio.idAdministrador or request.user == estudio.idCoordinador:
      tipo = "COORDINADOR"
    elif request.user in lista_expertos:
      tipo = "EXPERTO"

  elif tipoEstudio == 5:
    estudio = get_object_or_404(EstudioMultipol, id=idEstudio)
    lista_expertos = estudio.idExpertos.all()
    #lista_coordinadores = estudio.idCoordinador

    if request.user == estudio.idAdministrador or request.user == estudio.idCoordinador:
      tipo = 'COORDINADOR'
    elif request.user in lista_expertos:
      tipo = 'EXPERTO'

  return tipo


# Actualiza el estado de los estudios del usuario a medida que este se desarrolla
def actualizar_estudios(estudios_usuario):
  for estudio in estudios_usuario:
    if estudio.estado:
      if date.today() > estudio.idProyecto.fecha_final or estudio.idProyecto.estado is False \
        or date.today() > estudio.fecha_final:
        estudio.estado = False
        estudio.save()


"""----GESTION DE MENSAJES---"""


# Enviar mensaje desde la lista de mensajes del proyecto en general

class EnviarMensaje(CreateView):
  model = Mensaje
  form_class = FormNotificacion
  template_name = 'proyecto/mensajes/lista_mensajes_proyecto.html'

  def get_context_data(self, **kwargs):
    context = super(EnviarMensaje, self).get_context_data(**kwargs)
    proyecto = get_object_or_404(Proyecto, id=int(self.kwargs['pk']))

    mensajes = obtener_mensajes_usuario(self.request, proyecto.id)
    context['mensajes_recibidos'] = mensajes['destinatario']
    context['mensajes_enviados'] = mensajes['emisor']
    context['proyecto'] = proyecto
    context['usuario'] = obtener_tipo_usuario_proyecto(self.request,
                                                       proyecto.id)

    # mensajes sin leer y de hoy
    context.update(contexto_mensajes(self.request))

    return context

  def form_valid(self, form):
    form.instance.idEmisor = self.request.user
    form.instance.idProyecto = get_object_or_404(Proyecto,
                                                 id=int(self.kwargs['pk']))

    messages.add_message(self.request, messages.SUCCESS, 'Mensaje enviado')
    return super(EnviarMensaje, self).form_valid(form)

  def form_invalid(self, form):
    response = super(EnviarMensaje, self).form_invalid(form)
    messages.error(self.request,
                   'El mensaje no pudo ser enviado. Verifique los datos ingresados.')
    return response

  def get_success_url(self):
    proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
    return reverse('proyecto:mensajes', kwargs={'pk': proyecto.id})


class ConsultarMensaje(DetailView):
  model = Mensaje
  template_name = 'proyecto/mensajes/ver_mensaje.html'
  context_object_name = 'mensaje'

  def get_context_data(self, **kwargs):
    context = super(ConsultarMensaje, self).get_context_data(**kwargs)
    mensaje = get_object_or_404(Mensaje, id=self.kwargs['pk'])

    # cambio el estado del mensaje a visto
    if mensaje.idEmisor_id != self.request.user.id and mensaje.estado is False:
      mensaje.estado = not mensaje.estado
      mensaje.save()

    context['mensaje'] = mensaje
    context['usuario'] = obtener_tipo_usuario_proyecto(self.request,
                                                       mensaje.idProyecto.id)

    # mensajes sin leer y de hoy
    context.update(contexto_mensajes(self.request))
    return context


# Enviar mensaje dentro de un estudio
class EnviarMensajeEstudio(CreateView):
  model = Mensaje
  form_class = FormNotificacion
  template_name = 'proyecto/mensajes/lista_mensajes_estudios.html'

  def get_context_data(self, **kwargs):
    context = super(EnviarMensajeEstudio, self).get_context_data(**kwargs)
    idEstudio = int(self.kwargs['pk'])
    tipoEstudio = int(self.kwargs['tipoEstudio'])
    estudio = obtener_estudio(idEstudio, tipoEstudio)

    mensajes = obtener_mensajes_usuario(self.request, estudio.idProyecto.id,
                                        estudio)
    context['mensajes_recibidos'] = mensajes['destinatario']
    context['mensajes_enviados'] = mensajes['emisor']
    context['estudio'] = estudio
    context['usuario'] = obtener_tipo_usuario_estudio(self.request, idEstudio,
                                                      tipoEstudio)

    # mensajes sin leer y de hoy
    context.update(contexto_mensajes(self.request))

    return context

  def form_valid(self, form):
    estudio = obtener_estudio(int(self.kwargs['pk']),
                              int(self.kwargs['tipoEstudio']))
    form.instance.idEmisor = self.request.user
    form.instance.idProyecto = estudio.idProyecto
    form.instance.idEstudio = estudio.id
    form.instance.tipoEstudio = estudio.tipoTecnica.codigo
    form.instance.tituloEstudio = estudio.titulo

    messages.add_message(self.request, messages.SUCCESS, 'Mensaje enviado')
    return super(EnviarMensajeEstudio, self).form_valid(form)

  def form_invalid(self, form):
    response = super(EnviarMensajeEstudio, self).form_invalid(form)
    messages.error(self.request,
                   'El mensaje no pudo ser enviado. Verifique los datos ingresados.')
    return response

  def get_success_url(self):
    return reverse('proyecto:mensajes_estudio', kwargs={'pk': self.kwargs['pk'],
                                                        'tipoEstudio':
                                                          self.kwargs[
                                                            'tipoEstudio']})


# Ver el mensaje dentro de un estudio
class ConsultarMensajeEstudio(DetailView):
  model = Mensaje
  template_name = 'proyecto/mensajes/ver_mensaje_estudio.html'
  context_object_name = 'mensaje'

  def get_context_data(self, **kwargs):
    context = super(ConsultarMensajeEstudio, self).get_context_data(**kwargs)
    mensaje = get_object_or_404(Mensaje, id=self.kwargs['pk'])

    # cambio el estado del mensaje a visto
    if mensaje.idEmisor_id != self.request.user.id and mensaje.estado is False:
      mensaje.estado = not mensaje.estado
      mensaje.save()

    context['mensaje'] = mensaje
    context['usuario'] = obtener_tipo_usuario_estudio(self.request,
                                                      mensaje.idEstudio,
                                                      mensaje.tipoEstudio)

    # mensajes sin leer y de hoy
    context.update(contexto_mensajes(self.request))
    return context


# devuelve la lista de destinatarios segun la opcion seleccionada por el usuario
def obtener_destinatarios(request):
  if request.is_ajax():
    id = request.GET.get('idProyecto')
    tipo = request.GET.get('tipo')
    destinatarios = []

    proyecto = get_object_or_404(Proyecto, id=int(id))
    coordinadores = User.objects.filter(
      id__in=proyecto.idCoordinadores.all()).exclude(id=request.user.id)
    expertos = User.objects.filter(id__in=proyecto.idExpertos.all()).exclude(
      id=request.user.id)

    if tipo == 'todos':
      if request.user.id != proyecto.idAdministrador.id:
        admin = User.objects.filter(id=proyecto.idAdministrador_id)
        destinatarios = admin | coordinadores
        destinatarios = destinatarios.distinct()
      else:
        destinatarios = coordinadores | expertos
        destinatarios = destinatarios.distinct()
    elif tipo == 'admin':
      destinatarios = User.objects.filter(id=proyecto.idAdministrador_id)
    elif tipo == 'coordinadores':
      destinatarios = coordinadores

    else:
      destinatarios = expertos

    lista_ids = []

    for dest in destinatarios:
      lista_ids.append(dest.id)

    response = JsonResponse({'ids': lista_ids})
    return HttpResponse(response.content)
  else:
    return redirect('/')


# devuelve la lista de destinatarios segun la opcion seleccionada por el usuario dentro de un estudio
def obtener_destinatarios_estudios(request):
  if request.is_ajax():
    idEstudio = int(request.GET.get('idEstudio'))
    tipoEstudio = int(request.GET.get('tipoEstudio'))
    tipoDestinatario = request.GET.get('tipo')
    destinatarios = []
    estudio = obtener_estudio(idEstudio, tipoEstudio)

    if tipoEstudio == 1 or tipoEstudio == 2:
      destinatarios = destinatarios_mactor_entrevista(request, estudio,
                                                      tipoDestinatario)
    elif tipoEstudio == 3:
      destinatarios = destinatarios_abaco(request, estudio, tipoDestinatario)

    lista_ids = []

    for dest in destinatarios:
      lista_ids.append(dest.id)

    response = JsonResponse({'ids': lista_ids})
    return HttpResponse(response.content)
  else:
    return redirect('/')


# destinatarios para la tecnica mactor
def destinatarios_mactor_entrevista(request, estudio, tipoDestinatario):
  destinatarios = []
  usuario = obtener_tipo_usuario_estudio(request, estudio.id,
                                         estudio.tipoTecnica.codigo)

  if tipoDestinatario == 'todos':
    # para el admin
    if estudio.idAdministrador.id == request.user.id:
      coordinador = User.objects.filter(id=estudio.idCoordinador_id).exclude(
        id=request.user.id)
      expertos = User.objects.filter(id__in=estudio.idExpertos.all()).exclude(
        id=request.user.id)
      destinatarios = coordinador | expertos
    # para el coordinador
    elif estudio.idCoordinador.id == request.user.id:
      expertos = User.objects.filter(id__in=estudio.idExpertos.all()).exclude(
        id=request.user.id)
      admin = User.objects.filter(id=estudio.idAdministrador_id)
      destinatarios = admin | expertos
    # para los expertos
    elif usuario == 'EXPERTO':
      admin = User.objects.filter(id=estudio.idAdministrador_id).exclude(
        id=request.user.id)
      coordinador = User.objects.filter(id=estudio.idCoordinador_id).exclude(
        id=request.user.id)
      destinatarios = admin | coordinador

  elif tipoDestinatario == 'admin':
    destinatarios = User.objects.filter(id=estudio.idAdministrador_id)
  elif tipoDestinatario == 'coordinadores':
    destinatarios = User.objects.filter(id=estudio.idCoordinador_id)
  else:
    destinatarios = User.objects.filter(
      id__in=estudio.idExpertos.all()).exclude(id=request.user.id)

  destinatarios = destinatarios.distinct()

  return destinatarios


# destinatarios para la tecnica abaco de regnier
def destinatarios_abaco(request, estudio, tipoDestinatario):
  destinatarios = []
  usuario = obtener_tipo_usuario_estudio(request, estudio.id,
                                         estudio.tipoTecnica.codigo)

  if tipoDestinatario == 'todos':

    # para el admin
    if estudio.idAdministrador.id == request.user.id:
      coordinadores = User.objects.filter(
        id__in=estudio.idCoordinadores.all()).exclude(id=request.user.id)
      expertos = User.objects.filter(id__in=estudio.idExpertos.all()).exclude(
        id=request.user.id)
      destinatarios = coordinadores | expertos
    # para el coordinador
    elif request.user in estudio.idCoordinadores.all():
      admin = User.objects.filter(id=estudio.idAdministrador_id)
      coordinadores = User.objects.filter(
        id__in=estudio.idCoordinadores.all()).exclude(id=request.user.id)
      expertos = User.objects.filter(id__in=estudio.idExpertos.all()).exclude(
        id=request.user.id)
      destinatarios = admin | coordinadores
      destinatarios = destinatarios | expertos
    # para los expertos
    elif usuario == 'EXPERTO':
      admin = User.objects.filter(id=estudio.idAdministrador_id).exclude(
        id=request.user.id)
      coordinadores = User.objects.filter(
        id__in=estudio.idCoordinadores.all()).exclude(id=request.user.id)
      destinatarios = admin | coordinadores

  elif tipoDestinatario == 'admin':
    destinatarios = User.objects.filter(id=estudio.idAdministrador_id)
  elif tipoDestinatario == 'coordinadores':
    destinatarios = User.objects.filter(
      id__in=estudio.idCoordinadores.all()).exclude(id=request.user.id)
  elif tipoDestinatario == 'admin_coo':
    admin = User.objects.filter(id=estudio.idAdministrador_id)
    coordinadores = User.objects.filter(
      id__in=estudio.idCoordinadores.all()).exclude(id=request.user.id)
    destinatarios = admin | coordinadores
  else:
    destinatarios = User.objects.filter(
      id__in=estudio.idExpertos.all()).exclude(id=request.user.id)

  destinatarios = destinatarios.distinct()

  return destinatarios


# Obtener contexto mensajes para el navbar
def contexto_mensajes(request):
  proyectos = obtener_proyectos_usuario(request)
  mensajes = obtener_mensajes_usuario(request)['destinatario']
  sin_leer = obtener_mensajes_sin_leer(proyectos, mensajes)
  sin_leer_hoy = obtener_mensajes_hoy_sin_leer(request, proyectos)

  context = {'mensajes_navbar_sin_leer': sin_leer[0],
             'total_sin_leer': sin_leer[1],
             'mensajes_navbar_hoy_sin_leer': sin_leer_hoy[0],
             'total_hoy_sin_leer': sin_leer_hoy[1]}

  return context


# devuelve los mensajes del usuario
def obtener_mensajes_usuario(request, idProyecto='', estudio=''):
  mensajes_emisor = Mensaje.objects.filter(hijoMultiple=False,
                                           idEmisor_id=request.user.id)
  multiples = mensajes_emisor.annotate(c=Count('idDestinatarios')).filter(
    c__gt=1, multiples=False)
  enviar_mensaje_multiple(multiples)  # para que se cree el mensaje individual
  mensajes_destinatario = Mensaje.objects.filter(multiples=False,
                                                 idDestinatarios__id=request.user.id)

  if idProyecto != '':
    mensajes_emisor = mensajes_emisor.filter(idProyecto_id=idProyecto)
    mensajes_destinatario = mensajes_destinatario.filter(
      idProyecto_id=idProyecto)

  if estudio != '':
    mensajes_emisor = mensajes_emisor.filter(idEstudio=estudio.id,
                                             tipoEstudio=estudio.tipoTecnica.codigo)
    mensajes_destinatario = mensajes_destinatario.filter(idEstudio=estudio.id,
                                                         tipoEstudio=estudio.tipoTecnica.codigo)

  return {'emisor': mensajes_emisor, 'destinatario': mensajes_destinatario}


# devuelve la lista de proyectos donde hay mensajes sin leer junto a la cantidad de mensajes respectiva
def obtener_mensajes_sin_leer(proyectos, mensajes):
  # excluyo mensajes con multiples usuarios
  mensajes = mensajes.exclude(multiples=True)
  # excluyo mensajes ya leidos
  mensajes = mensajes.exclude(estado=True)

  # proyectos donde existen mensajes sin leer
  lista_proyectos = []
  total = 0
  for proyecto in proyectos:
    cantidad = mensajes.filter(idProyecto=proyecto.id).count()
    if cantidad > 0:
      total += cantidad
      lista_proyectos.append({'proyecto': proyecto, 'cantidad': cantidad})

  lista_contexto = [lista_proyectos, total]

  return lista_contexto


# devuelve la lista de proyectos donde hay mensajes del dia en curso sin leer
def obtener_mensajes_hoy_sin_leer(request, proyectos):
  # obtengo mensajes donde el usuario es destinatario
  mensajes = Mensaje.objects.filter(idDestinatarios__id=request.user.id,
                                    multiples=False)
  # obtengo mensajes del dia en curso
  mensajes = mensajes.filter(fechaHora__contains=date.today())
  # excluyo mensajes ya leidos
  mensajes = mensajes.exclude(estado=True)

  # proyectos donde existen mensajes sin leer del dia en curso
  lista_proyectos = []
  total = 0
  for proyecto in proyectos:
    cantidad = mensajes.filter(idProyecto=proyecto.id).count()
    if cantidad > 0:
      total += cantidad
      lista_proyectos.append({'proyecto': proyecto, 'cantidad': cantidad})

  lista_contexto = [lista_proyectos, total]

  return lista_contexto


# Enviar mensaje multiple (cuando el mensaje tiene mas de un destinatario), esto para controlar el estado del mensaje
def enviar_mensaje_multiple(mensajes_multiples):
  for mens in mensajes_multiples:
    for dest in mens.idDestinatarios.all():
      if dest != mens.idEmisor:
        m = Mensaje()
        m.idEmisor = mens.idEmisor
        m.fechaHora = mens.fechaHora
        m.mensaje = mens.mensaje
        m.hijoMultiple = True
        m.idProyecto = mens.idProyecto
        m.idEstudio = mens.idEstudio
        m.tipoEstudio = mens.tipoEstudio
        m.tituloEstudio = mens.tituloEstudio
        m.save()
        m.idDestinatarios.add(dest)
        m.save()

    mens.multiples = True
    mens.save()


# para cambiar el estado de un mensaje sin abrirlo (en la lista de mensajes)
def cambiar_estado_mensaje(request):
  if request.is_ajax():
    error = True
    mensaje = get_object_or_404(Mensaje, id=int(request.GET.get('id')))
    mensaje.estado = not mensaje.estado

    try:
      mensaje.save()
      error = False
    except:
      print("No fue posible actualizar el estado de la pregunta")

    response = JsonResponse({'error': error})
    return HttpResponse(response.content)
  else:
    return redirect('/')
