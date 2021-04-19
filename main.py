from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import shutil
import avatar_generator
import threading

input_image_path = None
avatar_img = None

def load_image():
    global input_image_path, input_image_view, output_image_view, generation_method_box
    input_image_path = filedialog.askopenfilename(filetypes=[("Image files", ("*.png", "*.jpg"))])
    if input_image_path:
        output_image_view.configure(image="")
        output_image_view.image=""
        img = ImageTk.PhotoImage(file=input_image_path)
        input_image_view.configure(image=img)
        input_image_view.image=img
        generate_button["state"] = "normal"
        generation_method_box["state"] = "readonly"

def run_generate_image():
    global load_button, generate_button, save_button, generation_method_box
    load_button["state"] = "disabled"
    generate_button["state"] = "disabled"
    save_button["state"] = "disabled"
    generation_method_box["state"] = "disabled"
    progress_bar.start(5)
    t = threading.Thread(target=generate_image)
    t.start()

def generate_image():
    global avatar_img, root
    avatar_img = avatar_generator.generate_avatar(generation_method_box.get(), input_image_path)
    root.after(0, after_generate_image)

def after_generate_image():
    global load_button, generate_button, save_button, generation_method_box, output_image_view
    img = ImageTk.PhotoImage(image=avatar_img)
    output_image_view.configure(image=img)
    output_image_view.image=img
    load_button["state"] = "normal"
    generate_button["state"] = "normal"
    save_button["state"] = "normal"
    generation_method_box["state"] = "readonly"
    progress_bar.stop()

def save_image():
    if not avatar_img:
        return
    output_image_path = filedialog.asksaveasfilename(defaultextension="*.*", filetypes=[("PNG file", "*.png"), ("JPG file", "*.jpg")])
    if output_image_path:
        avatar_img.save(output_image_path)

root = Tk()
root.title("Avatar generator")
root.resizable(False, False)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=NSEW)

mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=2)

pick_method = StringVar(value="Method:")
ttk.Label(mainframe, textvariable=pick_method).grid(column=0, row=0, sticky=NSEW)

generation_method = StringVar()
generation_method_box = ttk.Combobox(mainframe, state="readonly", textvariable = generation_method)
generation_method_box["values"] = ( "CycleGAN", "CycleGAN + pix2pix", "AttentionGAN", "AttentionGAN + pix2pix",
    "CUT (light skin, brown hair)", "CUT (light skin, black hair)", "CUT (light skin, blond hair)", "CUT (dark skin, black hair)" )
generation_method_box.grid(column=1, columnspan=2, row=0, sticky=NSEW)
generation_method_box.current(newindex=0)
generation_method_box["state"] = "disabled"

input_image_name = StringVar(value="Input image")
ttk.Label(mainframe, textvariable=input_image_name).grid(column=0, columnspan=2, row=1, sticky=NSEW)

input_image_view = ttk.Label(mainframe)
input_image_view.grid(column=0, columnspan=2, row=2, sticky=NSEW)

output_image_name = StringVar(value="Output image")
ttk.Label(mainframe, textvariable=output_image_name).grid(column=2, columnspan=2, row=1, sticky=NSEW)

output_image_view = ttk.Label(mainframe)
output_image_view.grid(column=2, columnspan=2, row=2, sticky=NSEW)

load_button = ttk.Button(mainframe, text="Load", command=load_image)
load_button.grid(column=0, row=3, sticky=NSEW)

generate_button = ttk.Button(mainframe, text="Generate", command=run_generate_image)
generate_button.grid(column=1, row=3, sticky=NSEW)
generate_button["state"] = "disabled"

save_button = ttk.Button(mainframe, text="Save", command=save_image)
save_button.grid(column=2, row=3, sticky=W)
save_button["state"] = "disabled"

progress_bar = ttk.Progressbar(mainframe, orient = HORIZONTAL, mode = 'indeterminate')
progress_bar.grid(column=0, columnspan=3, row=4, sticky=NSEW)

save_button.grid(column=2, row=3, sticky=NSEW)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()