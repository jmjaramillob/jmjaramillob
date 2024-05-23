from django import forms
from .models import Proyecto, Mensaje

# FORMULARIO PROYECTO PROSPECTIVO------------------------------------------------------------------------


class FormProyecto(forms.ModelForm):

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].upper()
        return nombre

    def clean_fecha_final(self):

        fecha_inicio = self.cleaned_data["fecha_inicio"]
        fecha_final = self.cleaned_data["fecha_final"]

        if fecha_final < fecha_inicio:
            raise forms.ValidationError("La fecha final debe ser posterior o igual a la fecha de inicio")
        return fecha_final

    class Meta:
        model = Proyecto

        fields = [
            'nombre',
            'objetivo',
            'idAdministrador',
            'idCoordinadores',
            'idExpertos',
            'fecha_inicio',
            'fecha_final',
            'estado'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivo': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idAdministrador': forms.Select(attrs={'class': 'form-control'}),
            'idCoordinadores': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'idExpertos': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control'}, ),
            'estado': forms.CheckboxInput()
        }


# FORMULARIO NOTIFICACIONES------------------------------------------------------------------------"""


class FormNotificacion(forms.ModelForm):

    class Meta:
        model = Mensaje
        exclude = ['fecha']

        fields = [
            'idDestinatarios',
            'mensaje',
            'estado'
        ]

        widgets = {
            'idDestinatarios': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'estado': forms.CheckboxInput()
        }
