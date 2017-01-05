# -*- encoding: utf-8 -*-

from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, ButtonHolder, Fieldset
from core.models import Cliente, Estoque, Venda, ProdutosPorVenda

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
                'sexo',
                'dt_nascimento',
                'endereco',
                'bairro',
                'cidade',
                'telefone',
                'celular',
                css_class="container-fluid"
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class="btn-success")
            )
        )
        super(ClienteForm, self).__init__(*args, **kwargs)

class EstoqueForm(ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'valor', 'quantidade']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                'produto',
                'valor',
                'quantidade',
                css_class="container-fluid"
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class="btn-success")
            )
        )
        super(EstoqueForm, self).__init__(*args, **kwargs)


class VendaForm(ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'forma_de_pagamento', 'dataDaVenda']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.form_tag = False
        helper.layout = Layout(
            Div(
                'cliente',
                'forma_de_pagamento',
                'dataDaVenda',
                css_class="container-fluid"
            ),
        )
        return helper

class ProdutosPorVendaFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProdutosPorVendaFormHelper, self).__init__(*args, **kwargs)
        self.form_tag=False
        self.field_class = 'col-lg-3'
        self.layout = Layout(
            Fieldset(
                'Produtos',
                'estoque',
                'quantidade',
                'valorDeVenda',
                'desconto'
            )
        )

ProdutosPorVendaFormSet = inlineformset_factory(Venda, ProdutosPorVenda, fields=['estoque', 'quantidade', 'valorDeVenda', 'desconto'], extra=4)