
# Face Recognition Security App


1. You have to register and add photos of known people with their names to the database.

2. Now we start the camera. 

First it is will use face detection to detect the faces in the frame and then it will use Face
Recognition to identify the face. So in every duration of 60 seconds the program will search for the faces. If it detects unknown faces it will send a notification to the user.

To run the program :

  1. run the following codes:
     a.pip install django 
     b.pip install django-crispy-forms
     c.pip install face_recognition
    
  2. go to Face-Recognition-App/FaceRec/settings.py and enter your e-mail acount details from which the notification will be sent. 
          (Turn on the Less secure app access in your Google account)
  3. then go to login to create an account.
 
 
 Now you are ready to use the app.
   


