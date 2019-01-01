import cv2
import numpy as np
import os
import tempfile
import re
from datetime import datetime
from PIL import Image
import pytesseract

def clean_image(crop):

    img_clean = cv2.resize(crop, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
    img_clean = cv2.bilateralFilter(img_clean, 9, 75,75)

    gray = cv2.cvtColor(img_clean, cv2.COLOR_BGR2GRAY)

    #Thesholding
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return gray

# https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/ 
def align_resize(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    cv2.imwrite(temp_filename, rotated)

    print("[INFO] angle: {:.3f}".format(angle))

    #Resizing image
    im = Image.open(temp_filename)
    im_resized = im.resize((640,480), Image.ANTIALIAS)
    im_resized.save(temp_filename, dpi=(300, 300))  # best for OCR

    image_align_resize = cv2.imread(temp_filename)
    return image_align_resize

def text_extract(txt1, txt2):
    textlines = txt1.replace('\n\n', '\n')
    textlines = textlines.split('\n')

    #Initialize---
    lastname = ''
    firstname = ''
    middlename = ''
    country = ''
    dob = ''
    date_of_issue = ''
    date_of_expiry = ''
    DL_number = ''
    Address = ''

    match = re.search('\d',textlines[2]) #check if 3rd line has middlename 
    if not match:
        #print('There are Digits')
        middlename = textlines.pop(2)
        middlename = ''.join(re.findall('[A-Z\s]',middlename))
    
    lastname = ''.join(re.findall('[A-Z]',textlines[0]))
    firstname = ''.join(re.findall('[A-Z\s]',textlines[1]))
    if middlename:
        firstname = firstname + ' ' + middlename

    dob_match = re.search(r'\d{2}.\d{2}.\d{4}', textlines[2])
    dob = datetime.strptime(dob_match.group(), '%d.%m.%Y').strftime('%d-%m-%Y')

    char_pos,_ = re.search('[A-Z]', textlines[2]).span(0)
    country = textlines[2][char_pos:]

    doi_match = re.search(r'\d{2}.\d{2}.\d{4}', textlines[3])
    date_of_issue = datetime.strptime(doi_match.group(),'%d.%m.%Y').strftime('%d-%m-%Y')

    doe_match = re.search(r'\d{2}.\d{2}.\d{4}', textlines[4])
    date_of_expiry = datetime.strptime(doe_match.group(),'%d.%m.%Y').strftime('%d-%m-%Y')

    DL_number = textlines[5]
    m = re.search('[A-Z]',DL_number)
    pos = (m.start())
    DL_number = DL_number[pos:pos+19]
    
    Address = ' '.join(txt2.split('\n'))
    return lastname,firstname,country,dob,date_of_issue,date_of_expiry,DL_number, Address


def extractDL(ukdl):
    image = ukdl
    image_resize = align_resize(image)
        ### UK DRIVING LICENSE
    name_image = name_image[60:140,180:400]
    dob_country_image = new_image[141:170,180:500]
    name_country_dob_doi_doe_dl = image_resize[60:250, 180:600]
    address = image_resize[320:365, 220:600]
    #cv2.imshow('Crop',crop_image)
    #cv2.waitKey(0)
    name_country_dob_doi_doe_dl_clean = clean_image(name_country_dob_doi_doe_dl)
    address_clean = clean_image(address)
    addr_image = clean_image(addr_image)
    text1 = pytesseract.image_to_string(name_country_dob_doi_doe_dl_clean)
    text2 = pytesseract.image_to_string(address_clean)
    #print(text)
    lastname,firstname,country,dob,date_of_issue,date_of_expiry,DL_number, Address = text_extract(text1, text2)

    print('LastName - {}\nFirstName - {}\nCountry - {}\nDate of Birth - {}\nDate of Issue - {}\nDate of Expiry - {}\nDL Number - {}\nAddres - {}'.format(lastname,firstname,country,dob,date_of_issue,date_of_expiry,DL_number, Address))

    '''     ###QATAR DRIVING LICENSE
    id_dob_doe = image_resize[150:280, 180:400]
    country = image_resize[300:350, 5:400]
    name = image_resize[430:480, :500]
    id_dob_doe_clean = clean_image(id_dob_doe)
    country_clean = clean_image(country)
    name_clean = clean_image(name)
    cv2.imshow('Crop', name_clean)
    cv2.waitKey(0)
    text1 = pytesseract.image_to_string(id_dob_doe_clean)
    text2 = pytesseract.image_to_string(country)
    text3 = pytesseract.image_to_string(name_clean)
    print(text1, text2, text3)
    '''
    return lastname,firstname,country,dob,date_of_issue,date_of_expiry,DL_number, Address