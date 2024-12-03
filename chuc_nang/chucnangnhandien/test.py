# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'license_layout.ui'
# Created by: PyQt5 UI code generator 5.15.5

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import cv2
from PyQt5.QtGui import QImage, QPixmap


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
        self.label.setStyleSheet("color: qconicalgradient(cx:0.5, cy:0.5, angle:0, "
                                 "stop:0 rgba(255, 255, 255, 255), stop:0.373979 rgba(255, 255, 255, 255), "
                                 "stop:0.373991 rgba(33, 30, 255, 255), stop:0.624018 rgba(33, 30, 255, 255), "
                                 "stop:0.624043 rgba(255, 0, 0, 255), stop:1 rgba(255, 0, 0, 255));")
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
        self.btn_info = self.create_button(self.frame_2, "Thông Tin", 880, 370)
        self.btn_chonanh = self.create_button(self.frame_2, "Chọn ảnh", 800, 320)

        # Result label
        self.lbl_result = self.create_label(self.frame_2, "result", 10, 20, 771, 741)

        # Image label for showing original image
        self.original_img = self.create_label(self.frame_2, "Ảnh bạn", 790, 20, 301, 291)

        # Input fields for vehicle license plate info
        self.let_bienso = self.create_input(self.frame_2, 880, 450, 211, 71, size=22)
        self.let_tinh = self.create_input(self.frame_2, 880, 550, 211, 41, size=14)
        self.let_gio = self.create_input(self.frame_2, 880, 630, 211, 41, size=14, bold=True)
        self.let_ngay = self.create_input(self.frame_2, 880, 710, 211, 41, size=14, bold=True)
        self.let_ten = self.create_input(self.frame_2, 880, 770, 211, 41, size=14)

        # Labels for the inputs
        self.create_label(self.frame_2, "Biển Số: ", 790, 470, 81, 31, size=10)
        self.create_label(self.frame_2, "Tỉnh", 790, 550, 81, 41, size=10)
        self.create_label(self.frame_2, "Gio", 790, 630, 81, 41, size=10)
        self.create_label(self.frame_2, "Ngày", 790, 710, 81, 31, size=10)

        # Spacer
        self.spacer = self.create_label(self.frame_2, "", 790, 610, 211, 151, bg_color="rgb(255, 255, 255)")

        self.verticalLayout.addWidget(self.frame)
        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

        # Connect buttons to their respective functions
        self.btn_chonanh.clicked.connect(self.open_image)
        self.btn_info.clicked.connect(self.open_webcam)

    def create_font(self, size, bold=False):
        """Helper function to create a font."""
        font = QtGui.QFont()
        font.setPointSize(size)
        font.setBold(bold)
        font.setWeight(75)
        return font

    def create_button(self, parent, text, x, y):
        """Helper function to create buttons."""
        button = QtWidgets.QPushButton(parent)
        button.setText(text)
        button.setGeometry(QtCore.QRect(x, y, 121, 41))
        button.setFont(self.create_font(size=11, bold=True))
        return button

    def create_label(self, parent, text, x, y, width, height, size=14, bg_color="rgb(255, 255, 255)"):
        """Helper function to create labels."""
        label = QtWidgets.QLabel(parent)
        label.setGeometry(QtCore.QRect(x, y, width, height))
        label.setText(text)
        label.setFont(self.create_font(size=size))
        label.setStyleSheet(f"background-color: {bg_color};")
        label.setFrameShape(QtWidgets.QFrame.Box)
        return label

    def create_input(self, parent, x, y, width, height, size=14, bold=False):
        """Helper function to create input fields."""
        input_field = QtWidgets.QLineEdit(parent)
        input_field.setGeometry(QtCore.QRect(x, y, width, height))
        input_field.setFont(self.create_font(size=size, bold=bold))
        input_field.setAlignment(QtCore.Qt.AlignCenter)
        input_field.setStyleSheet("background-color: rgb(255, 255, 255);")
        input_field.setText("")
        return input_field

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label.setText(_translate("Frame", "Nhận Dạng Biển Số Xe"))
        self.btn_nhandang.setText(_translate("Frame", "Nhận Dạng"))
        self.btn_info.setText(_translate("Frame", "Thông Tin"))
        self.btn_chonanh.setText(_translate("Frame", "Chọn ảnh"))
        self.lbl_result.setText(_translate("Frame", "result"))
        self.original_img.setText(_translate("Frame", "Ảnh bạn"))

    def open_image(self):
        """Open an image file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Image", "", "Images (*.png *.xpm *.jpg);;All Files (*)",
                                                   options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.original_img.setPixmap(pixmap.scaled(self.original_img.size(), QtCore.Qt.KeepAspectRatio))

    def open_webcam(self):
        """Open the webcam."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return

        self.show_webcam()

    def show_webcam(self):
        """Display webcam feed."""
        ret, frame = self.cap.read()
        if ret:
            # Convert frame to QImage format
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            pixmap = QPixmap(image)
            self.original_img.setPixmap(pixmap.scaled(self.original_img.size(), QtCore.Qt.KeepAspectRatio))

        # Continue capturing frames
        self.cap.release()
        self.cap = None


# Run the application
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
