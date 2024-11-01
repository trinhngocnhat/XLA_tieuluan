import tkinter as tk

root = tk.Tk()
root.title("Nhận diện biển số xe ")

#Set window size
root.geometry("400x300")

label = tk.Label(root, text="Hãy chọn chức năng bạn muốn ")
label.pack()

# Configure rows and columns to center all elements
root.grid_rowconfigure(0, weight=1)  # Top space
root.grid_rowconfigure(1, weight=1)  # Centered content
root.grid_rowconfigure(2, weight=1)  # Bottom space
root.grid_columnconfigure(0, weight=1)  # Left space
root.grid_columnconfigure(1, weight=1)  # Right space

# Use grid for label and buttons
label.grid(row=0, column=0, columnspan=5, pady=20)
tk.Button(root, text="livestream").grid(row=1, column=0, padx=10, pady=10)
tk.Button(root, text="chọn ảnh").grid(row=1, column=1, padx=10, pady=10)

root.mainloop()