#Import for Blink Detection
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream, FPS, VideoStream
from imutils import face_utils
import imutils
import os
import numpy as np
import time
import dlib
import cv2
#imports for passport text extraction and face match
from mrzparser import extractMRZ
import face_recognition
#Imports for Kivy UI
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from KivyCalendar import DatePicker
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup


class MainScreen(Screen):
    #from kivy.properties import ObjectProperty
    #theTxt = ObjectProperty(None)
    pass
    '''
    def build(self):
        kivy = Builder.load_file('IVerify.kv')
        return kivy
    
    def show_calendar(self):
        datePicker = CustomDatePicker()
        datePicker.show_popup(1, .3)
    '''    
class BlinkPhoto(Screen):
    def onCameraClick(self, *args):
        global blink_face #Final output of roi image is stored in this variable to be used for further OCR on another class

        image = self.ids['img_blink']
        lbl = self.ids['lbl_blink']
        
        def eye_aspect_ratio(eye):
            A = dist.euclidean(eye[1], eye[5])
            B = dist.euclidean(eye[2], eye[4])
            C = dist.euclidean(eye[0], eye[3])
            ear = (A + B) / (2.0 * C)
            return ear
        
        EYE_AR_THRESH = 0.3
        EYE_AR_CONSEC_FRAMES = 3
         
        # initialize the frame counters and the total number of blinks
        COUNTER = 0
        TOTAL = 1
        
        shape_predictor = 'F:/Data_Science/Python3/shape_predictor_68_face_landmarks.dat'
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(shape_predictor)
        
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
        
        #print("[INFO] starting video stream thread...")
        vs = VideoStream(src=0).start()
        fileStream = False
        time.sleep(1.0)
        cv2.namedWindow('Capture', cv2.WINDOW_NORMAL)
        flag = 1
        while (flag == 1):
            frame = vs.read()
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
            rects = detector(gray, 0)
            
            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
         
                ear = (leftEAR + rightEAR) / 2.0
                
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                
                if ear < EYE_AR_THRESH:
                    COUNTER += 1
                else:
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        #print('Blink detected, stay steady and look at the camera...!')
                        frame = vs.read()
                        time.sleep(5) 
                        img_name =  'Blinked_Face.png'
                        cv2.imwrite(img_name, frame)    
                        #print('{} written'.format(img_name))
                        flag = 0                        
                    COUNTER = 0  # reset the eye frame counter
            cv2.imshow('Capture', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        vs.stop()
        cv2.destroyAllWindows()
        if lbl.opacity == 1:
            lbl.opacity = 0
            image.opacity = 1
            image.source = img_name
            #cv2.imwrite('blinkface.png', img_name)
    
class IDSelect(Screen):
    def Selection(self, *args):
        lbl = self.ids['lbl_IDSelected']
        txt = self.text
        if lbl.opacity == 0:
            lbl.opacity = 1
            lbl.text = txt

    
class PassportScreen(Screen):
    def ImageSelect(self, filename):
        
        try:
            self.ids.img_passport.opacity = 1
            self.ids.img_passport.source = filename[0]
            self.ids.file_passport.opacity = 0
        except:
            pass
        global passportfile
        passportfile = filename[0]
    
    def file_browse(self):
        if self.ids.img_passport.source:
            self.ids.img_passport.source = ""
            self.ids.img_passport.opacity = 0

        self.ids.file_passport.opacity = 1
    
class Result(Screen):
    def displaydata(self):
        passport = cv2.imread(passportfile)
        # Face match result comparing passport photo and pic taken by blink
        source = '.\Blinked_Face.png'
        compare = passportfile				
        picture_of_me = face_recognition.load_image_file(source)
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

        compare_pic = face_recognition.load_image_file(compare)
        compare_face_encoding = face_recognition.face_encodings(compare_pic)[0]

        facematch = face_recognition.compare_faces([my_face_encoding], compare_face_encoding)

        if facematch[0] == True:
            print('Photo Matched')
            self.ids.txt_facematch.text = 'Face Recognized'
        else:
            print('No Match')
            self.ids.txt_facematch.text = 'Face Not Recognized'

        p1,p2,p3,p4,p5,p6,p7,p8 = extractMRZ(passport)
        self.ids.txt_countryissue.text = p1
        self.ids.txt_lastname.text = p2
        self.ids.txt_givenname.text = p3
        self.ids.txt_passportnum.text = p4
        self.ids.txt_nationality.text = p5
        self.ids.txt_dob.text = p6
        self.ids.txt_sex.text = p7
        self.ids.txt_doe.text = p8
    	
class ScreenManagement(ScreenManager):
    pass

'''
class CustomDatePicker(DatePicker):

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s.%s.%s" % tuple(self.cal.active_date)
        self.focus = False
        App.get_running_app().root.ids.txt_DOB.text = self.text
'''
kivy = Builder.load_file("IVerify.kv")
class IVerify(App):
    def build(self):
        return kivy
if __name__=='__main__':
    IVerify().run()
