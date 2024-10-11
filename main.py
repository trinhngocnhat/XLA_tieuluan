import cv2
import pytesseract
import numpy as np
import imutils
from imutils.contours import sort_contours
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply bilateral filter to reduce noise while keeping edges sharp
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # Edge detection
    edged = cv2.Canny(gray, 30, 200)

    # Find contours based on edges detected
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    license_plate = None

    for c in cnts:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # The license plate should be a rectangle (4 sides)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            license_plate = image[y:y + h, x:x + w]
            return license_plate

    return None

def preprocess_plate(plate_img):
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    # Apply threshold to get binary image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def recognize_text(preprocessed_img):
    config = '-l eng --oem 1 --psm 7'  # OEM and PSM settings can be adjusted
    text = pytesseract.image_to_string(preprocessed_img, config=config)
    # Clean the text
    text = ''.join(e for e in text if e.isalnum())
    return text

