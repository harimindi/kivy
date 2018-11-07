# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 20:48:24 2018

@author: hari
"""
import kivy.core.text
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream, FPS, VideoStream
from imutils import face_utils
import imutils
import numpy as np
import time
import dlib
import cv2

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.lang.builder import Builder

Builder.load_string('''
<Button>:
    background_normal: ''
    #background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: (0.733, 0.145, 0.145,1) if self.state=='normal' else (0,.7,.7,1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]
    background_color: 0.733, 0.145, 0.145,1.8
    font_size: 40
    color: 1,1,1,1
    size_hint: 0.3, 0.1
<Layout>:
        
    orientation: 'vertical'
    #canvas.before:
        #Color:
            #rgba:0.161, 0.561, 0.761,1
        #Rectangle:
            #pos: self.pos
            #size: self.size
    KivyCamera:
        id: kivycam
        #resolution: (300, 300)
        #play: False
    
    Button:
        id: blink
        text: "Blink"
        pos_hint: {'x':.1, 'y':.1}
        on_press: root.onCameraClick()
    Button:
        id: next
        text: "Quit"
        pos_hint: {'x':.6, 'y':.1}
        on_press: root.doexit()
''')

class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None

    def start(self, capture, fps=30):
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):
        return_value, frame = self.capture.read()
        if return_value:
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()


capture = None

class Layout(BoxLayout):
    def init_camtest(self):
        pass

    def onCameraClick(self, *args):
        #blinkbtn = self.ids['blink']
        #camera.export_to_png("C:/Hari Docs/Kivy/pic.png")
        #print('Picure Taken')
        global capture
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
        
        shape_predictor = 'C:\Hari Docs\python\Installers\shape_predictor_68_face_landmarks.dat'
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(shape_predictor)
        
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
        
        print("[INFO] starting video stream thread...")
        capture = VideoStream(src=0).start()
        self.ids.kivycam.start(capture)
        fileStream = False
        time.sleep(1.0)
        #fps= FPS().start()
        #cv2.namedWindow('Capture', cv2.WINDOW_NORMAL)
        
        while True:
            frame = capture.read()
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
                        print('Blink detected, stay steady and look at the camera...!')
                        while TOTAL <= 3:
                            frame = capture.read()
                            img_name =  'opencv_frame_{}.png'.format(TOTAL)
                            cv2.imwrite(img_name, frame)    
                            print('{} written'.format(img_name))
                            TOTAL += 1
                            time.sleep(1)
                        #fps.stop()
                        cv2.destroyAllWindows()
                        blink.stop()
                        #vs.stop()
                        exit()
                    COUNTER = 0  # reset the eye frame counter
            
    def doexit(self):
        global capture
        if capture != None:
            capture.release()
            capture = None
        EventLoop.close()

class myKivy(App):
    def build(self):
        homeWin = Layout()
        homeWin.init_camtest()
        return homeWin

if __name__=='__main__':
    myKivy().run()
