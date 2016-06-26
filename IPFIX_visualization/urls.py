from django.conf.urls import url

from . import views

app_name = 'IPFIX_visualization'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^t2v/(?P<t2vid>[0-9]+)/$', views.zoominont2v, name='zoominont2v'),
]
