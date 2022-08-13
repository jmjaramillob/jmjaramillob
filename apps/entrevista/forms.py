from django import forms
from .models import EstudioEntrevista, Pregunta, ValorEscalaLikert, RondaJuicio, Juicio


"""FORMULARIO ESTUDIO ENTREVISTA------------------------------------------------------------------------------------"""


class FormEstudioE(forms.ModelForm):

    def clean_titulo(self):
        mensaje = self.cleaned_data["titulo"].upper()
        return mensaje

    def clean_idExpertos(self):

        expertos = self.cleaned_data["idExpertos"]

        if self.cleaned_data["idCoordinador"] in expertos or self.cleaned_data["idAdministrador"] in expertos:
            raise forms.ValidationError("El administrador y el coordinador no pueden hacer parte del grupo de expertos")
        if len(expertos) < 2:
            raise forms.ValidationError("Debe registrar mínimo 2 expertos")
        return expertos

    def clean_fecha_final(self):

        fecha_inicio = self.cleaned_data["fecha_inicio"]
        fecha_final = self.cleaned_data["fecha_final"]

        if fecha_final < fecha_inicio:
            raise forms.ValidationError("La fecha final de la ronda debe ser posterior o igual a la fecha de inicio")
        return fecha_final

    class Meta:
        model = EstudioEntrevista

        fields = [
            'tipoTecnica',
            'titulo',
            'objetivo',
            'entrevistador',
            'entrevistado',
            'idAdministrador',
            'idCoordinador',
            'idExpertos',
            'fecha_inicio',
            'fecha_final',
            'estado',
            'idProyecto',
        ]

        labels = {
            'titulo': 'Título',
        }

        widgets = {
            'tipoTecnica': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'entrevistador': forms.TextInput(attrs={'class': 'form-control'}),
            'entrevistado': forms.TextInput(attrs={'class': 'form-control'}),
            'idAdministrador': forms.Select(attrs={'class': 'form-control'}),
            'idCoordinador': forms.Select(attrs={'class': 'form-control select2'}),
            'idExpertos': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(),
            'idProyecto': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO PREGUNTA----------------------------------------------------------------------------------------------"""


class FormPregunta(forms.ModelForm):

    class Meta:
        model = Pregunta

        fields = [
            'texto_pregunta',
            'texto_respuesta',
            'observacion',
            'estado',
            'idEstudio',
        ]

        labels = {
            'texto_pregunta': 'Enunciado de la pregunta',
            'texto_respuesta': 'Respuesta esperada',
            'observacion': 'Observación',
        }

        widgets = {
            'texto_pregunta': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'texto_respuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'estado': forms.CheckboxInput(),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO ESCALA------------------------------------------------------------------------------------------------"""


class FormValorEscala(forms.ModelForm):

    class Meta:
        model = ValorEscalaLikert

        fields = [
            'nombre',
            'valor',
            'estado',
            'descripcion',
            'idEstudio',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO RONDAS----------------------------------------------------------------------------------------------"""


class FormRonda(forms.ModelForm):

    def clean_fecha_final(self):

        fecha_inicio = self.cleaned_data["fecha_inicio"]
        fecha_final = self.cleaned_data["fecha_final"]

        if fecha_final < fecha_inicio:
            raise forms.ValidationError("La fecha final de la ronda debe ser posterior o igual a la fecha de inicio")
        return fecha_final

    class Meta:
        model = RondaJuicio

        fields = [
            'numero_ronda',
            'descripcion',
            'fecha_inicio',
            'fecha_final',
            'numero_preguntas',
            'estado',
            'idEstudio',
        ]

        labels = {
            'descripcion': 'Descripción',
        }

        widgets = {
            'numero_ronda': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control'}),
            'numero_preguntas': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO JUICIO---------------------------------------------------------------------------------------------"""


class FormJuicio(forms.ModelForm):

    class Meta:
        model = Juicio

        fields = [
            'texto_pregunta',
            'idValorEscala',
            'justificacion',
            'idExperto',
            'idRonda',
            ]

        widgets = {
            'texto_pregunta': forms.Select(attrs={'class': 'form-control'}),
            'idValorEscala': forms.Select(attrs={'class': 'form-control'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'idExperto': forms.Select(attrs={'class': 'regDropDown'}),
            'idRonda': forms.Select(attrs={'class': 'form-control'}),
            }