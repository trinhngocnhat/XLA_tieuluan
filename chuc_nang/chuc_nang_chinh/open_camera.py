import numpy as np
import cv2 as cv

def livestream():
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

        # Flip the frame horizontally
        flipped_frame = cv.flip(frame, 1)

        # Display the flipped frame
        cv.imshow('Livestream - Press Q to Quit', flipped_frame)

        # Break the loop when 'q' is pressed
        if cv.waitKey(1) == ord('q'):
            break

    # Release the capture when everything is done
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    # Call the function
    livestream()
