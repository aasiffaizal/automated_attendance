from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from .models import Staff
from .models import Students
from django.contrib.auth.decorators import login_required, permission_required
from timetable.models import Classroom,Timetable,Subject
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from attendance.models import Record,Counting,Record1,Error
from django.db.models import Count, Sum
import calendar
from detection import recognition
from haarcascade import detection
import calendar
import datetime as DT
import os
from django.conf import settings
from datetime import datetime
import cv2



def index(request):
    error=None
    if request.method == 'GET' and 'slug' in request.GET:
        slug = request.GET.get('slug')
        print slug
        url="/timetable/"+slug
        return HttpResponseRedirect(url)
    if request.user.is_authenticated():
        return HttpResponseRedirect('stafflogin')    
    elif request.method == 'POST' and 'staff_username' in request.POST:
        username = request.POST.get('staff_username', '')
        password = request.POST.get('staff_password', '')
        error="Username or password is incorrect"
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('stafflogin')
    elif request.method == 'POST' and 'admission_number' in request.POST:
        admission_number = request.POST.get('admission_number')
        url="studentlogin/"+admission_number
        return HttpResponseRedirect(url)
    elif request.method == 'POST' and 'slug' in request.POST:
        slug = request.POST.get('slug')
        print slug
        url="/timetable/"+slug
        return HttpResponseRedirect(url)
    classlist=Classroom.objects.all()
    return render(request, 'login/index.html', {'classlist': classlist,'error':error})

@login_required(login_url="/login")
def stafflogin(request):
    user=Staff.objects.get(username=request.user)
    classlist=Classroom.objects.all() 
    notifs=Error.objects.filter(staff__staff_id=user.staff_id)
    count=0
    for entry in notifs:
        count=count+1
    print count
    print settings.STATIC_DIR
    if request.method == 'POST':
        file_path = os.path.join(settings.FILES_DIR, "Group_photos")
        subject_images_names = os.listdir(file_path)
        for image_name in subject_images_names:  
        #ignore system files like .DS_Store
            if image_name.startswith("."):
                continue;
            image_path = file_path + "/" + image_name
            detection(image_path)
            attendance = recognition()
            time=datetime.fromtimestamp(os.path.getctime(image_path))
            hour = time_check_normal(time)
            slug=time.date()
            img = cv2.imread(image_path)
            URL= settings.STATIC_DIR+"/CS8A/"+str(slug)+"_Hour"+str(hour)+".jpg"
            print "URL"+URL
            cv2.imwrite(URL,img)
            print time
            os.remove(image_path)
            print hour
            print type(hour)
            for present in attendance:
                give_attendance(int(present),time.date(),hour)
        return render(request, 'login/stafflogin.html', {'user': user,'notifs':notifs,'classlist':classlist,'count':count})
    return render(request, 'login/stafflogin.html', {'user': user,'count':count,'classlist':classlist,'notifs':notifs})
     

def studentlogin(request,admission_number=None):
    attendances = []
    percentage=float(0)
    subjects=Subject.objects.all()
    user=Students.objects.get(admission_number=admission_number)
    end_date=DT.date.today()
    days=date_check(calendar.day_name[end_date.weekday()])
    print "days"
    print days
    start_date=end_date - DT.timedelta(days=int(days))
    reports=Record1.objects.all().filter(student__student_id=user.student_id,date_time__range=(start_date,end_date)).order_by('date_time')
    records=Record.objects.values('subject__subject_name').filter(student__student_id=user.student_id).annotate(the_count=Count('subject__subject_id')).order_by("subject_id")
    countings=Counting.objects.all().filter(classroom__class_id=user.class_id).order_by("subject_id")
    timetable=Timetable.objects.all().filter(classroom__class_id=user.class_id)
    #total=Counting.objects.filter(classroom__class_id=user.class_id).aggregate(Sum('count'))
    print countings
    print records
    for counting in countings:
        for record in records:
            if record['subject__subject_name'] == counting.subject.subject_name:
                if counting.count != 0:
                    percentage = round(float(float(record['the_count'])/float(counting.count))*100,1)
                    percentage = ('%f' % percentage).rstrip('0').rstrip('.')
                    attendances.append(percentage)
                else:
                    percentage=0
        if percentage == 0:
            percentage = ('%f' % percentage).rstrip('0').rstrip('.')
            attendances.append(percentage)
        percentage=float(0)
    print attendances            
    return render(request, 'login/studentlogin.html', {'reports':reports,'user': user,'subjects':subjects,'timetable':timetable,'start_date':start_date,'attendances':attendances})
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

