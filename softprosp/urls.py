"""softprosp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from apps.usuario.views import UserRegistrationView

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  # sobreescritura del formulario de registro de registration-redux
  url(r'^accounts/register/$', UserRegistrationView.as_view(),
      name='registration_register'),
  url(r'^proyecto/', include('apps.proyecto.urls', namespace="proyecto")),
  url(r'^usuario/', include('apps.usuario.urls', namespace="usuario")),
  url(r'^abaco/', include('apps.abaco.urls', namespace="abaco")),
  url(r'^delphi/', include('apps.delphi.urls', namespace="delphi")),
  url(r'^entrevista/', include('apps.entrevista.urls', namespace="entrevista")),
  url(r'^brainstorming/',
      include('apps.brainstorming.urls', namespace="brainstorming")),
  url(r'^mactor/', include('apps.mactor.urls', namespace="mactor")),
  url(r'^multipol/', include('apps.multipol.urls', namespace='multipol')),
  url(r'^extrapolacion', include('apps.extrapolacion_tendencias.urls',
                                 namespace='extrapolacion')),
  # urls vista control de usuarios paquete Registration redux
  url(r'^accounts/', include('registration.backends.default.urls')),
]
