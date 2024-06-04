import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox

from PIL import Image
from PIL import ImageTk
import numpy as np

import cv2

window = tk.Tk()

windows_width = window.winfo_screenwidth()
windows_height = window.winfo_screenheight()

app_width = 1440
app_height = 810

center_width = (windows_width - app_width) // 2
center_height = (windows_height - app_height) // 2

window.title("simpleshop")
window.geometry(f"{app_width}x{app_height}+{center_width}+{center_height}")
window.resizable(False, False)

image = None
imageCV = None
gray_image = None
mosaic_image = None
display_size = None

def uploadFile():
    fpath = fd.askopenfilename()
    if fpath:
        uploadPhoto(fpath)

def uploadPhoto(fpath):
    global image, imageLabel, imageCV, img_display, display_size

    imageCV = cv2.imread(fpath)

    if imageCV is not None:
        image = cv2.cvtColor(imageCV, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        width, height = image.size
        width_, height_ = 10, 10
        if height > 450:
            width_ = int(width * (450 / height))
            if width_ > 800:
                height_ = int(450 * (800 / width_))
            else:
                height_ = 450
            image = image.resize((width_, height_))
        if width_ > 800:
            height_ = int(height * (800 / width))
            if height_ > 450:
                width_ = int(800 * (450 / height_))
            else:
                width_ = 800
            image = image.resize((width_, height_))

        display_size = image.size

        img_display = ImageTk.PhotoImage(image)
        imageLabel.configure(image=img_display)
        imageLabel.image = img_display

    else:
        messagebox.showerror("Error", "Failed to load image. Please try a different file.")

def downloadFile():
    if gray_image or mosaic_image:
        file_path = fd.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            if gray_image:
                gray_image.save(file_path)
            elif mosaic_image:
                mosaic_image.save(file_path)

def apply_effects(gray_value, mosaic_value):
    global image, img_display, imageCV, gray_image, mosaic_image, display_size
    if imageCV is not None:
        # 그레이스케일 효과 적용
        alpha = float(gray_value) / 100.0
        gray_cv = cv2.cvtColor(imageCV, cv2.COLOR_BGR2GRAY)
        gray_cv_rgb = cv2.cvtColor(gray_cv, cv2.COLOR_GRAY2RGB)
        blended = cv2.addWeighted(imageCV, 1 - alpha, gray_cv_rgb, alpha, 0)

        # 모자이크 효과 적용
        scale = max(1, int(mosaic_value)) 
        height, width, _ = blended.shape
        small_img = cv2.resize(blended, (width // scale, height // scale), interpolation=cv2.INTER_LINEAR)
        mosaic_cv = cv2.resize(small_img, (width, height), interpolation=cv2.INTER_NEAREST)
        combined_image = Image.fromarray(cv2.cvtColor(mosaic_cv, cv2.COLOR_BGR2RGB))
        combined_image = combined_image.resize(display_size)

        img_display = ImageTk.PhotoImage(combined_image)
        imageLabel.config(image=img_display)
        imageLabel.image = img_display

def on_slider_change(value):
    gray_value = gray_slider.get()
    mosaic_value = mosaic_slider.get()
    apply_effects(gray_value, mosaic_value)

uploadPhoto_btn = tk.Button(window, text="파일 불러오기", command=uploadFile)
downloadPhoto_btn = tk.Button(window, text="파일 다운하기", command=downloadFile)

gray_slider = tk.Scale(window, from_=0, to=100, orient="horizontal", label="Grayscale Level", command=on_slider_change)
mosaic_slider = tk.Scale(window, from_=1, to=30, orient="horizontal", label="Mosaic Level", command=on_slider_change)

imageLabel = tk.Label()
uploadPhoto_btn.pack()
downloadPhoto_btn.pack()
gray_slider.pack()
mosaic_slider.pack()
imageLabel.pack()

tk.mainloop()