@login_required(login_url="/login")
def reports(request):
    user=Staff.objects.get(username=request.user)
    classlist=Classroom.objects.all() 
    notifs=Error.objects.filter(staff__staff_id=user.staff_id)
    print notifs
    return render(request, 'login/error.html', {'notifs': notifs})  

@login_required(login_url="/login")
def grant(request,err_id=None):
    error=Error.objects.get(id=err_id)
    print error
    hour=int(error.error_hrs)
    date=error.date_time
    print hour
    print date
    classroom = Classroom.objects.get(class_id=error.student.class_id)
    subject = Timetable.objects.get(classroom=classroom,day=calendar.day_name[date.weekday()]) 
    if hour is 1:
        hour1 = "present"
        Record1.objects.update_or_create(date_time=date, student=error.student,defaults={'hour1': hour1 },)
        Record.objects.update_or_create(student=error.student,hour=hour,date_time=date,subject=subject.hour1)
    if hour is 2:
        hour2 = "present"
        Record1.objects.update_or_create(date_time=date, student=error.student,defaults={'hour2': hour2 },)
        Record.objects.update_or_create(student=error.student,hour=hour,date_time=date,subject=subject.hour2)
    if hour is 3:
        hour3 = "present"
        Record1.objects.update_or_create(date_time=date, student=error.student,defaults={'hour3': hour3 },)
        Record.objects.update_or_create(student=error.student,hour=hour,date_time=date,subject=subject.hour3)
    if hour is 4:
        hour4 = "present"
        Record1.objects.update_or_create(date_time=date, student=error.student,defaults={'hour4': hour4 },)
        Record.objects.update_or_create(student=error.student,hour=hour,date_time=date,subject=subject.hour4)
    if hour is 5:
        hour5 = "present"
        Record1.objects.update_or_create(date_time=date, student=error.student,defaults={'hour5': hour5 },)
        Record.objects.update_or_create(student=error.student,hour=hour,date_time=date,subject=subject.hour5)
    if hour is 6:
        hour6 = "present"
        Record1.objects.update_or_create(date_time=date, student=error.student,defaults={'hour6': hour6 },)
        Record.objects.update_or_create(student=error.student,hour=hour,date_time=date,subject=subject.hour6)
    url="/login/deny/"+err_id
    return HttpResponseRedirect(url)

def deny(request,err_id=None):
    error=Error.objects.get(id=err_id)
    error.delete()
    return HttpResponseRedirect("/login/reports")

def update_week(request):
    attendance=['13','67','6','55']
    date = datetime.strptime('9 Apr 2018', '%d %b  %Y')
    print date
    hours=[4,5,6]
    for hour in hours:
        print attendance
        for present in attendance:
            give_attendance(int(present),date,hour)
    return HttpResponseRedirect('/login/')

def date_check(day):
    if day == 'Monday':
        return(0)
    if day == 'Tuesday':
        return(1)
    if day == 'Wednesday':
        return(2)
    if day == 'Thursday':
        return(3)
    if day == 'Friday':
        return(4)
    if day == 'Saturday':
        return(5)
    if day == 'Sunday':
        return(6)

@login_required(login_url="/login")
def manual_method(request):
    classlist=Classroom.objects.all()
    flag=None
    if request.method == 'POST' and request.POST.get('class', ''):
        flag = 1
        slug = request.POST.get('class', '')
        Class=Classroom.objects.get(slug=slug)  
        timetable=Timetable.objects.all().filter(classroom__class_id=Class.class_id)	
        studentlist=Students.objects.all().filter(class_id=Class.class_id).order_by('student_id')
        context={'flag':flag,'classlist':classlist,'slug':slug,'studentlist':studentlist}
        return render(request, 'login/manual.html',context)
    if request.method == 'POST' and "cancel" in request.POST:
        flag = None
        context={'flag':flag,'classlist':classlist}
        return render(request, 'login/manual.html',context)
    if request.method == 'POST' and "submit" in request.POST:
        roll_nos=request.POST.getlist("roll[]")
        date=request.POST.get('date', None)
        
        
        hour=request.POST.get('hour', None)
        slug = request.POST.get('slug', '')
        if request.POST.get('hour', '') and request.POST.get('date', '') and request.POST.getlist('roll[]',''):
            hour=int(hour)
            date = datetime.strptime(date, '%d-%m-%Y')
            for no in roll_nos:
                give_attendance(no,date,hour)
            return HttpResponseRedirect("/login/manual_method/")
        else:
            flag = 1
            Class=Classroom.objects.get(slug=slug)  
            timetable=Timetable.objects.all().filter(classroom__class_id=Class.class_id)	
            studentlist=Students.objects.all().filter(class_id=Class.class_id).order_by('student_id')
            err_msg="Fill the required fields to enter the attendance."
            context={'flag':flag,
                    'classlist':classlist,
                    'slug':slug,
                    'studentlist':studentlist,
                    'err_msg':err_msg}
            return render(request, 'login/manual.html',context)

    return render(request, 'login/manual.html',{'flag':flag,'classlist':classlist})

