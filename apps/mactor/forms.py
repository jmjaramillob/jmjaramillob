from django import forms
from .models import EstudioMactor, Actor, Objetivo, Ficha, RelacionMID, RelacionMAO, InformeFinal
from .choices import VALORES_MID, VALORES_2MAO


"""FORMULARIO ESTUDIO MACTOR------------------------------------------------------------------------------------"""


class FormEstudio(forms.ModelForm):

    def clean_titulo(self):
        mensaje = self.cleaned_data["titulo"].upper()
        return mensaje

    def clean_idExpertos(self):
        cantidad = self.cleaned_data["idExpertos"]
        if len(cantidad) > 10:
            raise forms.ValidationError("Seleccione máximo 10 expertos para el estudio.")
        return cantidad

    def clean_fecha_final(self):

        fecha_inicio = self.cleaned_data["fecha_inicio"]
        fecha_final = self.cleaned_data["fecha_final"]

        if fecha_final < fecha_inicio:
            raise forms.ValidationError("La fecha final debe ser posterior o igual a la fecha de inicio")
        return fecha_final

    class Meta:
        model = EstudioMactor

        fields = [
            'tipoTecnica',
            'titulo',
            'descripcion',
            'idCoordinador',
            'idExpertos',
            'fecha_inicio',
            'fecha_final',
            'dias_finalizacion_informe',
            'estado',
            'idProyecto'
        ]

        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'dias_finalizacion_informe': 'Dias adicionales para redacción del informe final'
        }

        widgets = {
            'tipoTecnica': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idCoordinador': forms.Select(attrs={'class': 'form-control'}),
            'idExpertos': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control'}, ),
            'dias_finalizacion_informe': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(),
            'idProyecto': forms.Select(attrs={'class': 'form-control'}),
        }

"""FORMULARIO ACTOR----------------------------------------------------------------------------------------------"""


class FormActor(forms.ModelForm):

    def clean_nombreLargo(self):
        nombreLargo = self.cleaned_data["nombreLargo"].upper()
        return nombreLargo

    def clean_nombreCorto(self):
        nombreCorto = self.cleaned_data["nombreCorto"].upper()
        return nombreCorto

    class Meta:
        model = Actor

        fields = [
            'nombreLargo',
            'nombreCorto',
            'descripcion',
            'idEstudio', # en este caso no se elimina para que se muestren los errores de duplicidad de los nombres
        ]

        labels = {
            'nombreLargo': 'Nombre Largo',
            'nombreCorto': 'Nombre Corto',
            'descripcion': 'Descripción',
        }

        widgets = {
            'nombreLargo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'nombreCorto': forms.TextInput(attrs={'class': 'form-control'}, ),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }

"""FORMULARIO OBJETIVO------------------------------------------------------------------------------------------"""


class FormObjetivo(forms.ModelForm):

    def clean_nombreLargo(self):
        nombreLargo = self.cleaned_data["nombreLargo"].upper()
        return nombreLargo

    def clean_nombreCorto(self):
        nombreCorto = self.cleaned_data["nombreCorto"].upper()
        return nombreCorto

    class Meta:
        model = Objetivo

        fields = [
            'nombreLargo',
            'nombreCorto',
            'descripcion',
            'idEstudio',
        ]

        labels = {
            'nombreLargo': 'Nombre Largo',
            'nombreCorto': 'Nombre Corto',
            'descripcion': 'Descripción',
        }

        widgets = {
            'nombreLargo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'nombreCorto': forms.TextInput(attrs={'class': 'form-control'}, ),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO FICHA DEL ACTOR------------------------------------------------------------------------------------"""


class FormFicha(forms.ModelForm):

    class Meta:
        model = Ficha

        fields = [
            'idActorX',
            'idActorY',
            'estrategia',
        ]

        widgets = {
            'idActorX': forms.Select(attrs={'class': 'form-control'}),
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'estrategia': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }

"""FORMULARIO DE INFLUENCIAS------------------------------------------------------------------------------------"""


class FormMID(forms.ModelForm):

    class Meta:
        model = RelacionMID

        fields = [
            'idActorY',
            'idActorX',
            'valor',
            'justificacion',
            'idExperto',
        ]

        widgets = {
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'idActorX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES_MID, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idExperto': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO 2MAO----------------------------------------------------------------------------------------------"""


class Form2mao(forms.ModelForm):

    class Meta:
        model = RelacionMAO

        fields = [
            'tipo',
            'idActorY',
            'idObjetivoX',
            'valor',
            'justificacion',
            'idExperto',
            ]

        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'idObjetivoX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES_2MAO, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idExperto': forms.Select(attrs={'class': 'form-control'}),
            }

"""FORMULARIO INFORME FINAL-------------------------------------------------------------------------------------"""


class FormInforme(forms.ModelForm):

    class Meta:
        model = InformeFinal

        fields = [
            'informe',
            'estado',
            'idEstudio',
        ]

        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control'}, ),
            'informe': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }
