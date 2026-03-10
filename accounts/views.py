from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreationForm

# Create your views here.
class RegisterView(SuccessMessageMixin, CreateView):
    User = get_user_model()
    model = User
    form_class = UserCreationForm
    success_message = "Se ha registrado exitosamente."
    success_url = reverse_lazy(settings.LOGIN_URL)
    template_name = "accounts/register.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
