from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Classroom(models.Model):
 department = models.CharField(max_length=30)
 class_id=models.IntegerField(primary_key=True)
 semester=models.IntegerField()
 section=models.CharField(max_length=2)
 staff=models.ForeignKey('login.Staff')
 slug=models.CharField(max_length=50,default='CS8')
 def __str__(self):
    return (self.department+str(self.semester)+'- '+self.section)

@python_2_unicode_compatible
class Timetable(models.Model):
 classroom=models.ForeignKey('Classroom')
 day=models.CharField(max_length=20)
 hour1=models.ForeignKey('Subject',on_delete=models.CASCADE, related_name='+')
 hour2=models.ForeignKey('Subject',on_delete=models.CASCADE, related_name='+')
 hour3=models.ForeignKey('Subject',on_delete=models.CASCADE, related_name='+')
 hour4=models.ForeignKey('Subject',on_delete=models.CASCADE, related_name='+')
 hour5=models.ForeignKey('Subject',on_delete=models.CASCADE, related_name='+')
 hour6=models.ForeignKey('Subject',on_delete=models.CASCADE, related_name='+')
 def __str__(self):
   return (self.classroom.department+str(self.classroom.semester)+self.classroom.section+' '+self.day)
@python_2_unicode_compatible
class Subject(models.Model):
  subject_id=models.IntegerField()
  subject_name=models.CharField(max_length=20)
  def __str__(self):
    return (str(self.subject_id)+' '+self.subject_name)
    