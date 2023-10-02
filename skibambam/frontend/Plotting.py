import customtkinter
import os
from PIL import Image

import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
from backend.DataHandeling import DataHandeling
from backend.DbController import DbController



class Plotting(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.plotting_frame = customtkinter.CTkFrame(master, width=1040, corner_radius=5)
        self.plotting_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.plotting_frame.grid_columnconfigure(0, weight=0)
        #self.entry_frame.grid_columnconfigure(1, weight=1)

        self.title = customtkinter.CTkLabel(self.plotting_frame,
                                            text="Plotting of Data",
                                            font=customtkinter.CTkFont(size=20, weight="bold"),
                                            anchor='w')
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.select_athlete_label = customtkinter.CTkLabel(self.plotting_frame,
                                                           text='Wich Athelte do you want to recieve the plots?',
                                                           anchor='w')
        self.select_athlete_label.grid(row=1, column=0, padx=20, pady=(20,0))


        self.datahandeling = DataHandeling()
        values = self.datahandeling.athlete_full_name()

        self.optionmenu_var = customtkinter.StringVar(value='choose athlete')
        self.athelte_dropdown = customtkinter.CTkOptionMenu(self.plotting_frame,
                                                            values=values,
                                                            command=self.athlete_drop_down,
                                                            variable=self.optionmenu_var,
                                                            width=600)
        self.athelte_dropdown.grid(row=2, column=0, padx=20, pady=(20,0))

        self.select_athlete_label = customtkinter.CTkLabel(self.plotting_frame,
                                                           text='which training load do you want to use',
                                                           anchor='w')
        self.select_athlete_label.grid(row=3, column=0, padx=20, pady=(20, 0))

        tl_values = self.datahandeling.return_list_off_tl_types()
        self.optionmenu_var = customtkinter.StringVar(value='choose training load')
        self.athelte_dropdown = customtkinter.CTkOptionMenu(self.plotting_frame,
                                                            values=tl_values,
                                                            command=self.tl_drop_down,
                                                            variable=self.optionmenu_var,
                                                            width=600)
        self.athelte_dropdown.grid(row=4, column=0, padx=20, pady=(20,0))

        self.deletedb = customtkinter.CTkButton(self.plotting_frame, text='plot it', command=self.plot,
                                                hover_color='#098F00')
        self.deletedb.grid(row=6, column=3, padx=20, pady=(10, 0))




    def athlete_drop_down(self, choice):
        self.athlete_id = ''

        choice = str(choice)
        choice = choice.split(' ')
        first_name = choice[0]
        last_name = choice[1]

        name_tuple = (first_name, last_name)
        athelte_id = self.datahandeling.returns_an_athlete_id_on_basis_of_first_second_name(name_tuple)
        athelte_id = athelte_id[0]
        athelte_id = athelte_id[0]
        self.athlete_id = athelte_id



    def tl_drop_down(self, choice):
        self.tl_id=''
        tl_id = ''

        tl_id = self.datahandeling.get_id_tl(choice)
        tl_id = tl_id[0]
        tl_id = tl_id[0]
        self.tl_id = tl_id

    def plot(self):
        self.datahandeling.plot_it(self.tl_id, self.athlete_id)

