from django.contrib import admin
from .models import EstudioLluviaDeIdeas, Idea, ValoracionIdea, Regla


class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_final', 'estado', 'tipoTecnica', 'idProyecto')
    ordering = ('titulo',)

admin.site.register(EstudioLluviaDeIdeas, EstudioAdmin)

