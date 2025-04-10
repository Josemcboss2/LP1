from django import forms
from .models import ContactMessage

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Nombre completo')
    email = forms.EmailField(label='Correo electrónico')
    phone = forms.CharField(label='Teléfono', required=False)
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)