# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import numpy as np

def textparse(text):
    country = text[2:5]
    names = text[5:44]
    docnumber = text[44:54]
    checkdigit1 = text[54:55]
    nationality = text[55:58]
    dob_raw = text[58:64]
    checkdigit2 = text[64:65]
    sex = text[65:66]
    expiry_raw = text[66:72]
    checkdigit3 = text[72:73]
    personalnum_raw = text[73:87]
    checkdigit4 = text[87:88]
    checkdigit5 = text[88:89]
    names = names.split('<<')
    lastname = names[0]
    givenname = names[1]
    print('IssuingCountry: {}\nLastName: {}\nGivenName: {}\nDocumentNumber: {}\nNationality: {}\nDate of Birth: {}\nSex: {}\nDate of Expiry: {}'.format(country,lastname, givenname,docnumber,nationality,dob_raw, sex,expiry_raw))
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

ocr = pytesseract.image_to_string(gray)
print(ocr)
textparse(ocr)

    #print(lastname, givenname)
    #print(docnumber)
    #print(checkdigit1)
    #print(nationality)
    #print(dob_raw)
    #print(checkdigit2)
    #print(sex)
    #print(expiry_raw)

#print ('Number of Lines: {}'.format(len(text.split('\n'))))
#[print(len(line)) for line in text.split('\n')]
