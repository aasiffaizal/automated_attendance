from django.db import models
from django.core.validators import validate_email
from django.utils.encoding import python_2_unicode_compatible
import calendar, datetime

@python_2_unicode_compatible
class Record(models.Model):
 student = models.ForeignKey('login.Students')
 subject=models.ForeignKey('timetable.Subject')
 date_time = models.DateField()
 hour=models.IntegerField(default=0)
 def __str__(self):
    return (self.student.student_name+' '+self.subject.subject_name)
 def day_of_week(self):
     return(calendar.day_name[self.date_time.weekday()])
@python_2_unicode_compatible
class Counting(models.Model):
 classroom=models.ForeignKey('timetable.Classroom')
 subject=models.ForeignKey('timetable.Subject')
 count=models.IntegerField()
 def __str__(self):
    return (self.subject.subject_name+' '+self.classroom.department+str(self.classroom.semester)+self.classroom.section)

@python_2_unicode_compatible
class Record1(models.Model):
 student = models.ForeignKey('login.Students')
 date_time = models.DateField()
 hour1=models.CharField(max_length=10,default="absent")
 hour2=models.CharField(max_length=10,default="absent")
 hour3=models.CharField(max_length=10,default="absent")
 hour4=models.CharField(max_length=10,default="absent")
 hour5=models.CharField(max_length=10,default="absent")
 hour6=models.CharField(max_length=10,default="absent")
 def __str__(self):
   return (self.student.student_name+' '+str(self.date_time))
 def day_of_week(self):
    return(calendar.day_name[self.date_time.weekday()])

@python_2_unicode_compatible
class Error(models.Model):
 student = models.ForeignKey('login.Students')
 staff=models.ForeignKey('login.Staff')
 date_time=models.DateField()
 error_hrs=models.CharField(max_length=15)
 def __str__(self):
   return (self.student.student_name+' '+str(self.date_time))