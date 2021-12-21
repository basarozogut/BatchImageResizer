import batch_resizer
import batch_resizer_config_helper
import tkinter as tk
import configparser
from tkinter import filedialog, messagebox
import os
from PIL import Image


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.resize_button = tk.Button(self)
        self.resize_button["text"] = "Resize"
        self.resize_button["command"] = self.resize
        self.resize_button.pack(side="left")

        self.quit = tk.Button(self, text="Close", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="left")

    def resize(self):
        fn = filedialog.askopenfilename(title="Choose a file", filetypes=[
                                        ("JPEG File", "*.jpg")], multiple=False)
        if fn:
            cfg = configparser.ConfigParser()
            cfg.read("config.ini")
            sizes_text = cfg["DEFAULT"]["ImageSizes"]
            sizes = batch_resizer_config_helper.parse_image_sizes(sizes_text)

            success = batch_resizer.batch_resize(fn, os.path.dirname(fn), sizes,
                                       resample=Image.BICUBIC, max_size_kilobytes=100, max_quality=95, min_quality=1)

            if success:
                messagebox.showinfo("Success", message="Process succeeded.")
            else:
                messagebox.showerror("Fail", message="Process failed.")


def center_window(root):
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()

    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

    root.geometry("+{}+{}".format(positionRight, positionDown))


root = tk.Tk()
center_window(root)
app = Application(master=root)
app.mainloop()
