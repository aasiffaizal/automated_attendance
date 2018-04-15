from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Record,Record1,Error
from login.models import Students,Staff
from timetable.models import Classroom
from datetime import datetime
import unicodedata
def index(request):
    return HttpResponse("Hello, world. You're at the attendance index.")

def reporterror(request):
    some_var = request.POST.getlist('checks[]')
    user=request.POST.get('user_id')
    Student=Students.objects.get(admission_number=user)
    
    #for date in dates:
     #   day=str(date)
    #day=day.replace(',','')
    #print day
    #date = datetime.strptime(day, '%B %d %Y')
    #print date
    #print type(date)
    print some_var
    for t in some_var:
      date,hour= t.split('_')
      print date
      date=date.replace(',','')
      date = datetime.strptime(date, '%B %d %Y')
      #record=Record1.objects.all().get(id=a)
      classdetails=Classroom.objects.all().get(class_id=Student.class_id)
      #Error.objects.create(staff=classdetails.staff,student=record.student,date_time=record.date_time,error_hrs=b )
      Error.objects.get_or_create(staff=classdetails.staff,student=Student,date_time=date,error_hrs=hour)
    print Student.admission_number
    url="/login/studentlogin/"+str(Student.admission_number)
    return HttpResponseRedirect(url)      
