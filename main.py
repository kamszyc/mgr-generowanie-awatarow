from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import shutil
import avatar_generator

input_image_path = None
avatar_img = None

def load_image():
    global input_image_path, input_image_view, output_image_view, save_button, generation_method_box
    input_image_path = filedialog.askopenfilename(filetypes=[("Image files", ("*.png", "*.jpg"))])
    if input_image_path:
        output_image_view.configure(image="")
        output_image_view.image=""
        img = ImageTk.PhotoImage(file=input_image_path)
        input_image_view.configure(image=img)
        input_image_view.image=img
        generate_button["state"] = "normal"
        generation_method_box["state"] = "readonly"

def generate_image():
    global input_image_path, output_image_view, avatar_img, generation_method_box
    avatar_img = avatar_generator.generate_avatar(generation_method_box.get(), input_image_path)
    img = ImageTk.PhotoImage(image=avatar_img)
    output_image_view.configure(image=img)
    output_image_view.image=img
    save_button["state"] = "normal"

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
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(2, weight=2)
root.rowconfigure(2, weight=2)

pick_method = StringVar(value="Method:")
ttk.Label(mainframe, textvariable=pick_method).grid(column=1, row=1, sticky=W)

generation_method = StringVar()
generation_method_box = ttk.Combobox(mainframe, state="readonly", textvariable = generation_method)
generation_method_box["values"] = ( "CycleGAN", "AttentionGAN", "CUT (light skin, brown hair)", "CUT (light skin, black hair)", "CUT (light skin, blond hair)", "CUT (dark skin, black hair)" )
generation_method_box.grid(column=2, columnspan=2, row=1, sticky=NSEW)
generation_method_box.current(newindex=0)
generation_method_box["state"] = "disabled"

input_image_name = StringVar(value="Input image")
ttk.Label(mainframe, textvariable=input_image_name).grid(column=1, columnspan=2, row=2, sticky=W)

input_image_view = ttk.Label(mainframe)
input_image_view.grid(column=1, columnspan=2, row=3, sticky=W)

output_image_name = StringVar(value="Output image")
ttk.Label(mainframe, textvariable=output_image_name).grid(column=3, columnspan=2, row=2, sticky=W)

output_image_view = ttk.Label(mainframe)
output_image_view.grid(column=3, columnspan=2, row=3, sticky=W)

ttk.Button(mainframe, text="Load", command=load_image).grid(column=1, row=4, sticky=W)

generate_button = ttk.Button(mainframe, text="Generate", command=generate_image)
generate_button.grid(column=2, row=4, sticky=W)
generate_button["state"] = "disabled"

save_button = ttk.Button(mainframe, text="Save", command=save_image)
save_button.grid(column=3, row=4, sticky=W)
save_button["state"] = "disabled"

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()