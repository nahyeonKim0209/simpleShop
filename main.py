import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox

from PIL import Image
from PIL import ImageTk

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

def uploadFile() :
    fpath = fd.askopenfilename()
    if fpath :
        uploadPhoto(fpath)

def uploadPhoto(fpath) :

    global image, imageLabel, imageCV

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

        imageData = ImageTk.PhotoImage(image)
        imageLabel.configure(image = imageData)
        imageLabel.image = imageData

    else:
        messagebox.showerror("Error", "Failed to load image. Please try a different file.")

def downloadFile() :
    if image:
        file_path = fd.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            gray_image.save(file_path)

def convert_to_grayscale():
    global image, img_display, imageCV, gray_image
    if imageCV is not None:
        gray_cv = cv2.cvtColor(imageCV, cv2.COLOR_BGR2GRAY)
        gray_image = Image.fromarray(gray_cv)
        img_display = ImageTk.PhotoImage(gray_image)
        imageLabel.config(image=img_display)
        imageLabel.image = img_display


uploadPhoto_btn = tk.Button(window, text="파일 불러오기", command = uploadFile)
downloadPhoto_btn = tk.Button(window, text="파일 다운하기", command = downloadFile)

grayscale_btn = tk.Button(window, text="흑백 전환", command = convert_to_grayscale)

imageLabel = tk.Label()
uploadPhoto_btn.pack()
downloadPhoto_btn.pack()

grayscale_btn.pack(side="right")

imageLabel.pack()

tk.mainloop()