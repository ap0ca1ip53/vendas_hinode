# -*- encoding: utf-8 -*-

from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from core.models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'sexo', 'endereco', 'bairro', 'dt_nascimento']

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()