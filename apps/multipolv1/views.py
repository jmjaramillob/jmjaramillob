import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.multipolv1.forms import (
    Accion,
    AccionForm,
    Criterio,
    CriterioForm,
    EstudioMultipolForm,
    Politica,
    PoliticaForm,
)
from apps.multipolv1.models import (
    EstudioMultipol,
    EvaluacionCriterioAccion,
    EvaluacionCriterioPolitica,
)
from apps.proyecto.models import Proyecto, Tecnica
from apps.proyecto.views import contexto_mensajes, obtener_tipo_usuario_estudio

####### GESTIÓN DE ESTUDIOS MULTIPOL ########################################################


class DetalleEstudio(DetailView):
    model = EstudioMultipol
    template_name = "multipol/detalle_estudio.html"
    context_object_name = "estudio"

    def get_context_data(self, **kwargs):
        context = super(DetalleEstudio, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioMultipol, id=self.kwargs["pk"])
        context["proyecto"] = estudio.idProyecto
        context["usuario"] = obtener_tipo_usuario_estudio(self.request, estudio.id, 5)
        return context


class CrearEstudio(CreateView):
    """Esta clase permite crear un nuevo estudio de multipol."""

    model = EstudioMultipol
    form_class = EstudioMultipolForm
    template_name = "multipol/crear_estudio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tecnica = Tecnica.objects.get(codigo=5)
        proyecto = get_object_or_404(Proyecto, id=self.kwargs["pk"])
        context["proyecto"] = proyecto
        context["tecnica"] = tecnica.id
        return context

    def form_valid(self, form):
        proyecto = get_object_or_404(Proyecto, id=self.kwargs["pk"])
        form.instance.idAdministrador = proyecto.idAdministrador
        messages.success(self.request, "El Estudio fue agregado con éxito")
        return super().form_valid(form)

    def form_invalid(self, form):
        proyecto = get_object_or_404(Proyecto, id=self.kwargs["pk"])
        invalid_form = super().form_invalid(form)
        titulo = form.cleaned_data.get("titulo", "")

        existe_estudio = EstudioMultipol.objects.filter(
            idProyecto=proyecto, titulo=titulo
        ).count()

        if existe_estudio > 0:
            messages.error(self.request, "Ya existe un estudio con este mismo título")
        else:
            messages.error(
                self.request, "Ingrese correctamente los datos del formulario"
            )

        return invalid_form


class UpdateEstudio(UpdateView):
    model = EstudioMultipol
    template_name = "multipol/edit_estudio.html"
    form_class = EstudioMultipolForm
    context_object_name = "estudio"

    def form_valid(self, form):
        messages.success(self.request, "El estudio se editó con éxito")
        return super().form_valid(form)

    def form_invalid(self, form):
        proyecto = get_object_or_404(Proyecto, id=self.kwargs["pk"])
        form_invalid = super().form_invalid(form)
        titulo = form.cleaned_data.get("titulo", "")
        estudio = get_object_or_404(EstudioMultipol, id=self.kwargs["pk"])
        estudios_existentes = EstudioMultipol.objects.filter(
            idProyecto=proyecto
        ).exclude(id=estudio.id)

        if estudios_existentes.filter(titulo=titulo).exists():
            messages.error(
                self.request,
                f"Ya existe un estudio Multipol registrado con el nombre {titulo}",
            )
        else:
            messages.error(
                self.request,
                "El estudio no pudo ser actualizado. Verifique los datos ingresados.",
            )
        return form_invalid


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def delete_estudio(request, *args, **kwargs):
    try:
        if request.is_ajax() and request.method == "POST":
            id = request.POST.get("id", None)
            estudio = EstudioMultipol.objects.get(pk=id)
            estudio.delete()
            return JsonResponse({"status": "Estudio eliminado con exito!"}, status=200)
    except Exception:
        return JsonResponse({"status": "Invalid request"}, status=400)
    return JsonResponse({"status": "Invalid request"}, status=400)


### Gestion de acciones del estudio ############################################################
class CreateAccion(CreateView):
    model = Accion
    form_class = AccionForm
    template_name = "multipol/acciones/add_accion.html"

    def get_context_data(self, **kwargs):
        context = super(CreateAccion, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioMultipol, id=self.kwargs["pk"])
        context["estudio"] = estudio
        # self.actualizar_informe(estudio)

        context.update(contexto_mensajes(self.request))
        return context


class ListAccion(ListView):
    model = Accion
    template_name = "multipol/acciones/accion_list.html"
    context_object_name = "acciones"

    def get_context_data(self, **kwargs):
        context = super(ListAccion, self).get_context_data(**kwargs)

        estudio = get_object_or_404(EstudioMultipol, id=self.kwargs["pk"])
        context["estudio"] = estudio
        context["acciones"] = Accion.objects.filter(estudio=estudio.id)
        print(context["acciones"])
        context.update(contexto_mensajes(self.request))
        return context


