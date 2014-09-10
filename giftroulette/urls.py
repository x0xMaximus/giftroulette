from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'giftroulette.gift.views.home', name='home'),
    url(r'^thankyou/(?P<gift_id>\d+)/$', 'giftroulette.gift.views.thankyou', name='thankyou'),
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
)
