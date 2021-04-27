from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import shutil
import avatar_generator
import threading

methods = ["CycleGAN", "CycleGAN + pix2pix", "AttentionGAN", "AttentionGAN + pix2pix",
    "CUT (light skin, brown hair)", "CUT (light skin, black hair)", "CUT (light skin, blond hair)", "CUT (dark skin, black hair)",
    "Neural style transfer (CycleGAN output as style)"]

input_image_path = None

method_to_avatar_imgs = {}
method_to_output_image_view = {}
method_to_save_button = {}

image_size = 256

def create_output_image_grid_cell(i, j):
    method = methods[i*3+j]
    ttk.Label(mainframe, text=method + " output").grid(column=2*j+2, row=2*i, sticky=NSEW)

    save_button = ttk.Button(mainframe, text="Save", command=lambda method = method:save_image(method))
    save_button["state"] = "disabled"
    save_button.grid(column=2*j+3, row=2*i, sticky=NSEW)
    method_to_save_button[method] = save_button

    output_image_view = ttk.Label(mainframe)
    output_image_view.grid(column=2*j+2, columnspan=2, row=2*i+1, sticky=NSEW)

    method_to_output_image_view[method] = output_image_view

def load_image():
    global input_image_path, input_image_view
    input_image_path = filedialog.askopenfilename(filetypes=[("Image files", ("*.png", "*.jpg"))])
    if input_image_path:
        for method in methods:
            output_image_view = method_to_output_image_view[method]
            output_image_view.configure(image="")
            output_image_view.image=""
            save_button = method_to_save_button[method]
            save_button["state"] = "disabled"
        image = Image.open(input_image_path)
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        photoimage = ImageTk.PhotoImage(image)
        input_image_view.configure(image=photoimage)
        input_image_view.image=photoimage
        generate_button["state"] = "normal"

def run_generate_images():
    global load_button, generate_button
    load_button["state"] = "disabled"
    generate_button["state"] = "disabled"
    for method in methods:
        output_image_view = method_to_output_image_view[method]
        output_image_view.configure(image="")
        output_image_view.image=""
        save_button = method_to_save_button[method]
        save_button["state"] = "disabled"
    progress_bar.start(5)
    t = threading.Thread(target=generate_images)
    t.start()

def generate_images():
    global method_to_avatar_imgs, root
    for method in methods:
        method_to_avatar_imgs[method] = avatar_generator.generate_avatar(method, input_image_path)
        root.after(0, lambda method = method:after_generate_one_image(method))
    root.after(0, after_generate_all_images)
    

def after_generate_one_image(method):
    global load_button, generate_button, method_to_output_image_view, method_to_avatar_imgs
    avatar_img = method_to_avatar_imgs[method]
    output_image_view = method_to_output_image_view[method]
    img = ImageTk.PhotoImage(image=avatar_img)
    output_image_view.configure(image=img)
    output_image_view.image=img
    method_to_save_button[method]["state"] = "normal"

def after_generate_all_images():
    load_button["state"] = "normal"
    generate_button["state"] = "normal"
    progress_bar.stop()


def save_image(method):
    global method_to_avatar_imgs
    if method not in method_to_avatar_imgs:
        return
    avatar_img = method_to_avatar_imgs[method]
    output_image_path = filedialog.asksaveasfilename(defaultextension="*.*", filetypes=[("PNG file", "*.png"), ("JPG file", "*.jpg")])
    if output_image_path:
        avatar_img.save(output_image_path)

root = Tk()
root.title("Avatar generator")
#root.resizable(False, False)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=NSEW)
for i in range(0, 8):
    mainframe.columnconfigure(i, minsize=image_size / 2)
mainframe.rowconfigure(1, minsize=image_size)
mainframe.rowconfigure(3, minsize=image_size)
mainframe.rowconfigure(5, minsize=image_size)

ttk.Label(mainframe, text="Input image").grid(column=0, columnspan=2, row=2, sticky=NSEW)

input_image_view = ttk.Label(mainframe)
input_image_view.grid(column=0, columnspan=2, row=3, sticky=NSEW)

load_button = ttk.Button(mainframe, text="Load", command=load_image)
load_button.grid(column=0, row=4, sticky=NSEW)

generate_button = ttk.Button(mainframe, text="Generate", command=run_generate_images)
generate_button.grid(column=1, row=4, sticky=NSEW)
generate_button["state"] = "disabled"

for i in range(3):
    for j in range(3):
        create_output_image_grid_cell(i,j)

progress_bar = ttk.Progressbar(mainframe, orient = HORIZONTAL, mode = 'indeterminate')
progress_bar.grid(column=0, columnspan=8, row=6, sticky=NSEW)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()