from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
import cv2
from PyQt5.QtGui import QImage, QPixmap
from ultralytics import YOLO
import numpy as np

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(1117, 863)

        # Main layout
        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")

        # Main frame
        self.frame = QtWidgets.QFrame(Frame)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Title label
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(180, 10, 781, 41))
        self.label.setFont(self.create_font(size=22, bold=True))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        # Secondary frame for buttons and images
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 60, 1101, 781))
        self.frame_2.setFont(self.create_font(size=20, bold=True))
        self.frame_2.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:0.701199, y1:1, x2:0.716, "
                                   "y2:0, stop:0 rgba(79, 200, 232, 255), stop:1 rgba(255, 255, 255, 255));")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # Buttons
        self.btn_nhandang = self.create_button(self.frame_2, "Nhận Dạng", 960, 320)
        self.btn_info = self.create_button(self.frame_2, "Webcam", 880, 370)
        self.btn_chonanh = self.create_button(self.frame_2, "Chọn file", 800, 320)

        # Result label (where the webcam feed or image will be displayed)
        self.lbl_result = self.create_label(self.frame_2, "result", 10, 20, 771, 741)

        # Add the main frame to the layout
        self.verticalLayout.addWidget(self.frame)

        # Initialize webcam running state
        self.is_webcam_running = False

        # Connect buttons to their respective functions
        self.btn_chonanh.clicked.connect(self.open_image)
        self.btn_info.clicked.connect(self.open_webcam)

        # Load YOLO model
        self.yolo_model = YOLO('C:/Users/ASUS/Documents/GitHub/XLA_tieuluan/runs/detect/train10/weights/best.pt')
        self.char_model = YOLO("C:/Users/ASUS/Documents/GitHub/XLA_tieuluan/runs/mnist_training/weights/best.pt")
    def create_font(self, size, bold=False):
        font = QtGui.QFont()
        font.setPointSize(size)
        font.setBold(bold)
        font.setWeight(75)
        return font

    def create_button(self, parent, text, x, y):
        button = QtWidgets.QPushButton(parent)
        button.setText(text)
        button.setGeometry(QtCore.QRect(x, y, 121, 41))
        button.setFont(self.create_font(size=11, bold=True))
        return button

    def create_label(self, parent, text, x, y, width, height, size=14, bg_color="rgb(255, 255, 255)"):
        label = QtWidgets.QLabel(parent)
        label.setGeometry(QtCore.QRect(x, y, width, height))
        label.setText(text)
        label.setFont(self.create_font(size=size))
        label.setStyleSheet(f"background-color: {bg_color};")
        label.setFrameShape(QtWidgets.QFrame.Box)
        return label

    def create_input(self, parent, x, y, width, height, size=14, bold=False):
        input_field = QtWidgets.QLineEdit(parent)
        input_field.setGeometry(QtCore.QRect(x, y, width, height))
        input_field.setFont(self.create_font(size=size, bold=bold))
        input_field.setAlignment(QtCore.Qt.AlignCenter)
        input_field.setStyleSheet("background-color: rgb(255, 255, 255);")
        input_field.setText("")
        return input_field

    def open_image(self):
        """Stop webcam and open an image file."""
        if self.is_webcam_running:
            self.stop_webcam()

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Image", "", "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.lbl_result.setPixmap(pixmap.scaled(self.lbl_result.size(), QtCore.Qt.KeepAspectRatio))

            # Run YOLO on the image
            self.run_yolo(file_name)

    def open_webcam(self):
        """Stop image display and open the webcam."""
        if self.is_webcam_running:
            return  # Webcam is already running

        self.lbl_result.clear()  # Clear any image displayed

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return

        self.is_webcam_running = True
        self.show_webcam()

    def show_webcam(self):
        """Display webcam feed inside the lbl_result and run YOLO."""
        ret, frame = self.cap.read()
        if ret:
            # Run YOLO on the webcam feed
            self.run_yolo_webcam(frame)

            # Convert frame to QImage format
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            pixmap = QPixmap(image)
            self.lbl_result.setPixmap(pixmap.scaled(self.lbl_result.size(), QtCore.Qt.KeepAspectRatio))

        # Continue capturing frames
        if self.cap.isOpened():
            QTimer.singleShot(10, self.show_webcam)  # Re-run show_webcam every 10ms

    def stop_webcam(self):
        """Stop the webcam."""
        if self.cap.isOpened():
            self.cap.release()
            self.cap = None
            self.is_webcam_running = False
            self.lbl_result.clear()  # Clear the webcam feed from the result label

        def detect_license_plate(self):
            """Detect the license plate and letters inside."""
            image = cv2.imread(self.image_path)
            results = self.plate_model(image)

            for result in results:
                for box in result.boxes.xyxy:
                    x1, y1, x2, y2 = map(int, box)
                    cropped_plate = image[y1:y2, x1:x2]
                    char_results = self.char_model(cropped_plate)

                    detected_text = self.extract_characters(char_results)
                    self.let_bienso.setText(detected_text)

        def extract_characters(self, results):
            """Extract characters from the detected results."""
            detected_text = ""
            for result in results:
                labels = result.boxes.cls.cpu().numpy()
                sorted_indices = result.boxes.xyxy[:, 0].argsort()
                detected_text = "".join([chr(int(labels[i]) + 65) for i in sorted_indices])
            return detected_text

    # Run the application
    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Frame = QtWidgets.QFrame()
        ui = Ui_Frame()
        ui.setupUi(Frame)
        Frame.show()
        sys.exit(app.exec_())