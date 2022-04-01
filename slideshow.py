import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkvideo import tkvideo
from datetime import datetime
import glob
import cv2
import time

# adjust window
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{screen_width}x{screen_height}')

l = Label()
l.pack()

# set the image directory
folder_dir = "C:/Users/hanna/PycharmProjects/pythonProject/Images/"
images = []

# loop through all the images in the file and save them to a list
for image in glob.glob('C:/Users/hanna/PycharmProjects/pythonProject/Images/*.jpg'):
    current_image = Image.open(image)
    images.append(current_image)


# function that resizes all the images to fit the screen while still maintaining their aspect ratio
def resize_image(image):
    aspect_ratio = image.width/image.height
    desired_image_height = screen_height
    desired_image_width = int(screen_height * aspect_ratio)
    if desired_image_width > screen_width:
        desired_image_width = screen_width
        desired_image_height = int(screen_width / aspect_ratio)
    img_resized = image.resize((desired_image_width, desired_image_height), Image.ANTIALIAS)
    return img_resized, desired_image_height, desired_image_width


x = 1

while x == 1:
    # apply the resize function to all the images
    resized_images = []
    for image in images:
        resized_image = ImageTk.PhotoImage(resize_image(image)[0])
        resized_images.append(resized_image)
    x = 2

video = tkvideo("video.mp4", label=l)


def resize_video():
    vid = cv2.VideoCapture("C:/Users/hanna/PycharmProjects/pythonProject/video.mp4")
    vid_height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    vid_width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    aspect_ratio = vid_width/vid_height
    desired_video_height = screen_height
    desired_video_width = int(screen_height * aspect_ratio)
    if desired_video_width > screen_width:
        desired_video_width = screen_width
        desired_video_height = int(screen_width / aspect_ratio)
    return desired_video_height, desired_video_width


x = 0
y = len(images)


# function to change to next image
def change_images():
    current_time = datetime.now()
    # currently set up to play video every minute, change to every hour when done testing.
    print(current_time.second)
    if current_time.second < 3 or current_time.second > 57:
        # play video
        l.config(image=video.play())
        # l.config(image=video.play(), width=resize_video()[1], height=resize_video()[0])
        root.after(15000, change_images)
        return None
    global x
    if x == y:
        x = 0
    if x != y:
        l.config(image=resized_images[x])
    x = x + 1

    # change images specified milliseconds
    root.after(4000, change_images)


# calling the function
change_images()

root.mainloop()
