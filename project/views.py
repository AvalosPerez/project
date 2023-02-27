from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render

# Create your views here.
from django.views import View

from administracion.models import Modulo
from project.funciones import enviar_correo


class Index(LoginRequiredMixin, View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        context = {}
        # action = request.GET['action']
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = {}
        # action = request.POST['action']
        pass

class MyLoginView(LoginView):

    def form_valid(self, form):

        User = get_user_model()
        username = form.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            email = user.email
        except User.DoesNotExist:
            email = None


        # Realiza cualquier operación adicional que desees antes de que el usuario inicie sesión


        # Llama al método form_valid de la superclase, que realiza la autenticación de usuario y redirige al usuario a la página de inicio
        response = super().form_valid(form)

        # Realiza cualquier operación adicional que desees después de que el usuario haya iniciado sesión
        # ...

        asunto = 'Login exitoso'
        plantilla = 'emails_template/email_login_exitoso.html'
        destinatario = email
        contexto = {'mensaje': 'siuuu'}
        enviar_correo(asunto, plantilla, destinatario, contexto)

        # Devuelve la respuesta de la superclase
        return response

    def form_invalid(self, form):
        User = get_user_model()
        username = form.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            email = user.email
        except User.DoesNotExist:
            email = None


        # Si las credenciales son incorrectas, envía un correo electrónico de login fallido
        asunto = 'Login Fallido'
        plantilla = 'emails_template/email_login_fallido.html'
        destinatario = email
        contexto = {'mensaje': 'Usted ha intentado ingresar al sistema'}
        enviar_correo(asunto, plantilla, destinatario, contexto)
        return super().form_invalid(form)
