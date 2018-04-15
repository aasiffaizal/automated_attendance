from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
      url(r'^attendance/', include('attendance.urls')),
    url(r'^login/', include('login.urls')),
    url(r'^$',  views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^timetable/', include('timetable.urls',namespace='timetable')),
    url(r'^attendance/', include('attendance.urls',namespace='attendance'))




]