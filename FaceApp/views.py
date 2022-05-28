from os import access
from django.shortcuts import render,redirect

from .models import Gallary
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
import face_recognition
import cv2
import numpy as np
import time

from django.conf import settings
from django.core.mail import send_mail



name = ""
def home(request):
    return render(request,'Home.html')

def opencam(request):
    try:
        while(True):
            person = Gallary.objects.filter(user=request.user)
            usern = request.user
            person_data = person.__len__()
    
            if(person_data <= 0):
                vid = cv2.VideoCapture(0)
                while(True):
                    ret, frame = vid.read()
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                vid.release()
                cv2.destroyAllWindows()   
                return render(request,"home.html",{"context":"Empty DataBase"})
    
            timeout = 20   # [seconds]
            timeout_start = time.time()
            video_capture = cv2.VideoCapture(0)
            process_frame = True
            face_locations=[]
            All_faces = []
            known_face_names = []
            known_face_encodings = []
            for face in person:
                All_faces.append(face.image)
                known_face_names.append(face.title)
        
            result, image = video_capture.read()
            d = {}
            for i in range(len(All_faces)):
                k = face_recognition.load_image_file(All_faces[i])
                d["encoding{0}".format(i)] = face_recognition.face_encodings(k)[0]
                known_face_encodings.append(d["encoding{0}".format(i)])

            
            name = "notfound"
            # face_locations = []
            face_encodings = []
            face_names = []
            # process_frame = True


            while time.time() < timeout_start + timeout:
                ret, frame = video_capture.read()
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]

                if process_frame:
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                            
                        face_names.append(name)

                process_frame = not process_frame

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return render(request,"home.html",{"context" : "CAMERA TURNED OFF"})
                    

            
            if name.lower() == "unknown":
                if result:
                    #cv2.imshow("IMG", image)
                    img2 = cv2.imwrite("IMG.png", image)
                    #cv2.destroyAllWindows()
                subject = 'welcome to Face Detecting System'
                message = f"Hi {usern}, This Person Is Not Register"
                
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [usern.email]
                send_mail( subject, message, email_from, recipient_list )
                #return render(request,"home.html",{"context" : "Face Not Found In DataBase"})

    except KeyboardInterrupt:
        pass


    if name.lower() == "notfound":
        return render(request,"home.html",{"context" : "Face Not Detect In Camera"})
    print(name.lower)

    
    
    return render(request,"home.html",{"name" : name})




def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})



def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")


def addimage(request):
    if request.method == "POST":
        gallary = Gallary(
            user=request.user,
            title = request.POST['name'],
            image = request.FILES['img']
        )
        gallary.save()
    return render(request,'AddImage.html')