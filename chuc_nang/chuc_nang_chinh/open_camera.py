# chuc_nang_chinh/open_camera.py
import cv2
from tkinter import messagebox
from chuc_nang.chuc_nang_default.nhan_dien import recognize_license_plate


def livestream():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Lỗi", "Không thể mở camera.")
        return None

    # Set the frame rate to 30 FPS
    cap.set(cv2.CAP_PROP_FPS, 30)




    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Lỗi", "Không thể chụp ảnh từ camera.")
            cap.release()
            cv2.destroyAllWindows()
            return None

        frame = recognize_license_plate(frame)

        # Show the frame
        cv2.imshow('Livestream - Press Q to Quit', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the capture when done
    cap.release()
    cv2.destroyAllWindows()
