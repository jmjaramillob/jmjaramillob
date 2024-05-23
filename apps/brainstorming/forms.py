from django import forms
from apps.brainstorming.models import EstudioLluviaDeIdeas

class FormEstudio(forms.ModelForm):

  def clean_titulo(self):
    mensaje = self.cleaned_data["titulo"].upper()
    return mensaje

  def clean_idExpertos(self):
    cantidad = self.cleaned_data["idExpertos"]
    if len(cantidad) > 10:
      raise forms.ValidationError(
        "Seleccione máximo 10 expertos para el estudio.")
    return cantidad

  def clean_fecha_final(self):

    fecha_inicio = self.cleaned_data["fecha_inicio"]
    fecha_final = self.cleaned_data["fecha_final"]

    if fecha_final < fecha_inicio:
      raise forms.ValidationError(
        "La fecha final debe ser posterior o igual a la fecha de inicio")
    return fecha_final

  class Meta:
    model = EstudioLluviaDeIdeas

    fields = [
      'tipoTecnica',
      'titulo',
      'idCoordinador',
      'idExpertos',
      'fecha_inicio',
      'fecha_final',
      'estado',
      'idProyecto'
    ]

    labels = {
      'titulo': 'Título',
    }

    widgets = {
      'tipoTecnica': forms.TextInput(attrs={'class': 'form-control'}),
      'titulo': forms.TextInput(attrs={'class': 'form-control'}),
      'idCoordinador': forms.Select(attrs={'class': 'form-control'}),
      'idExpertos': forms.SelectMultiple(
        attrs={'class': 'form-control select2'}),
      'fecha_inicio': forms.DateInput(attrs={'class': 'form-control'}),
      'fecha_final': forms.DateInput(attrs={'class': 'form-control'}, ),
      'estado': forms.CheckboxInput(),
      'idProyecto': forms.Select(attrs={'class': 'form-control'}),
    }