class EditAccion(UpdateView):
    model = Accion
    form_class = AccionForm
    template_name = "multipol/acciones/edit_accion.html"
    # success_url = reverse_lazy('multipol:lista_accion')

    def get_context_data(self, **kwargs):
        context = super(EditAccion, self).get_context_data(**kwargs)
        # estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk_estudio'])
        # context['estudio'] = estudio
        # self.actualizar_informe(estudio)

        context.update(contexto_mensajes(self.request))
        return context


class DeleteAccion(DeleteView):
    model = Accion
    # success_url = reverse_lazy('multipol:list_estudio')

    def post(self, request, *args, **kwargs):
        data = dict()
        if request.is_ajax():
            accion = json.loads(request.POST["content"])
            for i in accion:
                accion_delete = get_object_or_404(Accion, pk=i["id_accion"])
                accion_delete.delete()
                acciones = Accion.objects.all()
                data["html_data"] = render_to_string(
                    "multipol/includes/accion_list_table.html", {"acciones": acciones}
                )
        else:
            context = {}
            data["html_form"] = render_to_string(
                "multipol/includes/accion_confirm_delete.html", context, request=request
            )
        return JsonResponse(data)


### Gestion de criterios del estudio ############################################################


class CreateCriterio(CreateView):
    model = Criterio
    form_class = CriterioForm
    template_name = "multipol/criterios/add_criterio.html"

    def get_context_data(self, **kwargs):
        context = super(CreateCriterio, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioMultipol, id=self.kwargs["pk"])
        context["estudio"] = estudio
        # self.actualizar_informe(estudio)

        context.update(contexto_mensajes(self.request))
        return context


class ListCriterio(ListView):
    model = Criterio
    template_name = "multipol/criterios/criterio_list.html"
    context_object_name = "criterios"

    def get_context_data(self, **kwargs):
        context = super(ListCriterio, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioMultipol, id=self.kwargs["pk"])
        context["estudio"] = estudio
        context["criterios"] = Criterio.objects.filter(estudio=estudio.id)
        # self.actualizar_informe(estudio)

        context.update(contexto_mensajes(self.request))
        return context


class EditCriterio(UpdateView):
    model = Criterio
    form_class = CriterioForm
    template_name = "multipol/criterios/edit_criterio.html"

    def get_context_data(self, **kwargs):
        context = super(EditCriterio, self).get_context_data(**kwargs)
        print(self.request)
        # estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk_estudio'])
        # context['estudio'] = estudio
        # self.actualizar_informe(estudio)

        context.update(contexto_mensajes(self.request))
        return context


class DeleteCriterio(DeleteView):
    model = Criterio
    success_url = reverse_lazy("multipol:lista_criterio")

    def post(self, request, *args, **kwargs):
        data = dict()
        if request.is_ajax():
            criterio = json.loads(request.POST["content"])
            for i in criterio:
                criterio_delete = get_object_or_404(Criterio, pk=i["id_criterio"])
                criterio_delete.delete()
                criterios = Criterio.objects.all()
                data["html_data"] = render_to_string(
                    "multipol/includes/criterio_list_table.html",
                    {"criterios": criterios},
                )
        else:
            context = {}
            data["html_form"] = render_to_string(
                "multipol/includes/criterio_confirm_delete.html",
                context,
                request=request,
            )
        return JsonResponse(data)


### Gestion de políticas del estudio ############################################################


class CreatePolitica(CreateView):
    model = Politica
    form_class = PoliticaForm
    template_name = "multipol/politicas/add_politica.html"

    def get_context_data(self, **kwargs):
        context = super(CreatePolitica, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioMultipol, id=self.kwargs["pk"])
        context["estudio"] = estudio
        # self.actualizar_informe(estudio)

        context.update(contexto_mensajes(self.request))
        return context


class ListPolitica(ListView):
    model = Politica
    template_name = "multipol/politicas/politica_list.html"
    context_object_name = "politicas"

    def get_context_data(self, **kwargs):
        context = super(ListPolitica, self).get_context_data(**kwargs)
        estudio = get_object_or_404(EstudioMultipol, id=self.kwargs["pk"])
        context["estudio"] = estudio
        context["politicas"] = Politica.objects.filter(estudio=estudio.id)
        # self.actualizar_informe(estudio)

        context.update(contexto_mensajes(self.request))
        return context


class EditPolitica(UpdateView):
    model = Politica
    form_class = PoliticaForm
    template_name = "multipol/politicas/edit_politica.html"

    def get_context_data(self, **kwargs):
        context = super(EditPolitica, self).get_context_data(**kwargs)
        # estudio = get_object_or_404(EstudioMultipol, id=self.kwargs['pk'])
        # context['estudio'] = estudio
        # self.actualizar_informe(estudio)

        context.update(contexto_mensajes(self.request))
        return context


