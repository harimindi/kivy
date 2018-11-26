# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import numpy as np

#contruct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True,
                help = "Path to Input Image")
args = vars(ap.parse_args())
file = args["input"]
path = os.path.splitext(file)[0]
image = cv2.imread(file)

#preprocess image for tesseract
img_clean = cv2.resize(image, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
img_clean = cv2.bilateralFilter(img_clean, 9, 75,75)

#convert to gray
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Thesholding
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  

text = pytesseract.image_to_string(gray)
print(text)
