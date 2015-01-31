from django.conf.urls import url, patterns

from deployr2 import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^start_deployment/$', views.start_deployment, name='start_deployment')
)