from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView
from apps.multipolv1.forms import EstudioMultipolForm
from django.contrib import messages

from apps.multipolv1.models import EstudioMultipol
from apps.proyecto.models import Proyecto, Tecnica
from apps.proyecto.views import contexto_mensajes, obtener_tipo_usuario_estudio


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

class CrearEstudio(CreateView):
    """Esta clase permite crear un nuevo estudio de multipol."""

    model = EstudioMultipol
    form_class = EstudioMultipolForm
    template_name = 'multipol/crear_estudio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tecnica = Tecnica.objects.get(codigo=5)
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        context['proyecto'] = proyecto
        context['tecnica'] = tecnica.id
        return context

    def form_valid(self, form):
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        form.instance.idAdministrador = proyecto.idAdministrador
        messages.success(self.request, 'El Estudio fue agregado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
        invalid_form = super().form_invalid(form)
        titulo = form.cleaned_data.get('titulo', '')

        existe_estudio = EstudioMultipol.objects.filter(
            idProyecto=proyecto, titulo=titulo).count()

        if existe_estudio > 0:
            messages.error(self.request, 'Ya existe un estudio con este mismo título')
        else:
            messages.error(self.request, 'Ingrese correctamente los datos del formulario')

        return invalid_form
  
class UpdateEstudio(UpdateView):
  model = EstudioMultipol
  template_name = 'multipol/edit_estudio.html'
  form_class = EstudioMultipolForm
  context_object_name = 'estudio'

  def form_valid(self, form):
    messages.success(self.request, 'El estudio se editó con éxito')
    return super().form_valid(form)

  def form_invalid(self, form):
      proyecto = get_object_or_404(Proyecto, id=self.kwargs['pk'])
      form_invalid = super().form_invalid(form)
      titulo = form.cleaned_data.get('titulo', '')
      estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
      estudios_existentes = EstudioMultipol.objects.filter(idProyecto=proyecto).exclude(id=estudio.id)

      if estudios_existentes.filter(titulo=titulo).exists():
          messages.error(self.request, f'Ya existe un estudio Multipol registrado con el nombre {titulo}')
      else:
          messages.error(self.request, 'El estudio no pudo ser actualizado. Verifique los datos ingresados.')
      return form_invalid


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def delete_estudio(request, *args, **kwargs):
    try:
        if request.is_ajax() and request.method == "POST":
            id = request.POST.get("id", None)
            estudio = EstudioMultipol.objects.get(pk=id)
            estudio.delete()
            return JsonResponse({'status': 'Estudio eliminado con exito!'}, status=200)
    except Exception:
       return JsonResponse({'status': 'Invalid request'}, status=400)
    return JsonResponse({'status': 'Invalid request'}, status=400)

### Gestion de acciones del estudio ############################################################
