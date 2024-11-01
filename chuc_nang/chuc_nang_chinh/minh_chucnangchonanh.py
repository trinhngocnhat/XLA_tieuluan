import tkinter as tk
from tkinter import filedialog
from PIL import Image


def open_image():
  """
  Mở hộp thoại cho phép người dùng chọn file ảnh và hiển thị ảnh.
  """
  root = tk.Tk()
  root.withdraw()  # Ẩn cửa sổ tkinter chính

  file_path = filedialog.askopenfilename(
      initialdir="/",
      title="Chọn file ảnh",
      filetypes=(
          ("Tất cả các file", "*.*"),
          ("File ảnh", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"),
      ),
  )

  if file_path:
    try:
      img = Image.open(file_path)
      img.show()  # Hiển thị ảnh bằng ứng dụng xem ảnh mặc định
    except Exception as e:
      print(f"Lỗi khi mở ảnh: {e}")
  else:
    print("Không có file nào được chọn.")

# Gọi hàm để mở hộp thoại chọn file
open_image()
