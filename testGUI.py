import cv2
import numpy as np
from tkinter import Tk, Button, filedialog, Label, Frame, messagebox, Toplevel
from PIL import Image, ImageTk


class ImageProcessor:
    def __init__(self, master):
        self.master = master
        self.master.iconbitmap('icon.ico')
        self.master.title("Nhóm 9 - Gradient và Laplacian ")
        self.master.geometry("1000x1000")
        self.master.configure(bg="#D6EAF8")

        # Khung chính
        self.main_frame = Frame(master, bg="#D6EAF8")
        self.main_frame.pack(fill="both", expand=True)

        # Khung cho ảnh gốc
        self.original_frame = Frame(self.main_frame, bg="#D6EAF8")
        self.original_frame.pack(pady=20)

        self.original_label = Label(self.original_frame, text="Ảnh gốc", font=("Arial", 16), bg="#D6EAF8")
        self.original_label.pack()

        self.image_frame = Frame(self.original_frame, width=400, height=400, bg="white", bd=2, relief="groove")
        self.image_frame.pack(pady=10)

        self.image_label = Label(self.image_frame)
        self.image_label.pack()

        # Khung điều khiển
        self.control_frame = Frame(self.main_frame, bg="#D6EAF8")
        self.control_frame.pack(pady=20)

        self.title_label = Label(self.control_frame, text="Gradient và Laplacian", font=("Arial", 24), bg="#D6EAF8")
        self.title_label.pack(pady=10)

        self.button_load = Button(self.control_frame, text="Tải ảnh lên", command=self.load_image, bg="#3498DB",
                                  fg="white", font=("Arial", 14))
        self.button_load.pack(side="left", padx=10)

        self.button_process = Button(self.control_frame, text="Xử lý ảnh", command=self.process_image,
                                     font=("Arial", 14), state='disabled')
        self.button_process.pack(side="left", padx=10)

        self.button_clear = Button(self.control_frame, text="Xóa", command=self.clear_image, bg="#E74C3C", fg="white",
                                   font=("Arial", 14))
        self.button_clear.pack(side="left", padx=10)

        self.button_save = Button(self.control_frame, text="Lưu ảnh", command=self.save_image, font=("Arial", 14),
                                  state='disabled')
        self.button_save.pack(side="left", padx=10)

        # Khung kết quả
        self.bottom_frame = Frame(self.main_frame, bg="#D6EAF8")
        self.bottom_frame.pack(pady=20, fill="both", expand=True)

        # Khung kết quả
        self.results_frame = Frame(self.bottom_frame, bg="#D6EAF8")
        self.results_frame.pack(pady=10)

        self.gradient_label = Label(self.results_frame, text="Gradient")
        self.gradient_label.grid(row=0, column=0, padx=10, pady=5)
        self.gradient_image = Label(self.results_frame)
        self.gradient_image.grid(row=1, column=0, padx=10, pady=5)

        self.laplacian_label = Label(self.results_frame, text="Laplacian")
        self.laplacian_label.grid(row=0, column=1, padx=10, pady=5)
        self.laplacian_image = Label(self.results_frame)
        self.laplacian_image.grid(row=1, column=1, padx=10, pady=5)

        self.combined_label = Label(self.results_frame, text="Kết hợp Gradient và Laplacian")
        self.combined_label.grid(row=0, column=2, padx=10, pady=5)
        self.combined_image = Label(self.results_frame)
        self.combined_image.grid(row=1, column=2, padx=10, pady=5)

        self.button_gradient_info = Button(self.control_frame, text="Thông tin Gradient",
                                           command=self.show_gradient_info, font=("Arial", 14))
        self.button_gradient_info.pack(side="left", padx=20)

        self.button_laplacian_info = Button(self.control_frame, text="Thông tin Laplacian",
                                            command=self.show_laplacian_info, font=("Arial", 14))
        self.button_laplacian_info.pack(side="left", padx=20)

        self.image_path = None
        self.image = None
        self.gradient_magnitude = None
        self.laplacian = None
        self.combined = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if self.image_path:
            self.display_image()
        else:
            messagebox.showwarning("Cảnh báo", "Bạn chưa chọn ảnh nào.")
            return

    def display_image(self):
        self.image = Image.open(self.image_path)
        self.image.thumbnail((400, 400))
        self.image = ImageTk.PhotoImage(self.image)

        self.image_label.config(image=self.image)
        self.image_label.image = self.image

        self.button_process.config(state='normal')

    def clear_image(self):
        self.image_label.config(image='')
        self.image_label.image = None
        self.button_process.config(state='disabled')

        self.gradient_image.config(image='')
        self.laplacian_image.config(image='')
        self.combined_image.config(image='')

    def process_image(self):
        original_image = cv2.imread(self.image_path)

        if original_image is None:
            messagebox.showerror("Lỗi", "Không thể mở hoặc đọc tệp ảnh.")
            return

        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        # Gradient
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        self.gradient_magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)
        self.gradient_magnitude = np.uint8(self.gradient_magnitude)

        # Laplacian
        self.laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        self.laplacian = np.uint8(np.abs(self.laplacian))

        # Gradient và Laplacian
        self.combined = cv2.addWeighted(self.gradient_magnitude, 0.5, self.laplacian, 0.5, 0)

        self.display_result(self.gradient_magnitude, self.gradient_image)
        self.display_result(self.laplacian, self.laplacian_image)
        self.display_result(self.combined, self.combined_image)

        self.button_save.config(state='normal')

    def display_result(self, img, label):
        img = cv2.resize(img, (200, 200))
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img

    def save_image(self):
        if self.combined is None:
            messagebox.showwarning("Cảnh báo", "Bạn chưa xử lý ảnh nào để lưu.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if save_path:
            cv2.imwrite(save_path, self.combined)
            messagebox.showinfo("Thông báo", "Ảnh đã được lưu thành công.")

    def show_gradient_info(self):
        info_window = Toplevel(self.master)
        info_window.title("Thông tin về Gradient")
        info_window.geometry("400x200")
        label = Label(info_window, text="Thuật toán Gradient:\n\n"
                                        "- Sử dụng Sobel để tính đạo hàm của ảnh.\n"
                                        "- Kết quả cho thấy sự thay đổi về cường độ.\n"
                                        "- Được sử dụng để phát hiện biên của ảnh.", justify="left")
        label.pack(pady=20)

    def show_laplacian_info(self):
        info_window = Toplevel(self.master)
        info_window.title("Thông tin về Laplacian")
        info_window.geometry("400x200")
        label = Label(info_window, text="Thuật toán Laplacian:\n\n"
                                        "- Tính toán đạo hàm bậc hai của ảnh.\n"
                                        "- Nhấn mạnh các vùng chuyển tiếp và biên trong ảnh.\n"
                                        "- Thường được sử dụng trong xử lý ảnh để phát hiện biên.", justify="left")
        label.pack(pady=20)


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()

# import tkinter as tk
# from chuc_nang.chuc_nang_chinh.chon_hinh_anh import chon_hinh_anh
# from chuc_nang.chuc_nang_chinh.open_camera import livestream
#
# root = tk.Tk()
# root.title("Nhận diện biển số xe")
# root.geometry("1024x632")
#
# root.grid_rowconfigure([0, 1, 2], weight=1)
# root.grid_columnconfigure([0, 1], weight=1)
#
# tk.Label(root, text="Hãy chọn chức năng bạn muốn").grid(row=0, column=0, columnspan=5, pady=20)
# tk.Button(root, text="livestream", command=livestream).grid(row=1, column=0, padx=10, pady=10)
# tk.Button(root, text="chọn ảnh", command=chon_hinh_anh).grid(row=1, column=1, padx=10, pady=10)
#
# root.mainloop()
