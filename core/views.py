# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from core.models import Cliente


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
    fields = ['nome', 'sexo']
    form_class = 