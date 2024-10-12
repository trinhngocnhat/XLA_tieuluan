
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

# Các thông số xử lý ảnh
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9
Min_char = 0.01
Max_char = 0.09
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

# Mô hình KNN
npaClassifications = np.loadtxt("classificationS.txt", np.float32)
npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)
npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
kNearest = cv2.ml.KNearest_create()
kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

class MainWindow(QtWidgets.QFrame, layout_image.Ui_Frame):
    def __init__(self,*args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.btn_chonanh.clicked.connect(self.loadImage)
        self.btn_nhandang.clicked.connect(self.imgae_license)



    def loadImage(self):
        self.img_path = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.Ivehicle = cv2.imread(self.img_path)
        self.cv2_path = cv2.imread(self.img_path)
        self.img_goc = cv2.imread(self.img_path)
        self.setPhoto()

    def setPhoto(self):
        self.Ivehicle = imutils.resize(self.Ivehicle, width=300, height=340)
        frame = cv2.cvtColor(self.Ivehicle, cv2.COLOR_BGR2RGB)
        self.Ivehicle = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.original_img.setPixmap(QtGui.QPixmap.fromImage(self.Ivehicle))

    def imgae_license(self):
        global first_line, second_line
        imgGrayscaleplate, imgThreshplate = Preprocess.preprocess(self.cv2_path)
        canny_image = cv2.Canny(imgThreshplate, 250, 255)
        kernel = np.ones((3, 3), np.uint8)
        dilated_image = cv2.dilate(canny_image, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        screenCnt = []
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.06 * peri, True)
            [x, y, w, h] = cv2.boundingRect(approx.copy())
            ratio = w / h
            if (len(approx) == 4):
                screenCnt.append(approx)
                cv2.putText(self.cv2_path, str(len(approx.copy())), (x, y), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)

        if screenCnt is None:
            detected = 0
            print("No plate detected")
        else:
            detected = 1

        if detected == 1:
            for i in screenCnt:
                cv2.drawContours(self.cv2_path, [i], -1, (0, 255, 0), 3)

                # Tìm góc xoay ảnh
                (x1, y1) = i[0, 0]
                (x2, y2) = i[1, 0]
                (x3, y3) = i[2, 0]
                (x4, y4) = i[3, 0]
                array = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                sorted_array = sorted(array, key=lambda x: x[1])
                (x1, y1) = sorted_array[0]
                (x2, y2) = sorted_array[1]
                doi = abs(y1 - y2)
                ke = abs(x1 - x2)
                angle = math.atan(doi / ke) * (180.0 / math.pi)

                # Cắt biển số ra khỏi ảnh và xoay ảnh
                mask = np.zeros(imgGrayscaleplate.shape, np.uint8)
                new_image = cv2.drawContours(mask, [i], 0, 255, -1)
                (x, y) = np.where(mask == 255)
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))

                roi = self.cv2_path[topx:bottomx, topy:bottomy]
                imgThresh = imgThreshplate[topx:bottomx, topy:bottomy]
                ptPlateCenter = (bottomx - topx) / 2, (bottomy - topy) / 2
                rotationMatrix = cv2.getRotationMatrix2D(ptPlateCenter, -angle, 1.0) if x1 < x2 else cv2.getRotationMatrix2D(ptPlateCenter, angle, 1.0)

                roi = cv2.warpAffine(roi, rotationMatrix, (bottomy - topy, bottomx - topx))
                imgThresh = cv2.warpAffine(imgThresh, rotationMatrix, (bottomy - topy, bottomx - topy))
                roi = cv2.resize(roi, (0, 0), fx=3, fy=3)
                imgThresh = cv2.resize(imgThresh, (0, 0), fx=3, fy=3)

                # Tiền xử lý ảnh đề phân đoạn kí tự
                kerel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                thre_mor = cv2.morphologyEx(imgThresh, cv2.MORPH_DILATE, kerel3)
                cont, hier = cv2.findContours(thre_mor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Lọc vùng kí tự
                char_x_ind = {}
                char_x = []
                height, width, _ = roi.shape
                roiarea = height * width

                for ind, cnt in enumerate(cont):
                    (x, y, w, h) = cv2.boundingRect(cont[ind])
                    ratiochar = w / h
                    char_area = w * h

                    if (Min_char * roiarea < char_area < Max_char * roiarea) and (0.25 < ratiochar < 0.7):
                        if x in char_x:
                            x = x + 1
                        char_x.append(x)
                        char_x_ind[x] = ind
                char_x = sorted(char_x)
                strFinalString = ""
                first_line = ""
                second_line = ""

                for i in char_x:
                    (x, y, w, h) = cv2.boundingRect(cont[char_x_ind[i]])
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    imgROI = thre_mor[y:y + h, x:x + w]
                    imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
                    npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
                    npaROIResized = np.float32(npaROIResized)
                    _, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k=3)
                    strCurrentChar = str(chr(int(npaResults[0][0])))
                    cv2.putText(roi, strCurrentChar, (x, y + 50), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 0), 3)

                    if (y < height / 3):
                        first_line = first_line + strCurrentChar
                    else:
                        second_line = second_line + strCurrentChar

                print("\n License Plate " + str(n) + " is: " + first_line + " - " + second_line + "\n")
                roi = cv2.resize(roi, None, fx=0.75, fy=0.75)

                self.let_bienso.setText('{}-{}'.format(first_line, second_line))
                self.display_license_plate_info(first_line + second_line)

                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                self.Ivehicle = QImage(roi, roi.shape[1], roi.shape[0], roi.strides[0], QImage.Format_RGB888)
                self.drawing_img.setPixmap(QtGui.QPixmap.fromImage(self.Ivehicle))

    def display_license_plate_info(self, license_plate):
        """
        Hàm hiển thị thông tin biển số xe và loại biển số
        """
        # Phân tách biển số thành các phần
        in4 = license_plate[:2]  # Hai ký tự đầu tiên
        in5 = int(in4)  # Chuyển đổi thành số

        # Từ điển chứa mã và tên tỉnh
        lang = {
            11: 'Cao Bằng', 12: 'Lạng Sơn', 14: 'Quảng Ninh', 15: 'Hải Phòng', 
            17: 'Thái Bình', 18: 'Nam Định', 19: 'Phú Thọ', 20: 'Thái Nguyên', 
            21: 'Yên Bái', 22: 'Tuyên Quang', 23: 'Hà Giang', 24: 'Lao Cai', 
            25: 'Lai Châu', 26: 'Sơn La', 27: 'Điện Biên', 28: 'Hoà Bình', 
            29: 'Hà Nội', 30: 'HN', 31: 'Hà Nội', 32: 'Hà Nội', 
            33: 'Hà Nội', 40: 'Hà Nội', 34: 'Hải Dương', 35: 'Ninh Bình', 
            36: 'Thanh Hóa', 37: 'Nghệ An', 38: 'Hà Tĩnh', 43: 'Đà Nẵng', 
            47: 'Dak Lak', 48: 'Đắc Nông', 49: 'Lâm Đồng', 50: 'HCM', 
            51: 'HCM', 52: 'HCM', 53: 'HCM', 54: 'HCM', 55: 'HCM', 
            56: 'HCM', 57: 'HCM', 58: 'HCM', 59: 'HCM', 60: 'Đồng Nai', 
            61: 'Bình Dương', 62: 'Long An', 63: 'Tiền Giang', 
            64: 'Vĩnh Long', 65: 'Cần Thơ', 66: 'Đồng Tháp', 
            67: 'An Giang', 68: 'Kiên Giang', 69: 'Cà Mau', 
            70: 'Tây Ninh', 71: 'Bến Tre', 72: 'Vũng Tàu', 
            73: 'Quảng Bình', 74: 'Quảng Trị', 75: 'Huế', 
            76: 'Quảng Ngãi', 77: 'Bình Định', 78: 'Phú Yên', 
            79: 'Nha Trang', 81: 'Gia Lai', 82: 'Kon Tum', 
            83: 'Sóc Trăng', 84: 'Trà Vinh', 85: 'Ninh Thuận', 
            86: 'Bình Thuận', 88: 'Vĩnh Phúc', 89: 'Hưng Yên', 
            90: 'Hà Nam', 92: 'Quảng Nam', 93: 'Bình Phước', 
            94: 'Bạc Liêu', 95: 'Hậu Giang', 97: 'Bắc Cạn', 
            98: 'Bắc Giang', 99: 'Bắc Ninh',
        }

        # Xác định tỉnh từ biển số
        province_name = lang.get(in5, "Không xác định")

        # Xác định loại biển số
        plate_type = ""
        if license_plate.startswith("80"):
            plate_type = "Công an"
        elif license_plate.startswith("81"):
            plate_type = "Quân đội"
        elif license_plate.startswith("82"):
            plate_type = "Sở hữu cá nhân"
        elif license_plate.startswith("83"):
            plate_type = "Hợp đồng"
        elif license_plate.startswith("84"):
            plate_type = "Xe nước ngoài"
        else:
            plate_type = "Loại khác"

        # Cập nhật giao diện với thông tin biển số
        self.let_bienso.setText(license_plate)
        self.let_tinh.setText(province_name)
        self.let_loai_bien.setText(plate_type)  # Cần thêm một QLabel cho loại biển số trong giao diện


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
