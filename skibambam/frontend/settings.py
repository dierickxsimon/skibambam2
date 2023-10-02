import customtkinter
import os
from PIL import Image

import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from backend.DbController import DbController



class Settings(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.settings_frame = customtkinter.CTkFrame(master, width=1040, corner_radius=5)
        self.settings_frame.grid(row=0, column=0,  sticky="nsew", padx=10, pady=10)
        self.settings_frame.grid_columnconfigure(0, weight=0)

        self.title = customtkinter.CTkLabel(self.settings_frame, text="Settings",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.settings_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.settings_frame, values=["Dark", "Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.settings_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.settings_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=4, column=0, padx=20, pady=(10, 20))
        self.deletedb = customtkinter.CTkButton(self.settings_frame, text='delete data', command=self.deletedb, hover_color='#D80000')
        self.deletedb.grid(row=2, column=2, padx=20, pady=(10,0))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def deletedb(self):
        dbc = DbController()
        dbc.deletedb()
        CTkMessagebox(message="succesfully deleted db",
                      icon="check", option_1="Thanks")