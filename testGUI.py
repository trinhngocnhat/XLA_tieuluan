import cv2
from tkinter import Tk, Button, Label, Frame, messagebox
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

class SimpleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Image and Camera App")
        self.master.geometry("600x600")

        # Frame for displaying image
        self.image_frame = Frame(master, width=400, height=400, bg="white", bd=2, relief="groove")
        self.image_frame.pack(pady=20)

        self.image_label = Label(self.image_frame)
        self.image_label.pack()

        # Control buttons
        self.button_select_file = Button(master, text="Chọn file", command=self.select_file, bg="#3498DB", fg="white")
        self.button_select_file.pack(pady=10)

        self.button_open_camera = Button(master, text="Mở Camera", command=self.open_camera, bg="#2ECC71", fg="white")
        self.button_open_camera.pack(pady=10)

        # Image and camera variables
        self.image = None
        self.video_source = None
        self.is_camera_open = False

    def display_image(self):
        if self.image is not None:
            img = cv2.resize(self.image, (400, 400))  # Resize image
            img = Image.fromarray(img)  # Convert to PIL Image
            img = ImageTk.PhotoImage(img)  # Convert to Tkinter format

            self.image_label.config(image=img)
            self.image_label.image = img
        else:
            messagebox.showwarning("Cảnh báo", "Không có ảnh để hiển thị.")

    def select_file(self):
        file_path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            self.display_image()

    def open_camera(self):
        self.is_camera_open = True
        self.video_source = cv2.VideoCapture(0)

        if not self.video_source.isOpened():
            messagebox.showerror("Lỗi", "Không thể mở camera.")
            self.is_camera_open = False
            return

        self.update_frame()

    def update_frame(self):
        if self.is_camera_open:
            ret, frame = self.video_source.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.image = frame_rgb
                self.display_image()
                self.master.after(10, self.update_frame)
            else:
                messagebox.showerror("Lỗi", "Không thể chụp ảnh từ camera.")
                self.close_camera()

    def close_camera(self):
        if self.video_source:
            self.video_source.release()
            self.is_camera_open = False
            cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    app = SimpleApp(root)
    root.mainloop()
