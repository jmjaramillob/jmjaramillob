# coding: utf-8
from apps.delphi.models import Delphi, RondasDelphi, Cuestionario
from django import forms


class DelphiForm(forms.ModelForm):
    class Meta:
        model = Delphi
        fields = (
            'proyecto',
            'titulo',
            'descripcion',
            'objetivos',
            'expertos',
            'coordinadores',
            'fecha_inicio',
            'fecha_final',
            'estado',
            'slug',
        )
        labels = {
            'proyecto': 'Proyecto',
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'objetivos': 'Objetivos',
            'expertos': 'Expertos',
            'coordinadores': 'Coordinadores',
            'fecha_inicio': 'Fecha Inicio',
            'fecha_final': 'Fecha Final',
            'estado': 'Abierto',
            'slug': 'slug',

        }
        widgets = {
            'proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                 'placeholder': 'Ingrese aquí una descripción del estudio'}),
            'objetivos': forms.Textarea(attrs={'class': 'form-control', 'rows': '3',
                                               'placeholder': 'Ingresar los objetivos iniciales del estudio'}),
            'expertos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'coordinadores': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepiker'}),
            'fecha_final': forms.DateInput(attrs={'class': 'datepiker'}),
            'abierto': forms.CheckboxInput(),

        }


class CuestionarioForm(forms.ModelForm):
    class Meta:
        model = Cuestionario
        fields = ('nombre', 'estado', 'delphi', 'expertos', 'coordinadores',)
        labels = {
            'nombre': 'Nombre',
            'estado': 'Estado',
            'delphi': 'Estudio',
            'expertos': 'Expertos',
            'coordinadores': 'Coordinadores',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(),
            #'delphi': forms.TextInput(attrs={'class': 'form-control'}),
            'expertos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'coordinadores': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class RondasForm(forms.ModelForm):
    class Meta:
        model = RondasDelphi
        fields = (
            'delphi',
            'numero',
            'cuestionario',
            'abierto',
            'expertos',
            'coordinadores',
            'fecha_inicio',
            'fecha_final',

        )
        labels = {
            'delphi': 'Estudio',
            'numero': 'Número',
            'cuestionario': 'Cuestionario',
            'abierto': 'Abierto',
            'expertos': 'Expertos',
            'coordinadores': 'Coordinadores',
            'fecha_inicio': 'Fecha Inicio',
            'fecha_final': 'Fecha Final',

        }
        widgets = {
            'delphi': forms.TextInput(attrs={'class': 'form-control'}),
            'nuemro': forms.IntegerField(),
            'cuestionario': forms.Select(attrs={'class': 'form-control'}),
            'abierto': forms.CheckboxInput(),
            'expertos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'coordinadores': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control'}),

        }
