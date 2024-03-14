from django import forms
from apps.multipolv1.models import Accion, Criterio, Politica, EvaluacionCriterioPolitica, EvaluacionCriterioAccion, EstudioMultipol

class EstudioMultipolForm(forms.ModelForm):

  def clean_titulo(self):
    clean_titulo = self.cleaned_data['titulo'].upper()
    return clean_titulo

  def clean_idExpertos(self):
    expertos = self.cleaned_data['idExpertos']
    if len(expertos) > 10:
      raise forms.ValidationError("Seleccione máximo 10 expertos para el estudio.")
    return expertos

  def clean_fecha_final(self):
    fecha_inicio = self.cleaned_data['fecha_inicio']
    fecha_final = self.cleaned_data['fecha_final']

    if fecha_final < fecha_inicio:
      raise forms.ValidationError('Seleccione una fecha final correcta')
    return fecha_final

  class Meta:
    model = EstudioMultipol

    fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_final', 'idProyecto',
              'idCoordinador', 'idExpertos', 'estado', 'tipoTecnica', 'dias_finalizacion_informe']
    labels = {
      'titulo': 'Título del estudio',
      'descripcion': 'Descripción del estudio',
      'idCoordinador': 'Coordinador',
      'idExpertos': 'Expertos'
    }
    widgets = {
      'tipoTecnica': forms.TextInput(attrs={
        'class': 'form-control'
      }),
      'titulo': forms.TextInput(attrs={
        'class': 'form-control'
      }),
      'descripcion': forms.Textarea(attrs={
        'class': 'form-control'
      }),
      'idProyecto': forms.TextInput(attrs={
        'class': 'form-control',
      }),
      'idCoordinador': forms.Select(attrs={
        'class': 'form-control'
      }),
      'fecha_inicio': forms.DateInput(attrs={
        'class': 'form-control',
        'id': 'id_fecha_inicio'
      }),
      'fecha_final': forms.DateInput(attrs={
        'class': 'form-control',
        'id': 'id_fecha_final'
      }),
      'idExpertos': forms.SelectMultiple(attrs={
        'class': 'form-control select2'
      }),
      'dias_finalizacion_informe': forms.TextInput(attrs={
        'class': 'form-control'
      }),
      'Estado': forms.CheckboxInput()

    }


class AccionForm(forms.ModelForm):


  class Meta:
    model = Accion
    fields = ['estudio', 'short_name', 'long_name', 'description']

    labels = {
      'estudio': '',
      'short_name': 'Nombre Corto',
      'long_name': 'Nombre Largo',
      'description': 'Descripción'
    }

    widgets = {
      'estudio': forms.TextInput(attrs={
        'class': 'form-control hidden',
      }),
      'short_name': forms.TextInput(attrs={
        'class': 'form-control'
      }),
      'long_name': forms.TextInput(attrs={
        'class': 'form-control'
      }),
      'description': forms.Textarea(attrs={
        'class': 'form-control'
      })
    }



class CriterioForm(forms.ModelForm):


  class Meta:
    model = Criterio
    fields = ['estudio', 'short_name', 'long_name', 'peso', 'description']

    labels = {
    'estudio': '',
    'short_name': 'Nombre Corto',
    'long_name': 'Nombre Largo',
    'peso': 'Peso',
    'description': 'Descripción'
    }

    widgets = {
    'estudio': forms.TextInput(attrs={
      'class': 'form-control hidden',
    }),
    'short_name': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'long_name': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'peso': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'description': forms.Textarea(attrs={
      'class': 'form-control'
    })
    }


class PoliticaForm(forms.ModelForm):


  class Meta:
    model = Politica
    fields = ['estudio', 'short_name', 'long_name', 'peso', 'description']

    labels = {
    'estudio': '',
    'short_name': 'Nombre Corto',
    'long_name': 'Nombre Largo',
    'peso': 'Peso',
    'description': 'Descripción'
    }

    widgets = {
    'estudio': forms.TextInput(attrs={
      'class': 'form-control hidden',
    }),
    'short_name': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'long_name': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'peso': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'description': forms.Textarea(attrs={
      'class': 'form-control'
    })
    }