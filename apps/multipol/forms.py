from django import forms
from apps.multipol.models import Accion, Criterio, Politica, \
  EvaluacionCP, EvaluacionCA, EstudioMultipol

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
  # shortNameA = forms.CharField(max_length=10, label="Nombre Corto Acción", widget=forms.TextInput(attrs={'class': 'form-control'}))
  # longNameA = forms.CharField(max_length=50, label="Nombre Largo Acción", widget=forms.TextInput(attrs={'class': 'form-control'}))
  # descriptionA = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Descripción de Acción")

  class Meta:
    model = Accion
    fields = ['estudio', 'shortNameA', 'longNameA', 'descriptionA']

    labels = {
      'estudio': '',
      'shortNameA': 'Nombre Corto',
      'longNameA': 'Nombre Largo',
      'descriptionA': 'Descripción'
    }

    widgets = {
      'estudio': forms.TextInput(attrs={
        'class': 'form-control hidden',
      }),
      'shortNameA': forms.TextInput(attrs={
        'class': 'form-control'
      }),
      'longNameA': forms.TextInput(attrs={
        'class': 'form-control'
      }),
      'descriptionA': forms.Textarea(attrs={
        'class': 'form-control'
      })
    }


class CriterioForm(forms.ModelForm):
  '''
  shortNameC = forms.CharField(max_length=10, label="Nombre Corto Criterio")
  longNameC = forms.CharField(max_length=50)
  pesoC = forms.IntegerField(widget=forms.CharField())
  descriptionC = forms.CharField(widget=forms.Textarea())
  '''

  class Meta:
    model = Criterio
    fields = ['estudio', 'shortNameC', 'longNameC', 'pesoC', 'descriptionC']

  labels = {
    'estudio': '',
    'shortNameC': 'Nombre Corto',
    'longNameC': 'Nombre Largo',
    'descriptionC': 'Descripción'
  }

  widgets = {
    'estudio': forms.TextInput(attrs={
      'class': 'form-control hidden',
    }),
    'shortNameC': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'longNameC': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'descriptionC': forms.Textarea(attrs={
      'class': 'form-control'
    })
  }


class PoliticaForm(forms.ModelForm):
  '''
  shortNameP = forms.CharField(max_length=10, label="Nombre Corto Política")
  longNameP = forms.CharField(max_length=50)
  pesoP = forms.IntegerField(widget=forms.TextInput())
  descriptionP = forms.CharField(widget=forms.Textarea())
  '''

  class Meta:
    model = Politica
    fields = ['estudio', 'shortNameP', 'longNameP', 'pesoP', 'descriptionP']

  labels = {
    'estudio': '',
    'shortNameP': 'Nombre Corto',
    'longNameP': 'Nombre Largo',
    'descriptionP': 'Descripción'
  }

  widgets = {
    'estudio': forms.TextInput(attrs={
      'class': 'form-control hide',
    }),
    'shortNameP': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'longNameP': forms.TextInput(attrs={
      'class': 'form-control'
    }),
    'descriptionP': forms.Textarea(attrs={
      'class': 'form-control'
    })
  }


class EvaluacionCAForm(forms.ModelForm):
  class Meta:
    model = EvaluacionCA
    fields = ('estudio', 'accion', 'criterio' ,'valoracionCA',)


class EvaluacionCPForm(forms.ModelForm):
  valoracionCP = forms.IntegerField()

  class Meta:
    model = EvaluacionCP
    fields = ('estudio', 'criterio', 'politica', 'valoracionCP',)

  # def __init__(self, *args, **kwargs):
  #   super(EstudioMultipolForm, self).__init__(*args, **kwargs)
  #   self.fields['fecha_fin'].widget.attrs.update({'id': 'datepicker_fin'})
  #   self.fields['fecha_inicio'].widget.attrs.update({'id': 'datepicker_inicio'})
  #   for field in iter(self.fields):
  #     self.fields[field].widget.attrs.update({
  #       'class': 'form-control'
  #     })

