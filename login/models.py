from django.db import models
from django.core.validators import validate_email
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Staff(models.Model):
 staff_name = models.CharField(max_length=30)
 staff_id=models.IntegerField(primary_key=True)
 department = models.CharField(max_length=30)
 username = models.CharField(max_length=100)
 password = models.CharField(max_length=50)
 email = models.EmailField(unique=True, validators=[validate_email,])
 subject = models.ForeignKey('timetable.Subject')
 def __str__(self):
     return self.staff_name

@python_2_unicode_compatible
class Students(models.Model):
 student_name = models.CharField(max_length=30)
 student_id=models.IntegerField(primary_key=True)
 admission_number= models.CharField(max_length=40)
 class_id=models.IntegerField()
 def __str__(self):
     return self.student_name
	