import cv2
import pytesseract
from pytesseract import Output

# Path to the tesseract executable (adjust according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load Haar cascade for license plate detection (or replace with a pre-trained model)
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")


# Function to detect and recognize license plates
def detect_and_recognize_license_plate(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect license plates
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 20))

    for (x, y, w, h) in plates:
        # Draw a rectangle around detected plates
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop the detected plate for OCR
        plate = gray[y:y + h, x:x + w]

        # Recognize text from the cropped plate
        config = "--oem 3 --psm 7"
        text = pytesseract.image_to_string(plate, config=config)

        # Display the recognized text
        cv2.putText(frame, text.strip(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame


# Initialize video capture for livestream (0 for the default camera)
cap = cv2.VideoCapture(0)

# Stream video and apply license plate detection
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect and recognize license plates in the frame
    processed_frame = detect_and_recognize_license_plate(frame)

    # Display the frame
    cv2.imshow("License Plate Recognition", processed_frame)

    # Press 'q' to exit the livestream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
