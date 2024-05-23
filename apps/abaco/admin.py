from django.contrib import admin
from .models import EstudioAbaco, Idea, Sesion, ValoracionIdea, Regla, Escala, OpcionEscala


class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_final', 'estado', 'tipoTecnica', 'idProyecto')
    ordering = ('titulo',)

admin.site.register(EstudioAbaco, EstudioAdmin)

# -------------------------------------------------------------------------


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'idEstudio')
    search_fields = ('titulo',)                               # Campo de busqueda
    ordering = ('fecha',)                                    # Campo de ordenamiento

admin.site.register(Idea, IdeaAdmin)

# -------------------------------------------------------------------------


class ReglaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'idEstudio')
    search_fields = ('titulo',)                               # Campo de busqueda
    ordering = ('titulo',)                                    # Campo de ordenamiento

admin.site.register(Regla, ReglaAdmin)


# -------------------------------------------------------------------------


class SesionAdmin(admin.ModelAdmin):
    list_display = ('numero_sesion', 'tipo', 'idEstudio')
    search_fields = ('idEstudio',)                               # Campo de busqueda
    ordering = ('numero_sesion', 'idEstudio',)                   # Campo de ordenamiento

admin.site.register(Sesion, SesionAdmin)

# -------------------------------------------------------------------------


class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('idIdea', 'valoracion', 'estado', 'fechaHora')
    search_fields = ('idIdea',)                               # Campo de busqueda
    ordering = ('idIdea',)                                    # Campo de ordenamiento

admin.site.register(ValoracionIdea, ValoracionAdmin)


# -------------------------------------------------------------------------


class EscalaAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)                               # Campo de busqueda
    ordering = ('nombre',)                                    # Campo de ordenamiento

admin.site.register(Escala, EscalaAdmin)


# -------------------------------------------------------------------------


class OpcionEscalaAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'abreviacion', 'idEscala')
    search_fields = ('nombre',)                               # Campo de busqueda
    ordering = ('idEscala', 'nombre',)                                    # Campo de ordenamiento

admin.site.register(OpcionEscala, OpcionEscalaAdmin)



