from django.contrib import admin
from .models import EstudioEntrevista, Pregunta, ValorEscalaLikert, RondaJuicio, Juicio


class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_final', 'estado')
    ordering = ('titulo',)

admin.site.register(EstudioEntrevista, EstudioAdmin)


class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto_pregunta', 'idEstudio')
    ordering = ('idEstudio',)

admin.site.register(Pregunta, PreguntaAdmin)


class ValorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'valor', 'estado')
    ordering = ('valor',)

admin.site.register(ValorEscalaLikert, ValorAdmin)


class RondaJuicioAdmin(admin.ModelAdmin):
    list_display = ('idEstudio', 'numero_ronda', 'estado')
    ordering = ('idEstudio',)

admin.site.register(RondaJuicio, RondaJuicioAdmin)


class JuicioAdmin(admin.ModelAdmin):
    list_display = ('idRonda', 'texto_pregunta', 'idValorEscala')
    ordering = ('idRonda',)

admin.site.register(Juicio, JuicioAdmin)
