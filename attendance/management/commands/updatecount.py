from django.core.management.base import BaseCommand, CommandError
from attendance.models import Counting as CountTable
from timetable.models import Classroom,Timetable
from datetime import datetime
import calendar
from django.db.models import F



class Command(BaseCommand):
 help = 'Updates the count for all subjects'

    

 def handle(self, *args, **options):
  classes=Classroom.objects.all()
  for c in classes:
               date_time=datetime.now()
               day=calendar.day_name[date_time.weekday()]
               timetable=Timetable.objects.get(classroom__class_id=c.class_id,day=day)
             
               if CountTable.objects.filter(classroom__class_id=c.class_id,subject__subject_id=timetable.hour1.subject_id).exists():                       
                  updateobject=CountTable.objects.all().get(classroom__class_id=c.class_id,subject__subject_id=timetable.hour1.subject_id)
                  
                  
                  CountTable.objects.filter(id=updateobject.id).update(count=F('count')+1)
               else:   
                CountTable.objects.create(classroom=c,subject=timetable.hour1,count=1)

               if CountTable.objects.filter(classroom__class_id=c.class_id,subject__subject_id=timetable.hour2.subject_id).exists():                       
                  updateobject=CountTable.objects.all().get(classroom__class_id=c.class_id,subject__subject_id=timetable.hour2.subject_id)
                  
                  
                  CountTable.objects.filter(id=updateobject.id).update(count=F('count')+1)
               else:   
                CountTable.objects.create(classroom=c,subject=timetable.hour2,count=1)

               if CountTable.objects.filter(classroom__class_id=c.class_id,subject__subject_id=timetable.hour3.subject_id).exists():                       
                  updateobject=CountTable.objects.all().get(classroom__class_id=c.class_id,subject__subject_id=timetable.hour3.subject_id)
                  
                  
                  CountTable.objects.filter(id=updateobject.id).update(count=F('count')+1)
               else:   
                CountTable.objects.create(classroom=c,subject=timetable.hour3,count=1)

               if CountTable.objects.filter(classroom__class_id=c.class_id,subject__subject_id=timetable.hour4.subject_id).exists():                       
                  updateobject=CountTable.objects.all().get(classroom__class_id=c.class_id,subject__subject_id=timetable.hour4.subject_id)
                  
                  
                  CountTable.objects.filter(id=updateobject.id).update(count=F('count')+1)
               else:   
                CountTable.objects.create(classroom=c,subject=timetable.hour4,count=1)

               if CountTable.objects.filter(classroom__class_id=c.class_id,subject__subject_id=timetable.hour5.subject_id).exists():                       
                  updateobject=CountTable.objects.all().get(classroom__class_id=c.class_id,subject__subject_id=timetable.hour5.subject_id)
                  
                  
                  CountTable.objects.filter(id=updateobject.id).update(count=F('count')+1)
               else:   
                CountTable.objects.create(classroom=c,subject=timetable.hour5,count=1)

               if CountTable.objects.filter(classroom__class_id=c.class_id,subject__subject_id=timetable.hour6.subject_id).exists():                       
                  updateobject=CountTable.objects.all().get(classroom__class_id=c.class_id,subject__subject_id=timetable.hour6.subject_id)
                  
                  
                  CountTable.objects.filter(id=updateobject.id).update(count=F('count')+1)
               else:   
                CountTable.objects.create(classroom=c,subject=timetable.hour6,count=1)
               