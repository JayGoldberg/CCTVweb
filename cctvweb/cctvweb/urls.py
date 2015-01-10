from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cctvweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^player/', include('imagestore.urls')),
)

'''
player/event/
player/event/<event_id>/details
report/daily/2014-05-34/all
report/all/daily/2014-05-34
report/daily/2014-05-34/<cam_id>


'''
