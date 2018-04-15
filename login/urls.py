from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update_week/$', views.update_week,name='update_week'),
    url(r'^stafflogin/$', views.stafflogin,name='stafflogin'),
    url(r'^reports/$', views.reports,name='reports'),
    url(r'^manual_method/$', views.manual_method,name='manual_method'),
    url(r'^studentlogin/(?P<admission_number>[0-9]+)$', views.studentlogin,name='studentlogin'),
    url(r'^grant/(?P<err_id>[0-9]+)$', views.grant,name='grant'),
    url(r'^deny/(?P<err_id>[0-9]+)$', views.deny,name='deny'),
    url(r'^logout_view/$', views.logout_view,name='logout_view')
]