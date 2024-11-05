import tkinter as tk
from chuc_nang.chuc_nang_chinh.chon_hinh_anh import chon_hinh_anh
from chuc_nang.chuc_nang_chinh.open_camera import livestream

def display_prediction(prediction_text):
    prediction_display.config(text=prediction_text)

def livestream_with_prediction():
    display_prediction(livestream())

def chon_hinh_anh_with_prediction():
    display_prediction(chon_hinh_anh())

# Initialize the root window
root = tk.Tk()
root.title("Nhận diện biển số xe")
root.geometry("1024x632")
root.configure(bg="black")

# Create frames
tk.Frame(root, bg="yellow", height=150).pack(fill=tk.BOTH, expand=True)
prediction_display = tk.Label(root, text="Kết quả sẽ hiển thị ở đây", bg="light blue", font=("Helvetica", 10))
prediction_display.pack(fill=tk.BOTH, expand=True)
bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(fill=tk.BOTH, expand=True)

# Add buttons
tk.Button(bottom_frame, text="livestream", command=livestream_with_prediction, bg="yellow", font=("Helvetica", 10)).pack(side=tk.LEFT, padx=20, pady=20, ipadx=10, ipady=5)
tk.Button(bottom_frame, text="chọn hình ảnh", command=chon_hinh_anh_with_prediction, bg="yellow", font=("Helvetica", 10)).pack(side=tk.RIGHT, padx=20, pady=20, ipadx=10, ipady=5)

# Run the GUI main loop
root.mainloop()
