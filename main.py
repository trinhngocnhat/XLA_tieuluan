import cv2
import numpy as np
from tkinter import Tk, Button, Label, Frame, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO
from chuc_nang.chuc_nang_chinh.open_camera import livestream
from chuc_nang.chuc_nang_chinh.chon_hinh_anh import chon_hinh_anh


class ImageProcessor:
    def __init__(self, master):
        self.master = master
        self.master.iconbitmap('icon.ico')
        self.master.title("Nhóm 9 - Camera và Chọn Hình Ảnh")
        self.master.geometry("1000x1000")
        self.master.configure(bg="#D6EAF8")

        # Load YOLO model
        self.model = YOLO(r"C:\Users\ASUS\Documents\GitHub\XLA_tieuluan\yolov8n.pt")

        # Main frame
        self.main_frame = Frame(master, bg="#D6EAF8")
        self.main_frame.pack(fill="both", expand=True)

        # Frame for original image
        self.original_frame = Frame(self.main_frame, bg="#D6EAF8")
        self.original_frame.pack(pady=20)

        self.original_label = Label(self.original_frame, text="Ảnh gốc", font=("Arial", 16), bg="#D6EAF8")
        self.original_label.pack()

        self.image_frame = Frame(self.original_frame, width=400, height=400, bg="white", bd=2, relief="groove")
        self.image_frame.pack(pady=10)

        self.image_label = Label(self.image_frame)
        self.image_label.pack()

        # Control frame
        self.control_frame = Frame(self.main_frame, bg="#D6EAF8")
        self.control_frame.pack(pady=20)

        # Load Image Button
        self.button_load_file = Button(self.control_frame, text="Chọn Ảnh", command=self.open_file, bg="#3498DB",
                                       fg="white", font=("Arial", 14))
        self.button_load_file.pack(side="left", padx=10)

        # Open Camera Button
        self.button_open_camera = Button(self.control_frame, text="Mở Camera", command=self.open_camera,
                                         bg="#2ECC71", fg="white", font=("Arial", 14))
        self.button_open_camera.pack(side="left", padx=10)

        # Cancel Button
        self.button_cancel = Button(self.control_frame, text="Hủy", command=self.cancel_operation,
                                    bg="#E74C3C", fg="white", font=("Arial", 14))
        self.button_cancel.pack(side="left", padx=10)

        # Placeholder for image data
        self.image = None
        self.video_source = None  # Variable for the camera feed
        self.is_camera_open = False  # Flag to check if camera is open

        # Footer for displaying information
        self.footer_frame = Frame(master, bg="#D6EAF8")
        self.footer_frame.pack(side="bottom", fill="x", pady=10)

        self.footer_label = Label(self.footer_frame,
                                  text="Biển số xe: XX-12345    Nơi cấp: Hà Nội    Loại biển số: Xe con",
                                  font=("Arial", 12), bg="#D6EAF8", anchor="w")
        self.footer_label.pack(padx=20)

    def display_image(self, image):
        """ Displays the processed image in the GUI """
        if image is not None:
            # Resize and convert to Tkinter-compatible image
            img = cv2.resize(image, (400, 400))  # Resize the image to fit the label
            img = Image.fromarray(img)  # Convert NumPy array to PIL Image
            img = ImageTk.PhotoImage(img)  # Convert PIL Image to Tkinter-compatible format

            # Display the image in the label
            self.image_label.config(image=img)
            self.image_label.image = img
        else:
            messagebox.showwarning("Cảnh báo", "Không có ảnh để hiển thị.")

    def process_image_with_yolo(self, image):
        """ Runs YOLO detection on the given image """
        results = self.model(image)
        annotated_frame = results[0].plot()  # Plot detections on the image
        return annotated_frame

    def open_file(self):
        """ Load image from a file and run YOLO detection """
        image = chon_hinh_anh()
        if image is not None:
            self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
            processed_image = self.process_image_with_yolo(self.image)
            self.display_image(processed_image)

    def open_camera(self):
        """ Open camera and run YOLO detection on live feed """
        self.is_camera_open = True
        self.video_source = cv2.VideoCapture(0)

        if not self.video_source.isOpened():
            messagebox.showerror("Lỗi", "Không thể mở camera.")
            self.is_camera_open = False
            return

        # Start the camera feed
        self.update_frame()

    def update_frame(self):
        """ Reads the next frame and updates the GUI with YOLO detection """
        if self.is_camera_open:
            ret, frame = self.video_source.read()

            if ret:
                # Convert the frame to RGB format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Run YOLO detection on the frame
                processed_frame = self.process_image_with_yolo(frame_rgb)

                # Display the processed frame
                self.display_image(processed_frame)

                # Call this function every 10ms to update the frame
                self.master.after(10, self.update_frame)
            else:
                messagebox.showerror("Lỗi", "Không thể chụp ảnh từ camera.")
                self.close_camera()

    def close_camera(self):
        """ Releases the camera and closes any open windows """
        if self.video_source:
            self.video_source.release()
            self.is_camera_open = False
            cv2.destroyAllWindows()

    def cancel_operation(self):
        """ Cancels the current operation (camera or image load) """
        if self.is_camera_open:
            self.close_camera()
            messagebox.showinfo("Thông báo", "Đã hủy việc mở camera.")
        else:
            self.image = None
            self.image_label.config(image="")
            self.image_label.image = None
            messagebox.showinfo("Thông báo", "Đã hủy việc chọn ảnh.")


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()
