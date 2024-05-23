from django.contrib.auth.models import User
from ..proyecto.models import Proyecto
from ..mactor.models import EstudioMactor
from ..entrevista.models import EstudioEntrevista
from ..abaco.models import EstudioAbaco
from ..brainstorming.models import EstudioLluviaDeIdeas
from ..multipolv1.models import EstudioMultipol
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404

from registration.backends.default.views import RegistrationView
from django.contrib.sites.shortcuts import get_current_site
from registration.models import RegistrationProfile
from registration import signals

# ------ REGISTRO DE USUARIOS DESDE FUERA DE LA PLATAFORMA


class UserRegistrationView(RegistrationView):

    form_class = UserRegistrationForm

    def register(self, form):

        site = get_current_site(self.request)

        if hasattr(form, 'save'):
            new_user_instance = form.save()
        else:
            new_user_instance = (User().objects
                                 .create_user(**form.cleaned_data))

        new_user = RegistrationProfile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=self.request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user


# ------REGISTRO DE USUARIOS DESDE DENTRO DE LA PLATAFORMA

# Registrar un usuario desde la vista de proyectos


class RegistrarUsuarioProyecto(CreateView):
    model = User
    template_name = "usuario/registrar_usuario_proyecto.html"
    form_class = UserRegistrationForm

    def get_context_data(self, **kwargs):
        context = super(RegistrarUsuarioProyecto, self).get_context_data(**kwargs)
        print(self.kwargs['id']) # 0 - idProyecto
        context['idProyecto'] = self.kwargs['id']
        return context

    def form_valid(self, form):
        # form.instance.idAdministrador = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Usuario registrado.')
        #  self.send_emails(form)
        return super(RegistrarUsuarioProyecto, self).form_valid(form)

    def form_invalid(self, form):
        response = super(RegistrarUsuarioProyecto, self).form_invalid(form)
        messages.error(self.request, 'El usuario no pudo ser registrado. Verifique los datos ingresados.')
        return response

    def get_success_url(self):
        return reverse('usuario:registrar_usuario_proyecto', kwargs={'id': self.kwargs['id']})


class RegistrarUsuarioEstudio(CreateView):

    model = User
    template_name = "usuario/registrar_usuario_proyecto.html"
    form_class = UserRegistrationForm

    def get_context_data(self, **kwargs):
        context = super(RegistrarUsuarioEstudio, self).get_context_data(**kwargs)
        # print(self.kwargs['idProyecto']) # proyecto - estudio
        # print(self.kwargs['tipoEstudio']) # mactor - entrevista
        # print(self.kwargs['idEstudio']) # 0 - idEstudio

        estudio = self.kwargs['idEstudio']
        tipoEstudio = int(self.kwargs['tipoEstudio'])
        if estudio != '0':
            if tipoEstudio == 1 :
                estudio = get_object_or_404(EstudioMactor, id=int(estudio))
            elif tipoEstudio == 2:
                estudio = get_object_or_404(EstudioEntrevista, id=int(estudio))
            elif tipoEstudio == 3:
                estudio = get_object_or_404(EstudioAbaco, id=int(estudio))
            elif tipoEstudio == 4:
                estudio = get_object_or_404(EstudioLluviaDeIdeas, id=int(estudio))
            elif tipoEstudio == 5:
                estudio = get_object_or_404(EstudioMultipol, id=int(estudio))

        context['proyecto'] = get_object_or_404(Proyecto, id=int(self.kwargs['idProyecto']))
        context['idEstudio'] = estudio
        context['tipo'] = tipoEstudio
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Usuario registrado.')
        return super(RegistrarUsuarioEstudio, self).form_valid(form)

    def form_invalid(self, form):
        response = super(RegistrarUsuarioEstudio, self).form_invalid(form)
        messages.error(self.request, 'El usuario no pudo ser registrado. Verifique los datos ingresados.')
        return response

    def get_success_url(self):
        return reverse('usuario:registrar_usuario_estudio', kwargs={'idProyecto': self.kwargs['idProyecto'],
                                                                    'tipoEstudio': int(self.kwargs['tipoEstudio']),
                                                                    'idEstudio': self.kwargs['idEstudio']})
