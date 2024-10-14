import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

# Hàm để chọn file
def choose_file():
    # Mở hộp thoại để chọn file
    file_path = filedialog.askopenfilename(
        title="Chọn hình ảnh",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        # Đọc và hiển thị hình ảnh
        image = cv2.imread(file_path)
        display_image(image)

# Hàm hiển thị hình ảnh bằng OpenCV
def display_image(image):
    # Chuyển đổi hình ảnh từ BGR sang RGB để hiển thị
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)
    # Hiển thị hình ảnh trong giao diện
    panel.config(image=image_tk)
    panel.image = image_tk

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Chọn ảnh để nhận diện biển số")

# Tạo nút chọn file
btn_choose = tk.Button(root, text="Chọn ảnh", command=choose_file)
btn_choose.pack(pady=10)

# Tạo vùng hiển thị ảnh
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

# Chạy vòng lặp giao diện
root.mainloop()
