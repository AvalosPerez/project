# Create your models here.
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.db import models
from django.template.loader import get_template, render_to_string

from project import settings

def enviar_correo(asunto, plantilla, destinatario, contexto):
    try:
        cuerpo_correo = render_to_string(plantilla, contexto)
        correo = EmailMessage(asunto, cuerpo_correo, to=[destinatario])
        correo.content_subtype = 'html'
        correo.send()
    except Exception as ex:
        pass



def create_mail_simple(user_mail, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_mail
        ],
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    return message