from tkinter import filedialog, messagebox
import cv2
from chuc_nang.chuc_nang_default.nhan_dien import \
    recognize_license_plate  # Import the function for license plate recognition


def chon_hinh_anh():
    """ Allow user to select an image file and process it to recognize license plates. """
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        # Read the image from file
        image = cv2.imread(file_path)

        if image is None:
            messagebox.showerror("Lỗi", "Không thể mở hoặc đọc tệp ảnh.")
            return None

        # Perform License Plate Detection and OCR
        image_with_plates = recognize_license_plate(image)

        # Display the processed image with rectangles drawn around detected license plates
        cv2.imshow('License Plate Recognition', image_with_plates)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()

        # Return the processed image
        return image_with_plates
    else:
        messagebox.showwarning("Cảnh báo", "Bạn chưa chọn ảnh nào.")
        return None
