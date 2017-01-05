from django.conf.urls import url
from core.models import Cliente
from . import views

app_name = 'hinode'
urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),

    url(r'^clientes/$', views.ClienteList.as_view(), name='clientes_list'),
    url(r'^clientes/add/$', views.ClienteCreate.as_view(), name='clientes_add'),
    url(r'^clientes/update/(?P<pk>[0-9]+)/$', views.ClienteUpdate.as_view(), name='clientes_update'),
    url(r'^clientes/delete/(?P<cliente_id>[0-9]+)/$', views.cliente_delete, name='clientes_delete'),

    url(r'^estoque/$', views.EstoqueList.as_view(), name='estoque_list'),
    url(r'^estoque/add/$', views.EstoqueCreate.as_view(), name='estoque_add'),
    url(r'^estoque/update/(?P<pk>[0-9]+)/$', views.EstoqueUpdate.as_view(), name='estoque_update'),
    url(r'^estoque/delete/(?P<estoque_id>[0-9]+)/$', views.estoque_delete, name='estoque_delete'),

    url(r'^vendas/$', views.VendasList.as_view(), name='vendas_list'),
    url(r'^vendas/add/$', views.VendasCreate.as_view(), name='vendas_add'),
]