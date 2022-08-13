from django import forms
from .models import EstudioAbaco, Idea, Regla, ValoracionIdea, Sesion

"""FORMULARIO ESTUDIO ABACO DE REGNIER--------------------------------------------------------------------"""


class FormEstudio(forms.ModelForm):

    def clean_titulo(self):
        mensaje = self.cleaned_data["titulo"].upper()
        return mensaje

    def clean_fecha_final(self):

        fecha_inicio = self.cleaned_data["fecha_inicio"]
        fecha_final = self.cleaned_data["fecha_final"]

        if fecha_final < fecha_inicio:
            raise forms.ValidationError("La fecha final debe ser posterior o igual a la fecha de inicio")
        return fecha_final

    class Meta:
        model = EstudioAbaco

        fields = [
            'tipoTecnica',
            'titulo',
            'tematica',
            'idCoordinadores',
            'idExpertos',
            'fecha_inicio',
            'fecha_final',
            'idEscala',
            'estado',
            'idProyecto'
        ]

        labels = {
            'titulo': 'Título',
            'tematica': 'Temática',
            'idEscala': 'Escala',
        }

        widgets = {
            'tipoTecnica': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tematica': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idCoordinadores': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'idExpertos': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control'}, ),
            'idEscala': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(),
            'estadoValoraciones': forms.CheckboxInput(),
            'idProyecto': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO SESIONES----------------------------------------------------------------------------------------------"""


class FormSesion(forms.ModelForm):

    def clean_fecha_final(self):

        fecha_inicio = self.cleaned_data["fecha_inicio"]
        fecha_final = self.cleaned_data["fecha_final"]

        if fecha_final < fecha_inicio:
            raise forms.ValidationError("La fecha final debe ser posterior o igual a la fecha de inicio")
        return fecha_final

    class Meta:
        model = Sesion

        fields = [
            'numero_sesion',
            'tipo',
            'descripcion',
            'fecha_inicio',
            'fecha_final',
            'estado',
            'idEstudio',
        ]

        labels = {
            'descripcion': 'Descripción',
        }

        widgets = {
            'numero_sesion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO IDEA----------------------------------------------------------------------------------------------"""


class FormIdea(forms.ModelForm):

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].upper()
        return titulo

    class Meta:
        model = Idea

        fields = [
            'titulo',
            'descripcion',
            'idCreador',
            'estado',
            'idEstudio',
        ]

        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idCreador': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO REGLA----------------------------------------------------------------------------------------------"""


class FormRegla(forms.ModelForm):

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].upper()
        return titulo

    class Meta:
        model = Regla

        fields = [
            'titulo',
            'descripcion',
            'estado',
            'idEstudio',
        ]

        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'estado': forms.CheckboxInput(),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }



"""FORMULARIO VALORACION IDEA----------------------------------------------------------------------------------------"""


class FormValoracion(forms.ModelForm):

    class Meta:
        model = ValoracionIdea

        fields = [
            'idIdea',
            'valoracion',
            'justificacion',
            'idExperto',
        ]

        labels = {
            'idIdea': 'Idea',
            'valoracion': 'Valoración',
            'justificacion': 'Justificación',
        }

        widgets = {
            'idIdea': forms.Select(attrs={'class': 'form-control'}),
            'valoracion': forms.Select(attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idExperto': forms.Select(attrs={'class': 'form-control'}),
        }
#
