import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up Tesseract executable path if needed (update to your installation path)
# Example: on Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the pre-trained Haar Cascade for license plate detection
cascade_path = cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml'

# Check if the cascade file exists at the specified path
if not os.path.exists(cascade_path):
    raise IOError(f"Haar cascade for license plate not found at {cascade_path}")

plate_cascade = cv2.CascadeClassifier(cascade_path)

# Check if Haar Cascade is loaded properly
if plate_cascade.empty():
    raise IOError("Failed to load Haar cascade for license plate detection.")

def recognize_license_plate(frame):
    """ Recognize license plates in a frame and perform OCR on them. """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect license plates in the frame
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in plates:
        # Draw a red rectangle around the detected license plate
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red color for rectangle

        # Crop and preprocess the detected plate for OCR
        plate_roi = gray[y:y + h, x:x + w]
        text = pytesseract.image_to_string(plate_roi, config='--psm 8')

        # Display recognized text on the video frame
        cv2.putText(frame, text.strip(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)  # Red text

    return frame
