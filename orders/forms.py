from django import forms


class OrderEmailForm(forms.Form):
    customer_email = forms.EmailField(max_length=255)
    robot_serial = forms.CharField(max_length=5)