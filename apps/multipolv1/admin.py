from django.contrib import admin

from apps.multipolv1.models import EstudioMultipol, Accion, Criterio, Politica, EvaluacionCriterioAccion, EvaluacionCriterioPolitica

# Register your models here.

admin.site.register(EstudioMultipol)
admin.site.register(Accion)
admin.site.register(Criterio)
admin.site.register(Politica)
admin.site.register(EvaluacionCriterioAccion)
admin.site.register(EvaluacionCriterioPolitica)
