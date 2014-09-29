from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.flatpages import views

urlpatterns = patterns('',
    url(r'^$', 'giftroulette.gift.views.home', name='home'),

    url(r'^gift/(?P<gift_hash>\w+)/$', 'giftroulette.gift.views.gift_read', name='gift_read'),
    url(r'^gift/(?P<gift_hash>\w+)/thankyou/$', 'giftroulette.gift.views.thankyou', name='thankyou'),
    url(r'^gift/(?P<gift_hash>\w+)/upload/$', 'giftroulette.gift.views.upload', name='upload'),
    url(r'^gift/(?P<gift_hash>\w+)/email/$', 'giftroulette.gift.views.email', name='email'),


    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<url>.*/)$', views.flatpage),
)
