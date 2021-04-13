from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import shutil
import avatar_generator

input_image_path = None

def load_image():
    global input_image_path, input_image_label, output_image_label
    input_image_path = filedialog.askopenfilename()
    if input_image_path:
        output_image_label.configure(image="")
        output_image_label.image=""
        img = ImageTk.PhotoImage(file=input_image_path)
        input_image_label.configure(image=img)
        input_image_label.image=img

def generate_image():
    global input_image_path, output_image_label
    avatar_img = avatar_generator.get_cyclegan_output(input_image_path)
    img = ImageTk.PhotoImage(image=avatar_img)
    output_image_label.configure(image=img)
    output_image_label.image=img

root = Tk()
root.title("Avatar generator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

input_image_name = StringVar(value="Input image")
ttk.Label(mainframe, textvariable=input_image_name).grid(column=1, row=1, sticky=W)

input_image_label = ttk.Label(mainframe)
input_image_label.grid(column=1, row=2, sticky=W)

output_image_name = StringVar(value="Output image")
ttk.Label(mainframe, textvariable=output_image_name).grid(column=2, row=1, sticky=W)

output_image_label = ttk.Label(mainframe)
output_image_label.grid(column=2, row=2, sticky=W)

ttk.Button(mainframe, text="Load", command=load_image).grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text="Generate", command=generate_image).grid(column=2, row=3, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()