from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render
from .models import Timetable,Subject,Classroom
from login.models import Students
from attendance.models import Record,Counting

from django.db.models import Count
def index(request,slug):
  attendances = []
  attendances_list = []
  percentage=float(0)
  Class=Classroom.objects.get(slug=slug)  
  timetable=Timetable.objects.all().filter(classroom__class_id=Class.class_id)	
  studentlist=Students.objects.all().filter(class_id=Class.class_id).order_by('student_id')
  #print studentlist
  subjects=Subject.objects.all().order_by("subject_id")
  string='str'
  print studentlist
  for user in studentlist:
    attendances = []
    records=Record.objects.values('subject__subject_name').filter(student__student_id=user.student_id).annotate(the_count=Count('subject__subject_id')).order_by('subject_id')

    countings=Counting.objects.all().filter(classroom__class_id=user.class_id).order_by("subject_id")
    if len(countings)!=len(subjects):
      for subject in subjects:
        Present=0
        for counting in countings:
          if subject.subject_name == counting.subject.subject_name:
            Present = 1
        if Present == 0:
          print Class
          print subject.subject_name
          Counting.objects.create(classroom=Class,subject=subject,count=0)
          #print "hi"
    print countings
    countings=Counting.objects.all().filter(classroom__class_id=user.class_id).order_by("subject_id")
    for counting in countings:
      for record in records:
        if record['subject__subject_name'] == counting.subject.subject_name:
          print record['the_count']
          if counting.count != 0:
            percentage = round(float(float(record['the_count'])/float(counting.count))*100,1)
            percentage = ('%f' % percentage).rstrip('0').rstrip('.')
            attendances.append(float(percentage))
          else:
            percentage=0
      if percentage==0:
        percentage = ('%f' % percentage).rstrip('0').rstrip('.')
        attendances.append(float(percentage))
      percentage=float(0)
    #attendances.insert(0,str(user.student_name))
    #attendances.insert(0,str(user.student_id))
    #attendances.insert(0,str(user.admission_number))
    attendances_list.append(attendances)
  attendances_list=zip(studentlist,attendances_list)
  #print attendances_list
  return render(request, 'timetable/index.html', {'slug':slug,'studentlist':studentlist,'timetable': timetable,'attendances_list':attendances_list,'subjects':subjects})
  
def details(request):
  attendances = []
  percentage=float(0)  
  a=request.GET.get("admission_number","") 
  user=Students.objects.get(admission_number=a)
  records=Record.objects.values('subject__subject_name').filter(student__student_id=user.student_id).annotate(the_count=Count('subject__subject_id')).order_by('subject_id')
  
  countings=Counting.objects.all().filter(classroom__class_id=user.class_id)
  subjects=Subject.objects.all()
  for counting in countings:
    for record in records:
      if record['subject__subject_name'] == counting.subject.subject_name:
        #print record['the_count']
        percentage = round(float(float(record['the_count'])/float(counting.count))*100,1)
        percentage = ('%f' % percentage).rstrip('0').rstrip('.')
        attendances.append(percentage)
    if percentage==0:
      percentage = ('%f' % percentage).rstrip('0').rstrip('.')
      attendances.append(float(percentage))
    percentage=float(0)
       
     #   print subject_name + ' ' + ((record.the_count/counting.count)*100)
  return render(request, 'timetable/studentdetails.html', { 'subjects': subjects,'user': user,'records':records,'counting':countings,'attendances':attendances})