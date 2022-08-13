from django.shortcuts import render
from apps.delphi.forms import DelphiForm, CuestionarioForm, RondasForm
from apps.delphi.models import Delphi, Cuestionario, RondasDelphi
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
# Create your views here.

class Nuevo_estudio_Delphi(CreateView):
    form_class = DelphiForm
    template_name = 'addDelphi.html'
    success_url = reverse_lazy('delphi:estudios_delphi')


class ListaDelphi(ListView):
    model = Delphi
    template_name = 'listaEstudios.html'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        total_delphis = self.model.objects.count()
        kwargs.update({'total_delphis': total_delphis})
        return super().get_context_data(**kwargs)


class EditarDelphi(UpdateView):
    model = Delphi
    form_class = DelphiForm
    template_name = 'addDelphi.html'
    success_url = reverse_lazy('delphi:estudios_delphi')


class EditarRonda(UpdateView):
    model = RondasDelphi
    form_class = RondasForm
    template_name = 'rondasDelphi.html'
    success_url = reverse_lazy('delphi:estudios_delphi')


class EditarCuestionario(UpdateView):
    model = Cuestionario
    form_class = CuestionarioForm
    template_name = 'cuestionarioDelphi.html'
    success_url = reverse_lazy('delphi:estudios_delphi')




class DetalleEstudio(DetailView):
    model = Delphi
    template_name = 'detalleEstudio.html'
    success_url = reverse_lazy('delphi:estudios_delphi')

    def get_context_data(self, **kwargs):
        cuetionarios = Cuestionario.objects.filter(delphi=self.object)
        kwargs.update({'cuestionarios': cuetionarios})
        return super(DetalleEstudio, self).get_context_data(**kwargs)


class CrearRonda(CreateView):
    model = RondasDelphi
    template_name = 'rondasDelphi.html'
    form_class = RondasForm
    success_url = reverse_lazy('delphi:estudios_delphi')

    def get_context_data(self, **kwargs):
        cuestionario = Cuestionario.objects.get(pk=self.kwargs.get('pk'))
        kwargs.update({'cuestionario': cuestionario})
        return super(CrearRonda, self).get_context_data(**kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.cuestionario = Cuestionario.objects.get(pk=self.kwargs.get('pk'))
        return super(CrearRonda, self).form_valid(form=form)


class Crear_Cuestionario(CreateView):
    model = Cuestionario
    template_name = 'cuestionarioDelphi.html'
    form_class = CuestionarioForm
    success_url = reverse_lazy('delphi:estudios_delphi')

    def get_context_data(self, **kwargs):
        delphi = Delphi.objects.get(pk=self.kwargs.get('pk'))
        kwargs.update({'delphi': delphi})
        return super(Crear_Cuestionario, self).get_context_data(**kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.delphi = Delphi.objects.get(pk=self.kwargs.get('pk'))
        return super(Crear_Cuestionario, self).form_valid(form=form)


class DetalleCuestionario(DetailView):
    model = Cuestionario
    template_name = 'detalleCuestionario.html'

    def get_context_data(self, **kwargs):
        ronda = RondasDelphi.objects.filter(cuestionario=self.object)
        kwargs.update({'ronda': ronda})
        return super(DetalleCuestionario, self).get_context_data(**kwargs)