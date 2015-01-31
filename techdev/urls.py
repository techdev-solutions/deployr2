from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'techdev.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('deployr2.urls', namespace="deployr2"))
)
