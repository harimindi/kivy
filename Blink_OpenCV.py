# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A+B)/(2.0*C)
    return ear

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3
COUNTER = 0
TOTAL = 0

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
shape_predictor = 'C:\Hari Docs\python\Installers\shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']        

print("[INFO] starting video stream thread...")
capture = VideoStream(src=0).start()
#capture = cv2.VideoCapture(0)
fileStream = False
time.sleep(1.0)

cv2.namedWindow('Capture', cv2.WINDOW_NORMAL)
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
                TOTAL +=1
                frame = capture.read()
                time.sleep(1)
                img_name = 'Photo_{}.png'.format(TOTAL)
                cv2.imwrite(img_name, frame)
                print('{} Photo taken...'.format(TOTAL))
                #capture.stop()
                #cv2.destroyWindow('Capture')
            COUNTER = 0
        #break
    cv2.imshow('Frame', capture)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
#capture.stop()

        

