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
processed_image = None
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

        display_size = image.size

        image = resize_image(image, 800, 450)

        img_display = ImageTk.PhotoImage(image)
        imageLabel.configure(image=img_display)
        imageLabel.image = img_display

    else:
        messagebox.showerror("Error", "Failed to load image. Please try a different file.")

def downloadFile():
    global processed_image, imageCV
    if processed_image:
        file_path = fd.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            original_height, original_width, _ = imageCV.shape
            processed_image_resized = processed_image.resize((original_width, original_height))
            processed_image_resized.save(file_path)

def resize_image(image, target_width, target_height):
    width, height = image.size
    if height > target_height:
        width_ = int(width * (target_height / height))
        if width_ > target_width:
            height_ = int(target_height * (target_width / width_))
        else:
            height_ = target_height
        image = image.resize((width_, height_))
    if width_ > target_width:
        height_ = int(height * (target_width / width))
        if height_ > target_height:
            width_ = int(target_width * (target_height / height_))
        else:
            width_ = target_width
        image = image.resize((width_, height_))
    return image

#가우시안 노이즈 함수
def add_gaussian_noise(image, std):
    h, w, c = image.shape
    noise = np.random.normal(0, std, (h, w, c))
    noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return noisy_image

def apply_noise(image, noise_level):
    std = noise_level * 2.55 
    noisy_image = add_gaussian_noise(image, std)
    return noisy_image

#노출 조정 함수
def adjust_exposure(image, exposure_value):
    if exposure_value >= 0:
        exposure_value = exposure_value / 100.0
        exposure_image = image.point(lambda p: p * (1 + exposure_value))
    else:
        exposure_value = abs(exposure_value) / 100.0
        exposure_image = image.point(lambda p: p / (1 + exposure_value))
    return exposure_image

def apply_effects(gray_value, mosaic_value, noise_value, exposure_value):
    global image, img_display, imageCV, processed_image, display_size
    if imageCV is not None:
        # 그레이스케일
        alpha = float(gray_value) / 100.0
        gray_cv = cv2.cvtColor(imageCV, cv2.COLOR_BGR2GRAY)
        gray_cv_rgb = cv2.cvtColor(gray_cv, cv2.COLOR_GRAY2RGB)
        blended = cv2.addWeighted(imageCV, 1 - alpha, gray_cv_rgb, alpha, 0)

        # 모자이크
        scale = max(1, int(mosaic_value)) 
        height, width, _ = blended.shape
        small_img = cv2.resize(blended, (width // scale, height // scale), interpolation=cv2.INTER_LINEAR)
        mosaic_cv = cv2.resize(small_img, (width, height), interpolation=cv2.INTER_NEAREST)

        # 노이즈
        noisy_image = apply_noise(mosaic_cv, noise_value)
        noisy_image = cv2.cvtColor(noisy_image, cv2.COLOR_BGR2RGB)
        noisy_image = Image.fromarray(noisy_image)

        # 노출
        exposure_image = adjust_exposure(noisy_image, exposure_value)

        processed_image = resize_image(exposure_image, 800, 450)

        img_display = ImageTk.PhotoImage(processed_image)
        imageLabel.config(image=img_display)
        imageLabel.image = img_display


def on_slider_change(value):
    gray_value = gray_slider.get()
    mosaic_value = mosaic_slider.get()
    noise_value = noise_slider.get()
    exposure_value = exposure_slider.get()
    
    apply_effects(gray_value, mosaic_value, noise_value, exposure_value)

uploadPhoto_btn = tk.Button(window, text="파일 불러오기", command=uploadFile)
downloadPhoto_btn = tk.Button(window, text="파일 다운하기", command=downloadFile)

gray_slider = tk.Scale(window, from_=0, to=100, orient="horizontal", label="Grayscale Level", command=on_slider_change)
mosaic_slider = tk.Scale(window, from_=1, to=30, orient="horizontal", label="Mosaic Level", command=on_slider_change)
noise_slider = tk.Scale(window, from_=0, to=100, orient="horizontal", label="Noise Level", command=on_slider_change)
exposure_slider = tk.Scale(window, from_=-100, to=100, orient="horizontal", label="Exposure Level", command=on_slider_change)

imageLabel = tk.Label(window)
uploadPhoto_btn.pack()
downloadPhoto_btn.pack()
gray_slider.pack()
mosaic_slider.pack()
noise_slider.pack()
exposure_slider.pack()
imageLabel.pack()

tk.mainloop()
