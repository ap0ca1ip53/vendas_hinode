# -*- encoding: utf-8 -*-

from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiField, Fieldset, Div
from core.models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'sexo', 'endereco', 'bairro', 'cidade', 'telefone','celular', 'dt_nascimento']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
                Div(
                    'nome',
                    'sexo'
                    'dt_nascimento'
                ),
                'endereco',
                Div(
                    'bairro',
                    'cidade'
                ),
                Div(
                    'telefone',
                    'celular'
                )
        )
        super(ClienteForm, self).__init__(*args, **kwargs)