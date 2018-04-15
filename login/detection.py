#import OpenCV module
import cv2
#import os module for reading training data directories and paths
import os
from datetime import datetime
#import numpy to convert python lists to numpy arrays as 
#it is needed by OpenCV face recognizers
import numpy as np
#cv2.imshow(img)
import matplotlib.pyplot as plt
import pickle
from haarcascade import detection
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
from django.conf import settings

################################# start face detection ####################################

def detect_face(img):
    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #load OpenCV face detector, I am using LBP which is fast
    #there is also a more accurate but slow Haar classifier
    face_path = os.path.join(settings.FILES_DIR, "haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier(face_path)

    #let's detect multiscale (some images may be closer to camera than others) images
    #result is a list of faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=1);
    
    #if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None
    
    #under the assumption that there will be only one face,
    #extract the face area
    (x, y, w, h) = faces[0]
    
    #return only the face part of the image
    return cv2.resize(gray[y:y+w, x:x+h], (100, 100)), faces[0]


################################## end face detection ##################################

################################## start Training data ##################################
#this function will read all persons' training images, detect face from each image
#and will return two lists of exactly same size, one list 
# of faces and another list of labels for each face
def prepare_training_data(data_folder_path):
    
    #------STEP-1--------
    #get the directories (one directory for each subject) in data folder
    file_path = os.path.join(settings.FILES_DIR, "database")
    dirs = os.listdir(file_path)
    
    #list to hold all subject faces
    faces = []
    #list to hold labels for all subjects
    labels = []
    
    #let's go through each directory and read images within it
    for dir_name in dirs:
        
        #our subject directories start with letter 's' so
        #ignore any non-relevant directories if any
        if not dir_name.startswith("s"):
            continue;
            
        #------STEP-2--------
        #extract label number of subject from dir_name
        #format of dir name = slabel
        #, so removing letter 's' from dir_name will give us label
        label = int(dir_name.replace("s", ""))
        
        #build path of directory containin images for current subject subject
        #sample subject_dir_path = "training-data/s1"
        subject_dir_path = data_folder_path + "/" + dir_name
        
        #get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)
        
        #------STEP-3--------
        #go through each image name, read image, 
        #detect face and add face to list of faces
        for image_name in subject_images_names:
            
            #ignore system files like .DS_Store
            if image_name.startswith("."):
                continue;
            
            #build image path
            #sample image path = training-data/s1/1.pgm
            image_path = subject_dir_path + "/" + image_name

            #read image
            image = cv2.imread(image_path)
            
            #display an image window to show the image 
            cv2.imshow("Training on image...", image)
            cv2.waitKey(100)
            
            #detect face
            face, rect = detect_face(image)
            
            #------STEP-4--------
            #for the purpose of this tutorial
            #we will ignore faces that are not detected
            if face is not None:
                #add face to list of faces
                faces.append(face)
                #add label for this face
                labels.append(label)
            
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    return faces, labels


################################## end Training data ##################################

################################## start face recognition###############################
def predict(test_img):
    #make a copy of the image as we don't want to chang original image
    img = test_img.copy()
    #detect face from the image
    face, rect = detect_face(img)
    if face is not None:
        #predict the image using our face recognizer 
        label= face_recognizer.predict(face)
        #get name of respective label returned by face recognizer
        name=str(label)
        student_id = name[name.find("(")+1:name.find(",")]
        label_text = "s"+str(label)
        #print student_id
        

        return student_id
    else:
        print None
################################## end face recognition###############################



################################## start drawing #####################################
#function to draw rectangle on image 
#according to given (x, y) coordinates and 
#given width and heigh
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
#function to draw text on give image starting from
#passed (x, y) coordinates. 
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
################################## end drawing #####################################



################################## start recognition function ################################
def recognition():
    #detection()
    attendance = []
    time = []
    print("Preparing data...")
    faces_path = os.path.join(settings.FILES_DIR, "faces.p")
    labels_path = os.path.join(settings.FILES_DIR, "labels.p")
    faces = pickle.load( open( faces_path, "rb" ) ) 
    labels = pickle.load( open( labels_path, "rb" ) ) 
    print("Data prepared")
    subjects=["","s1","s2","Aasif"]
    #print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))
    face_recognizer.train(faces, np.array(labels))

    print("Predicting images...")
    unknown_path = os.path.join(settings.FILES_DIR, "Unknown")
    subject_images_names = os.listdir(unknown_path)
    for image_name in subject_images_names:
        if image_name.startswith("U_"):
            
            image_path = unknown_path + "/" + image_name
            #load test images

            test_img = cv2.imread(image_path)
            #test_img2 = cv2.imread("Unknown/U_2.jpg")
            creation_time = datetime.fromtimestamp(os.path.getctime(image_path))
            #perform a prediction
            predicted_img_name = predict(test_img)
            if predicted_img_name is not None:
                attendance.append(predicted_img_name)
                #time.append(creation_time)
                cv2.imwrite(settings.FILES_DIR+"/Result/R_"+predicted_img_name+".jpg",test_img)
            #predicted_img2 = predict(test_img2)
        else:
            continue
    print("Prediction complete")
    #print image_path
    attendance = list(set(attendance))
    return attendance

################################## end recognition function ################################

