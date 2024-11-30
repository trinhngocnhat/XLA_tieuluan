import sys
import imutils
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QImage

import layout_image
import cv2
import numpy as np
import Preprocess
import math

img_path = None
Ivehicle = None

ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

n = 1

Min_char = 0.01
Max_char = 0.09

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

# mô hình KNN
npaClassifications = np.loadtxt("classificationS.txt", np.float32)
npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)
npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
kNearest = cv2.ml.KNearest_create()
kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)


class MainWindow(QtWidgets.QFrame, layout_image.Ui_Frame):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.btn_chonanh.clicked.connect(self.loadImage)
        self.btn_nhandang.clicked.connect(self.imgae_license)
        self.btn_info.setText("Mở Camera")  # Đổi tên nút thành "Mở Camera"
        self.btn_info.clicked.connect(self.openCamera)  # Kết nối nút với hàm openCamera

    def loadImage(self):
        self.img_path = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.Ivehicle = cv2.imread(self.img_path)

        # nguyen goc
        self.cv2_path = cv2.imread(self.img_path)

        self.img_goc = cv2.imread(self.img_path)
        self.setPhoto()

    def setPhoto(self):
        self.Ivehicle = imutils.resize(self.Ivehicle, width=300, height=340)
        frame = cv2.cvtColor(self.Ivehicle, cv2.COLOR_BGR2RGB)
        self.Ivehicle = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.original_img.setPixmap(QtGui.QPixmap.fromImage(self.Ivehicle))

    def openCamera(self):
        """
        Hàm mở camera sử dụng OpenCV.
        """
        cap = cv2.VideoCapture(0)  # Khởi tạo camera (0 là camera mặc định)
        if not cap.isOpened():
            print("Không thể mở camera!")
            return

        while True:
            ret, frame = cap.read()  # Đọc từng frame từ camera
            if not ret:
                print("Không thể đọc frame từ camera!")
                break

            # Hiển thị frame lên cửa sổ OpenCV
            cv2.imshow("Camera", frame)

            # Nhấn phím 'q' để thoát
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()  # Giải phóng camera
        cv2.destroyAllWindows()  # Đóng các cửa sổ OpenCV

    def imgae_license(self, img_path):
        # Tiền xử lý ảnh
        global first_line, second_line
        imgGrayscaleplate, imgThreshplate = Preprocess.preprocess(self.cv2_path)
        canny_image = cv2.Canny(imgThreshplate, 250, 255)  # Tách biên bằng canny
        kernel = np.ones((3, 3), np.uint8)
        dilated_image = cv2.dilate(canny_image, kernel, iterations=1)  # tăng sharp cho edge (Phép nở)
        # vẽ contour và lọc biển số
        contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        screenCnt = []
        for c in contours:
            peri = cv2.arcLength(c, True)  # Tính chu vi
            approx = cv2.approxPolyDP(c, 0.06 * peri, True)  # làm xấp xỉ đa giác, chỉ giữ contour có 4 cạnh
            [x, y, w, h] = cv2.boundingRect(approx.copy())
            ratio = w / h
            if len(approx) == 4:
                screenCnt.append(approx)
                cv2.putText(self.cv2_path, str(len(approx.copy())), (x, y), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)

        if not screenCnt:
            print("Không phát hiện biển số.")
        else:
            for i in screenCnt:
                cv2.drawContours(self.cv2_path, [i], -1, (0, 255, 0), 3)  # Khoanh vùng biển số xe
                # Xử lý ảnh biển số (Cắt, xoay, nhận dạng ký tự...)
                # Phần này giữ nguyên.

    # Các hàm khác giữ nguyên...


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    try:
        sys.exit(app.exec_())
    except (SystemError, SystemExit):
        app.exit()
