from django.conf.urls import url

from . import views

app_name = 'hinode'
urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^clientes/$', views.ClienteList.as_view(), name='clientes_list'),
    url(r'^clientes/add/$', views.ClienteCreate.as_view(), name='clientes_add'),
    url(r'^clientes/(?P<pk>[0-9]+)/$', views.ClienteUpdate.as_view(), name='clientes_update'),
    url(r'^clientes/(?P<pk>[0-9]+)/delete/$', views.ClienteDelete.as_view(), name='clientes_delete'),
]