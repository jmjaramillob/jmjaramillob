from django.contrib import admin
from apps.multipol.models import *


# Register your models here.

class EstudioMultipolAdmin(admin.ModelAdmin):
  list_display = ['id', 'titulo', 'descripcion', 'tipoTecnica', 'fecha_inicio',
                  'fecha_final', 'estado', 'dias_finalizacion_informe']
  ordering = ['titulo']

admin.site.register(EstudioMultipol, EstudioMultipolAdmin)

class AccionAdmin(admin.ModelAdmin):
  list_display = ['longNameA', 'shortNameA', 'descriptionA']
  ordering = ['longNameA']

admin.site.register(Accion, AccionAdmin)

class CriterioAdmin(admin.ModelAdmin):
  list_display = ['longNameC', 'shortNameC', 'pesoC', 'descriptionC']
  ordering = ['longNameC']

admin.site.register(Criterio, CriterioAdmin)

class PoliticaAdmin(admin.ModelAdmin):
  list_display = ['longNameP', 'shortNameP', 'pesoP', 'descriptionP']
  ordering = ['longNameP']

admin.site.register(Politica, PoliticaAdmin)

class EvaluacionCAAdmin(admin.ModelAdmin):
  list_display = ['__str__', 'criterio', 'accion', 'valoracionCA']

admin.site.register(EvaluacionCA, EvaluacionCAAdmin)

class EvaluacionCPAdmin(admin.ModelAdmin):
  list_display = ['criterio', 'politica', 'valoracionCP']

admin.site.register(EvaluacionCP, EvaluacionCPAdmin)

