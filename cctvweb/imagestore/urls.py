from django.conf.urls import patterns, include, url

from imagestore import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<image_id>\d+)/$', views.player, name='player')
)
