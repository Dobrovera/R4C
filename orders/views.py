import json

from django.core.mail import send_mass_mail
from django.views import View
from django.http import HttpResponse

from customers.models import Customer
from robots.models import Robot
from .models import Order
from .forms import OrderEmailForm


class OrderView(View):

    def post(self, request):

        try:
            order = json.loads(request.body)
            form = OrderEmailForm(order)

            if form.is_valid():
                customer_email = order['customer_email']
                robot_serial = order['robot_serial']

                if not Robot.objects.filter(serial=robot_serial).exists():
                    if Customer.objects.filter(email=customer_email).exists():
                        customer = Customer.objects.filter(email=customer_email).get()

                    else:
                        customer = Customer(
                            email=customer_email,
                        )
                        customer.save()

                    order = Order(
                        customer=customer,
                        robot_serial=robot_serial
                    )
                    order.save()

                    return HttpResponse('Данные успешно сохранены!')

                elif Robot.objects.filter(serial=robot_serial).exists():
                    return HttpResponse('Такой робот уже в наличии!')

            else:
                return HttpResponse(f'Ошибка формы: {form.errors.as_json()}', 500)

        except Exception as e:
            return HttpResponse(f'Ошибка: {e}', 500)


def send_mail_to_customer(email, model, version):
    try:
        subject = 'Компания R4C'
        message = (f"Добрый день! \n"
                   f"Недавно вы интересовались нашим роботом модели {model}, версии {version}. \n"
                   f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами")
        company_email = 'r4c@gmail.com'
        message = (
            subject,
            message,
            company_email,
            email,
        )
        send_mass_mail((message,), fail_silently=False)

    except Exception as e:
        print(f'Ошибка: {e}')
