import tkinter as tk
from chuc_nang.chuc_nang_chinh.chon_hinh_anh import chon_hinh_anh
from chuc_nang.chuc_nang_chinh.open_camera import livestream

root = tk.Tk()
root.title("Nhận diện biển số xe")
root.geometry("1024x632")

root.grid_rowconfigure([0, 1, 2], weight=1)
root.grid_columnconfigure([0, 1], weight=1)

tk.Label(root, text="Hãy chọn chức năng bạn muốn").grid(row=0, column=0, columnspan=5, pady=20)
tk.Button(root, text="livestream", command=livestream).grid(row=1, column=0, padx=10, pady=10)
tk.Button(root, text="chọn ảnh", command=chon_hinh_anh).grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
