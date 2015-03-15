from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    
    # main
    url(r'^$', 'mysite.main.views.home', name='home'),
    url(r'^about/$', 'mysite.main.views.about', name='about'),
    url(r'^contact/$', 'mysite.main.views.contact', name='contact'),
    url(r'^request/$', 'mysite.main.views.request_pass', name='request'),
    
    # login, logout ...
    url(r'^sign_up/$', 'mysite.main.views.signup', name='signup'),
    url(r'^sign_in/$', 'django.contrib.auth.views.login', {'template_name': 'templates/main/signin.html'}, name='signin'),
    url(r'^sign_out/$', 'django.contrib.auth.views.logout', {'next_page': '/sign_in/'}, name='signout'),
    
    # videos
    url(r'^search/$', 'mysite.video.views.search', name='search'),
    url(r'^upload/$', 'mysite.video.views.upload', name='upload'),
    url(r'^genres/$', 'mysite.video.views.genres', name='genres'),
    url(r'^genre/(?P<slug>[-\w]+)/$', 'mysite.video.views.genre', name='genre'),
    url(r'^hot/$', 'mysite.video.views.hot', name='hot'),
    url(r'^hot/(?P<by>[month|year|day]+)/$', 'mysite.video.views.hot', name='hot_by'),
    # using user-friendly url style avoiding network admin understanding of situation
    url(r'^v/(?P<video_id>\d+)$', 'mysite.video.views.watch', name='watch'),
    
    url( r'^videos/', include( 'videostream.urls' ) ),
    
    url(r'^assets/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    
    url(r'^admin/', include(admin.site.urls)),
)
