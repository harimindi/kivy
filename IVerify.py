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
from ocrdl import extractDL
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
        self.ids.btn_blink.text = 'Recapture'
        
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
        
        shape_predictor = './shape_predictor_68_face_landmarks.dat'
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
    
    txt = ''
    def Selection(self, text):
        lbl = self.ids['lbl_IDSelected']
        txt = '>> '+ text + ' selected'
        if lbl.opacity == 0:
            lbl.opacity = 1
            lbl.text = txt
        else:
            lbl.text = txt
    
    def idDocument(self, *args):
        global idflag
        lbl_txt = self.ids.lbl_IDSelected.text
        if 'UK Passport' in lbl_txt:
            self.parent.current = 'Passport_Screen'
            idflag = 1
        elif 'UK Driving License' in lbl_txt:
            self.parent.current = 'ukdl_Screen'
            idflag = 2

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

class UKDL(Screen):
    def ukdlSelect(self, filename):
        try:
            self.ids.img_ukdl.opacity = 1
            self.ids.img_ukdl.source = filename[0]
            self.ids.file_ukdl.opacity = 0
        except:
            pass
        global ukdlfile
        ukdlfile = filename[0]
    
    def file_browse(self):
        if self.ids.img_ukdl.source:
            self.ids.img_ukdl.source = ""
            self.ids.img_ukdl.opacity = 0

        self.ids.file_ukdl.opacity = 1

#idflag == 1 is for Passport Screen and 2 is Driving License Screen   
    def screen_change(self, *args):
        if idflag == 2:
            self.parent.current = 'addrSelect_Screen'
        else:
            self.parent.current = 'Result_Screen'

class AddrSelect(Screen):
    txt = ''
    def addrSelection(self, text):
        lbl = self.ids['lbl_Addrselected']
        txt = '>> ' + text + ' selected'
        if lbl.opacity == 0:
            lbl.opacity = 1
            lbl.text = txt
        else:
            lbl.text = txt
    
    def addrDocument(self, *args):
        lbl_txt = self.ids.lbl_Addrselected.text
        if 'UK Driving License' in lbl_txt:
            self.parent.current = 'ukdl_Screen'
        else:
            self.parent.current = 'Result_Screen'
            
class Result(Screen):
    def displaydata(self):
        # Face match result comparing passport photo and pic taken by blink
        source = '.\Blinked_Face.png'
        if idflag == 1:                     #UK Passport
            compare = passportfile
        elif idflag == 2:                   # UK Driving License
            compare = ukdlfile

        #Photo match with Blinked face
        if source != '':
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
        else:
            self.ids.txt_facematch.text = 'No Photo Taken'
        
        #extract ID document data
        if idflag == 1:
            passport = cv2.imread(passportfile)
            country,lastname,firstname,docnumber,nationality,dob,sex,doe = extractMRZ(passport)
    	#elif idflag == 2:
        else:
            ukdl = cv2.imread(ukdlfile)
            lastname,firstname,country,dob,date_of_issue,doe,docnumber,Address = extractDL(ukdl)
            nationality = 'United Kingdom'
        
        self.ids.txt_countryissue.text = country
        self.ids.txt_lastname.text = lastname
        self.ids.txt_givenname.text = firstname
        self.ids.txt_passportnum.text = docnumber
        self.ids.txt_nationality.text = nationality
        self.ids.txt_dob.text = dob
        self.ids.txt_sex.text = sex
        self.ids.txt_doe.text = doe
    
    def close_App(self, *args):
        os.remove('.\Blinked_Face.png')
        App.get_running_app().stop()
        
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
kivy = Builder.load_file("Form2.kv")
class Form2(App):
    def build(self):
        return kivy
if __name__=='__main__':
    Form2().run()
