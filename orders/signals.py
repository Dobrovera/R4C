from django.dispatch import receiver
from django.db.models.signals import post_save
from django.forms.models import model_to_dict

from robots.models import Robot
from .views import send_mail_to_customer
from .models import Order


@receiver(post_save, sender=Robot)
def email_send_signal(sender, instance, **kwargs):
    model = model_to_dict(instance, fields='model')['model']
    version = model_to_dict(instance, fields='version')['version']
    serial = model_to_dict(instance, fields='serial')['serial']
    emails = []

    try:
        order = Order.objects.filter(robot_serial=serial).all()
        for ord in order:
            emails.append(ord.customer.email)

        send_mail_to_customer(emails, model, version)

    except Exception:
        return None

    else:
        Order.objects.filter(robot_serial=serial).delete()
