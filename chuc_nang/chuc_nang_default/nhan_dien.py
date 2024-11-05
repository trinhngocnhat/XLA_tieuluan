import cv2 as cv
import pytesseract

# Set up Tesseract executable path if needed (update to your installation path)
# For example, on Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the pre-trained Haar Cascade for license plate detection
plate_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_russian_plate_number.xml')


def recognize_license_plate(frame):
    # Convert the frame to grayscale for detection
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect license plates in the frame
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in plates:
        # Draw a rectangle around the detected license plate
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Crop and preprocess the detected plate for OCR
        plate_roi = gray[y:y + h, x:x + w]
        # Use Tesseract to extract text from the license plate region
        text = pytesseract.image_to_string(plate_roi, config='--psm 8')

        # Display recognized text on the video frame
        cv.putText(frame, text.strip(), (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    return frame


def livestream_license_plate():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame is read correctly, ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Process frame for license plate recognition
        frame = recognize_license_plate(frame)

        # Display the processed frame
        cv.imshow('License Plate Recognition - Press Q to Quit', frame)

        # Break the loop when 'q' is pressed
        if cv.waitKey(1) == ord('q'):
            break

    # Release the capture when everything is done
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    # Call the function
    livestream_license_plate()
