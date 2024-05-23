from django.contrib import admin
from .models import Proyecto, FaseProspectiva, Tecnica, Mensaje


class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_inicio', 'fecha_final', 'estado']
    ordering = ('nombre',)

admin.site.register(Proyecto, ProyectoAdmin)


class MensajeAdmin(admin.ModelAdmin):
    list_display = ('fechaHora', 'idEmisor', 'mensaje', 'tipoEstudio', 'multiples', 'hijoMultiple', 'estado')
    ordering = ('-fechaHora',)

admin.site.register(Mensaje, MensajeAdmin)


class FaseAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    ordering = ('nombre',)

admin.site.register(FaseProspectiva, FaseAdmin)


class TecnicaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    ordering = ('nombre',)

admin.site.register(Tecnica, TecnicaAdmin)
