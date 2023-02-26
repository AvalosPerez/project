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
        # Realiza cualquier operación adicional que desees antes de que el usuario inicie sesión
        # ...

        # Llama al método form_valid de la superclase, que realiza la autenticación de usuario y redirige al usuario a la página de inicio
        response = super().form_valid(form)

        # Realiza cualquier operación adicional que desees después de que el usuario haya iniciado sesión
        # ...

        asunto = 'Correo de prueba'

        plantilla = 'emails_template/email_login_exitoso.html'
        destinatario = 'fuenteskevin543@gmail.com'
        contexto = {'mensaje': 'siuuu'}
        enviar_correo(asunto, plantilla, destinatario, contexto)

        # Devuelve la respuesta de la superclase
        return response