def give_attendance(roll_no,date,hour):
    if hour is 1:
        hour1 = "present"
    if hour is 2:
        hour2 = "present"
    if hour is 3:
        hour3 = "present"
    if hour is 4:
        hour4 = "present"
    if hour is 5:
        hour5 = "present"
    if hour is 6:
        hour6 = "present"
    student = Students.objects.get(student_id=int(roll_no))
    classroom = Classroom.objects.get(class_id=student.class_id)
    print classroom
    subject = Timetable.objects.get(classroom=classroom,day=calendar.day_name[date.weekday()]) #day=friday
    if hour is 1:
        obj, created = Record1.objects.update_or_create(date_time=date, student=student,defaults={'hour1': hour1 },)
        Record.objects.get_or_create(student=student,hour=hour,date_time=date,subject=subject.hour1)
    if hour is 2:
        obj, created = Record1.objects.update_or_create(date_time=date, student=student,defaults={'hour2': hour2 },)
        Record.objects.get_or_create(student=student,hour=hour,date_time=date,subject=subject.hour2)
    if hour is 3:
        obj, created = Record1.objects.update_or_create(date_time=date, student=student,defaults={'hour3': hour3 },)
        Record.objects.get_or_create(student=student,hour=hour,date_time=date,subject=subject.hour3)
    if hour is 4:
        obj, created = Record1.objects.update_or_create(date_time=date, student=student,defaults={'hour4': hour4 },)
        Record.objects.get_or_create(student=student,hour=hour,date_time=date,subject=subject.hour4)
    if hour is 5:
        obj, created = Record1.objects.update_or_create(date_time=date, student=student,defaults={'hour5': hour5 },)
        Record.objects.get_or_create(student=student,hour=hour,date_time=date,subject=subject.hour5)
    if hour is 6:
        obj, created = Record1.objects.update_or_create(date_time=date, student=student,defaults={'hour6': hour6 },)
        Record.objects.get_or_create(student=student,hour=hour,date_time=date,subject=subject.hour6)
    return

def time_check_normal(time):
    hour1_time = time.replace(hour=9, minute=30, second=0, microsecond=0)
    hour2_time = time.replace(hour=10, minute=30, second=0, microsecond=0)
    hour3_time = time.replace(hour=11, minute=30, second=0, microsecond=0) 
    lunch_time = time.replace(hour=12, minute=30, second=0, microsecond=0)
    hour4_time = time.replace(hour=13, minute=30, second=0, microsecond=0)
    hour5_time = time.replace(hour=14, minute=30, second=0, microsecond=0)
    hour6_time = time.replace(hour=15, minute=30, second=0, microsecond=0)
    if time > hour1_time and time < hour2_time:
        hour = int('1')
    if time > hour2_time and time < hour3_time:
        hour = int('2')
    if time > hour3_time and time < lunch_time:
        hour = int('3')
    if time > hour4_time and time < hour5_time:
        hour = int('4')
    if time > hour5_time and time < hour6_time:
        hour = int('5')
    if time > hour6_time:
        hour = int('6')
    return hour

def time_check_friday(time):
    hour1_time = time.replace(hour=9, minute=30, second=0, microsecond=0)
    hour2_time = time.replace(hour=10, minute=25, second=0, microsecond=0)
    hour3_time = time.replace(hour=11, minute=20, second=0, microsecond=0) 
    lunch_time = time.replace(hour=12, minute=15, second=0, microsecond=0)
    hour4_time = time.replace(hour=14, minute=0, second=0, microsecond=0)
    hour5_time = time.replace(hour=15, minute=0, second=0, microsecond=0)
    hour6_time = time.replace(hour=16, minute=0, second=0, microsecond=0)
    if time > hour1_time and time < hour2_time:
        hour = int('1')
    if time > hour2_time and time < hour3_time:
        hour = int('2')
    if time > hour3_time and time < lunch_time:
        hour = int('3')
    if time > hour4_time and time < hour5_time:
        hour = int('4')
    if time > hour5_time and time < hour6_time:
        hour = int('5')
    if time > hour6_time:
        hour = int('6')
    return hour