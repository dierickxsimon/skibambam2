import customtkinter
import os
from PIL import Image

import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog


class Exportdata(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.entry_frame = customtkinter.CTkFrame(master, width=1040, corner_radius=5)
        self.entry_frame.grid(row=0, column=0,  sticky="nsew", padx=10, pady=10)
        self.entry_frame.grid_columnconfigure(0, weight=0)
        #self.entry_frame.grid_columnconfigure(1, weight=1)

        self.title = customtkinter.CTkLabel(self.entry_frame, text="Export Data",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10))