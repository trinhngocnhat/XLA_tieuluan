from ultralytics import YOLO
import cv2

# Load the trained YOLO model
yolo_model = YOLO('C:/Users/ASUS/Documents/GitHub/XLA_tieuluan/runs/detect/train10/weights/best.pt')  # Replace with your YOLO model file path

# Open the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Perform YOLO prediction on the current frame
    results = yolo_model(frame)

    # Process each detected object
    for result in results:
        for box in result.boxes:
            # Extract the bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # x1, y1, x2, y2

            # Draw bounding box around the detected object
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green color

            # Optional: You can display the label of the detected object
            label = f"{result.names[int(box.cls)]}"  # Class name from the result
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with YOLO detection annotations
    cv2.imshow('YOLO Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
