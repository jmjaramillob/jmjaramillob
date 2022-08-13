from django.contrib.auth.models import User
from registration.forms import RegistrationForm


# Form para el registro de usuarios (agregando campos de nombre y apellido al formulario de registration redux)

class UserRegistrationForm(RegistrationForm):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

