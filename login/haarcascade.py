import numpy as np
import cv2, os
fn_dir = 'database'
from django.conf import settings
#path = os.path.join(fn_dir, "Unknown")
#if not os.path.isdir(path):
#    os.mkdir(path)
def detection(image_path):
    face_path = os.path.join(settings.FILES_DIR, "haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier(face_path)
    count=0
    print image_path
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(20, 20), flags=cv2.CASCADE_SCALE_IMAGE)
    no_faces=len(faces)
    for (x,y,w,h) in faces:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),5)
        roi_gray = gray[y:y+w, x:x+h]
        roi_color = img[y:y+h, x:x+w]
        var1 = gray[y: y + w, x: x + h]
        face_resize = cv2.resize(var1, (100, 100))
        count=count+1
        count=str(count)
        cv2.imwrite(settings.FILES_DIR+"/Unknown/U_"+count+".jpg",face_resize)
        
        count=int(count)    
        count=str(count)
        print "Found"+str(no_faces)+" faces"
        count=int(count)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

