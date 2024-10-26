import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import pytesseract

# Configure tesseract path (if necessary)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Tkinter window
window = tk.Tk()
window.title("License Plate Recognition")
window.geometry("800x600")

# Global variables
selected_image = None


def open_image():
    global selected_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    # Read and display the image
    selected_image = cv2.imread(file_path)
    image_rgb = cv2.cvtColor(selected_image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_tk = ImageTk.PhotoImage(image_pil)

    # Display the image in Tkinter
    image_label.config(image=image_tk)
    image_label.image = image_tk


def recognize_plate():
    if selected_image is None:
        messagebox.showwarning("Warning", "Please select an image first.")
        return

    # Convert to grayscale and apply some preprocessing
    gray = cv2.cvtColor(selected_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blurred, 30, 200)

    # Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    license_plate_text = ""

    for contour in contours:
        # Approximate contour
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * perimeter, True)

        if len(approx) == 4:  # Assuming license plate has 4 edges
            x, y, w, h = cv2.boundingRect(contour)
            license_plate = selected_image[y:y + h, x:x + w]
            license_plate_gray = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)

            # Use Tesseract to recognize text
            license_plate_text = pytesseract.image_to_string(license_plate_gray, config='--psm 8')
            break

    if license_plate_text:
        result_label.config(text=f"License Plate: {license_plate_text.strip()}")
    else:
        result_label.config(text="License Plate: Not found")


# Tkinter UI components
open_button = tk.Button(window, text="Open Image", command=open_image)
open_button.pack()

recognize_button = tk.Button(window, text="Recognize License Plate", command=recognize_plate)
recognize_button.pack()

image_label = tk.Label(window)
image_label.pack()

result_label = tk.Label(window, text="License Plate: ", font=("Helvetica", 16))
result_label.pack()

window.mainloop()
