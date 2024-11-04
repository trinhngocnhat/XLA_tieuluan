import tkinter as tk
from chuc_nang.chuc_nang_chinh.chon_hinh_anh import chon_hinh_anh
from chuc_nang.chuc_nang_chinh.open_camera import livestream

def display_prediction(prediction_text):
    """Display prediction text in the GUI."""
    prediction_display.config(state=tk.NORMAL)  # Enable editing to update text
    prediction_display.delete(1.0, tk.END)  # Clear previous content
    prediction_display.insert(tk.END, prediction_text)  # Insert new prediction
    prediction_display.config(state=tk.DISABLED)  # Disable editing for read-only display

def livestream_with_prediction():
    """Wrapper function for livestream to display predictions."""
    # Assuming livestream() function processes and returns predictions
    prediction = livestream()
    display_prediction(prediction)

def chon_hinh_anh_with_prediction():
    """Wrapper function for chon_hinh_anh to display predictions."""
    # Assuming chon_hinh_anh() function processes and returns predictions
    prediction = chon_hinh_anh()
    display_prediction(prediction)

# Initialize the root window
root = tk.Tk()
root.title("Nhận diện biển số xe")

# Set window size
root.geometry("600x400")

# Main instruction label
label = tk.Label(root, text="Hãy chọn chức năng bạn muốn", font=("Helvetica", 14))
label.grid(row=0, column=0, columnspan=2, pady=20)

# Buttons for functionalities
tk.Button(root, text="Livestream", command=livestream_with_prediction, width=15).grid(row=1, column=0, padx=10, pady=10)
tk.Button(root, text="Chọn ảnh", command=chon_hinh_anh_with_prediction, width=15).grid(row=1, column=1, padx=10, pady=10)

# Prediction display area
prediction_label = tk.Label(root, text="Kết quả nhận diện biển số:", font=("Helvetica", 12))
prediction_label.grid(row=2, column=0, columnspan=2, pady=10)

# Text widget to display prediction results
prediction_display = tk.Text(root, height=10, width=50, wrap=tk.WORD)
prediction_display.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
prediction_display.config(state=tk.DISABLED)  # Set to read-only initially

# Run the GUI main loop
root.mainloop()
