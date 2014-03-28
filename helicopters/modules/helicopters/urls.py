from django.conf.urls import patterns, include, url
from flight_log import views, utility
from flight_log import man_draft_log_views as draft_views
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^log/', views.log),
    url(r'^log/(?P<param>\d{1})/$', views.log),
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$', views.home),
    url(r'^signin/$', views.signin),
    url(r'^register/$', 'register.views.register'),
    url(r'^login/$', views.signin),
    url(r'^logout/$', views.logout),
    url(r'^send_email/$' , utility.send_email),
    #url(r'^email_succseful/$', utility.email_succseful),
#     url(r'^draft_process', draft_views.edit_delete, name = "draft_process"),
    url(r'^search/$', views.search),
    url(r'^search/print/$', views.print_pdf),
    url(r'^log/print/$', views.print_pdf),
    url(r'^download/$', views.download),
)

