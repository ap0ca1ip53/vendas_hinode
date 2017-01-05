# -*- encoding: utf-8 -*-

from datetime import date
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from core.models import Cliente, Estoque, Venda, ProdutosPorVenda
from core.forms import ClienteForm, EstoqueForm, VendaForm, ProdutosPorVendaFormHelper, ProdutosPorVendaFormSet
from django.urls import reverse_lazy
from extra_views import InlineFormSetView, CreateWithInlinesView



def index(request):
    return render(request, 'core/home.html')


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('hinode:index'))

    kwargs['extra_context'] = {'next': 'hinode:index'}
    kwargs['template_name'] = 'core/login.html'
    return login(request, *args, **kwargs)


def logout_view(request, *args, **kwargs):
    kwargs['next_page'] = reverse('hinode:index')
    return logout(request, *args, **kwargs)

class ClienteList(ListView):
    model = Cliente
    template = 'core/cliente_list.html'

class ClienteCreate(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('hinode:clientes_list')

class ClienteUpdate(UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('hinode:clientes_list')

def cliente_delete(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    cliente.delete()

    return HttpResponseRedirect(reverse('hinode:clientes_list'))

class EstoqueList(ListView):
    model = Estoque

    def get_queryset(self):
        qs = super(EstoqueList, self).get_queryset()
        qs = qs.filter(consultor=self.request.user)

        return qs

class EstoqueCreate(CreateView):
    model = Estoque
    form_class = EstoqueForm
    success_url = reverse_lazy('hinode:estoque_list')

    def form_valid(self, form):
        form.instance.consultor = self.request.user
        return super(EstoqueCreate, self).form_valid(form)

class EstoqueUpdate(UpdateView):
    model = Estoque
    form_class = EstoqueForm
    success_url = reverse_lazy('hinode:estoque_list')

def estoque_delete(request, estoque_id):
    produto = Estoque.objects.get(pk=estoque_id)
    produto.delete()

    return HttpResponseRedirect(reverse('hinode:estoque_list'))

class VendasList(ListView):
    model = Venda
    template = 'core/vendas_list.html'

"""class ProdutosPorVendaInline(InlineFormSetView):
    model = Venda
    inline_model = ProdutosPorVenda
    fields = ['estoque', 'venda', 'quantidade', 'valorDeVenda']

class VendasCreate(CreateWithInlinesView):
    model = Venda
    inlines = [ProdutosPorVendaInline]
    form_class = VendaForm
    success_url = reverse_lazy('hinode:vendas_list')

"""
class VendasCreate(CreateView):
    model = Venda
    form_class = VendaForm
    success_url = reverse_lazy('hinode:vendas_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        produto_form = ProdutosPorVendaFormSet()
        produto_formhelper = ProdutosPorVendaFormHelper()

        return self.render_to_response(
            self.get_context_data(form=form, produto_form=produto_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        produto_form = ProdutosPorVendaFormSet(self.request.POST)

        if (form.is_valid() and produto_form.is_valid()):
            return self.form_valid(form, produto_form)

        return self.form_invalid(form, produto_form)

    def form_valid(self, form, produto_form):

        #Called if all forms are valid. Creates a Author instance along
        #with associated books and then redirects to a success page.

        self.object = form.save()
        produto_form.instance = self.object
        produto_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, produto_form):

        #Called if whether a form is invalid. Re-renders the context
        #data with the data-filled forms and errors.

        return self.render_to_response(
            self.get_context_data(form=form, produto_form=produto_form)
        )

    def get_context_data(self, **kwargs):
        #Add formset and formhelper to the context_data.

        ctx = super(VendasCreate, self).get_context_data(**kwargs)
        produto_formhelper = ProdutosPorVendaFormHelper()

        if self.request.POST:
            ctx['form'] = VendaForm(self.request.POST)
            ctx['produto_form'] = ProdutosPorVendaFormSet(self.request.POST)
            ctx['produto_formhelper'] = produto_formhelper
        else:
            ctx['form'] = VendaForm()
            ctx['produto_form'] = ProdutosPorVendaFormSet()
            ctx['produto_formhelper'] = produto_formhelper
        return ctx