class DeletePolitica(DeleteView):
    model = Politica
    success_url = reverse_lazy("multipol:lista_politica")

    def post(self, request, *args, **kwargs):
        data = dict()
        estudio = get_object_or_404(EstudioMultipol, id=self.kwargs["pk"])
        if request.is_ajax():
            politica = json.loads(request.POST["content"])
            for i in politica:
                politica_delete = get_object_or_404(Politica, pk=i["id_politica"])
                politica_delete.delete()
                politicas = Politica.objects.all()
                data["html_data"] = render_to_string(
                    "multipol/includes/politica_list_table.html",
                    {"politicas": politicas},
                )
        else:
            context = {}
            data["html_form"] = render_to_string(
                "multipol/includes/politica_confirm_delete.html",
                context,
                request=request,
            )
        return JsonResponse(data)


###### Gestión de las evaluaciones para los resultados de estudio #####################################################


def evaluacion_criterio_accion(request, pk):
    estudio = get_object_or_404(EstudioMultipol, id=pk)
    acciones = Accion.objects.filter(estudio=estudio.id)
    criterios = Criterio.objects.filter(estudio=estudio.id)
    eval_ca = EvaluacionCriterioAccion.objects.filter(estudio=estudio.id)

    if request.method == "POST" or request.is_ajax():
        try:
            response = json.loads(request.POST["content"])
            criterio = get_object_or_404(Criterio, pk=response.get("criterio", None))
            accion = get_object_or_404(Accion, pk=response.get("accion", None))

            evaluacion, created = EvaluacionCriterioAccion.objects.get_or_create(
                criterio=criterio,
                accion=accion,
                defaults={"experto": request.user, "estudio": estudio},
            )

            evaluacion.puntuacion = response["puntuacion"]
            evaluacion.opinion = response["opinion"]
            evaluacion.save()

            message = (
                "Evaluacion actualizada satisfactoriamente."
                if not created
                else "Evaluacion creada satisfactoriamente."
            )

            return JsonResponse({"message": message})

        except Exception:
            return JsonResponse(
                data={"message": "La evaluacion al ser procesada."}, status=404
            )

    context = {
        "acciones": acciones,
        "criterios": criterios,
        "estudio": estudio,
        "evaluacion_ca": eval_ca,
    }
    return render(
        request, "multipol/evaluaciones/evaluacion_criterio_accion.html", context
    )


def evaluacion_criterio_politica(request, pk):
    estudio = get_object_or_404(EstudioMultipol, id=pk)
    politicas = Politica.objects.filter(estudio=estudio.id)
    criterios = Criterio.objects.filter(estudio=estudio.id)
    eval_cp = EvaluacionCriterioPolitica.objects.filter(estudio=estudio.id)
    # self.actualizar_informe(estudio)

    if request.method == "POST" or request.is_ajax():
        try:
            response = json.loads(request.POST["content"])
            criterio = get_object_or_404(Criterio, pk=response.get("criterio", None))
            politica = get_object_or_404(Politica, pk=response.get("politica", None))
            data = {
                **response,
                "politica": politica,
                "criterio": criterio,
                "experto": request.user,
                "estudio": estudio,
            }
            print(data)
            EvaluacionCriterioPolitica.objects.create(**data)
            return JsonResponse({"message": "Evaluacion creada satisfactoriamente."})
        except Exception as e:
            print(e)
            return JsonResponse(
                data={"message": "La evaluacion no pudo ser creada."}, status=404
            )
    for ecp in eval_cp:
        print(ecp.politica)
    context = {
        "politicas": politicas,
        "criterios": criterios,
        "estudio": estudio,
        "evaluacion_cp": eval_cp,
    }

    return render(
        request, "multipol/evaluaciones/evaluacion_criterio_politica.html", context
    )


def llenar_matriz_evaluacionCA(request, pk):
    # consenso = verificar_consenso(request, idEstudio)
    evaluacionesCA = EvaluacionCriterioAccion.objects.filter(estudio=pk).values()
    evaluacionesCA = list(evaluacionesCA)
    evaluacionesCP = EvaluacionCriterioPolitica.objects.filter(estudio=pk).values()
    evaluacionesCP = list(evaluacionesCP)
    evaluacionCA = {}
    puntuacion_total = 0

    # Este for se utiliza para calcular los valores de la relacion entre cada accion y politica
    for i in range(len(evaluacionesCA)):
        for j in range(len(evaluacionesCP)):
            puntuacion_total = puntuacion_total + evaluacionesCA[i] * (
                evaluacionesCP[j] * 100
            )

    for eca in evaluacionesCA:
        for ecp in evaluacionesCP:
            evaluacionCA["accion"]: eca.accion
            evaluacionCA["politica"]: ecp.politica

            evaluacionCA["puntuacion"]: eca.valoracion * (ecp.valoracion * 100)
    return JsonResponse({"evaluacionesCA": evaluacionesCA})
