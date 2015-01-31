from django.conf.urls import url, patterns

from deployr2 import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^start_deployment/$', views.start_deployment, name='start_deployment'),
   url(r'^get_builds$', views.get_builds_for_build_type_and_branch),
)