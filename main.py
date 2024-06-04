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

def uploadFile() :
    fpath = fd.askopenfilename()
    if fpath :
        uploadPhoto(fpath)

def uploadPhoto(fpath) :

    global image, imageLabel, imageCV, img_display

    imageCV = cv2.imread(fpath)

    if imageCV is not None:

        image = cv2.cvtColor(imageCV, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        width, height = image.size
        width_, height_ = 10, 10
        if height > 450 :
            width_ = int(width * (450/height))
            if width_ > 800 :
                height_ = int(450 * (800/width_))
            else : height_ = 450
            image = image.resize((width_, height_))
        if width_ > 800 :
            height_ = int(height * (800/width))
            if height_ > 450 :
                width_ = int(800 * (450/height_))
            else : width_ = 800
            image = image.resize((width_, height_))

        img_display = ImageTk.PhotoImage(image)
        imageLabel.configure(image = img_display)
        imageLabel.image = img_display

    else:
        messagebox.showerror("Error", "Failed to load image. Please try a different file.")

def downloadFile() :
    if gray_image:
        file_path = fd.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            gray_image.save(file_path)

def update_grayscale(value):
    global image, img_display, imageCV, gray_image
    if imageCV is not None:
        alpha = float(value) / 100.0
        gray_cv = cv2.cvtColor(imageCV, cv2.COLOR_BGR2GRAY)
        gray_cv_rgb = cv2.cvtColor(gray_cv, cv2.COLOR_GRAY2RGB)
        blended = cv2.addWeighted(imageCV, 1 - alpha, gray_cv_rgb, alpha, 0)
        gray_image = Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
        gray_image = gray_image.resize(image.size)

        img_display = ImageTk.PhotoImage(gray_image)
        imageLabel.config(image=img_display)
        imageLabel.image = img_display

def apply_mosaic(value):
    global image, img_display, imageCV, mosaic_image
    if imageCV is not None:
        scale = max(1, int(value))
        height, width, _=imageCV.shape

        small_img = cv2.resize(imageCV, (width // scale, height // scale))

uploadPhoto_btn = tk.Button(window, text="파일 불러오기", command = uploadFile)
downloadPhoto_btn = tk.Button(window, text="파일 다운하기", command = downloadFile)

gray_slider = tk.Scale(window, from_=0, to=100, orient="horizontal", label="Grayscale Level", command=update_grayscale)

imageLabel = tk.Label()
uploadPhoto_btn.pack()
downloadPhoto_btn.pack()
gray_slider.pack()
imageLabel.pack()

tk.mainloop()
