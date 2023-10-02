import customtkinter
import os
from PIL import Image

import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from backend.DbController import DbController
from backend.FileReader import FileReader
from backend.DataHandeling import DataHandeling
from backend.CalculateEdwardsTrimp import CalculateEdwardsTrimp
from backend.Athlete import Athelete



class Entryform(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.data = ()
        self.testdata = ()


        self.entry_frame = customtkinter.CTkFrame(master, width=1040, corner_radius=5)
        self.entry_frame.grid(row=0, column=0,  sticky="nsew", padx=10, pady=10)
        self.entry_frame.grid_columnconfigure(0, weight=0)

        self.title = customtkinter.CTkLabel(self.entry_frame, text="Athlete Entry Form",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.entry_first_name_label = customtkinter.CTkLabel(self.entry_frame, text='First Name:', anchor='w')
        self.entry_first_name_label.grid(row=1, column=0, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.entry_last_name_label = customtkinter.CTkLabel(self.entry_frame, text='Last Name:', anchor='w')
        self.entry_last_name_label.grid(row=1, column=2, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.entry_first_name = customtkinter.CTkEntry(self.entry_frame, width= 400, placeholder_text="first name")
        self.entry_first_name.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=(10, 20), sticky="nsew")


        self.entry_last_name = customtkinter.CTkEntry(self.entry_frame, width=400, placeholder_text="last name")
        self.entry_last_name.grid(row=2, column=2, columnspan=2, padx=(20, 0), pady=(10, 20), sticky="nse")

        self.max_hr_label = customtkinter.CTkLabel(self.entry_frame, text='Maximal Heart Rate:', anchor='w')
        self.max_hr_label.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.rest_hr_label = customtkinter.CTkLabel(self.entry_frame, text='Resting Heart Rate:', anchor='w')
        self.rest_hr_label.grid(row=3, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.vo2max_label = customtkinter.CTkLabel(self.entry_frame, text="VO2max Value:", anchor='w')
        self.vo2max_label.grid(row=3, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.max_hr = customtkinter.CTkEntry(self.entry_frame, width=200, placeholder_text="maximal heart rate")
        self.max_hr.grid(row=4, column=1, padx=(20, 0), pady=(10, 20), sticky="nsw")

        self.rest_hr = customtkinter.CTkEntry(self.entry_frame, width=200,  placeholder_text="resting heart rate")
        self.rest_hr.grid(row=4, column=0, padx=(20, 0), pady=(10, 20), sticky="nsw")

        self.vo2max = customtkinter.CTkEntry(self.entry_frame, width=200, placeholder_text="VO2max")
        self.vo2max.grid(row=4, column=2, padx=(20, 0), pady=(10, 20), sticky="nsw")


        self.select_athlete_data_label = customtkinter.CTkLabel(self.entry_frame, text='select data of athlete', anchor='w')
        self.select_athlete_data_label.grid(row=5, column=0, padx=(20,0), pady=(20,0))

        self.select_athlete_test_data_label = customtkinter.CTkLabel(self.entry_frame, text='select test data of athlete',
                                                                    anchor='w')
        self.select_athlete_test_data_label.grid(row=7, column=0, padx=(20, 0), pady=(20, 0))

        self.select_athlete_data = customtkinter.CTkButton(self.entry_frame, text='select', command=lambda: self.select_athlete_data_meth('fit'))
        self.select_athlete_data.grid(row=6, column=0, padx=(20, 0), pady=10)

        self.select_athlete_test_data = customtkinter.CTkButton(self.entry_frame, text='select', command=lambda: self.select_athlete_data_meth('csv'))
        self.select_athlete_test_data.grid(row=8, column=0, padx=(20, 0), pady=10)

        self.input_athelte_data = customtkinter.CTkButton(self.entry_frame, text='Enter', hover_color='#098F00', font=customtkinter.CTkFont(weight="bold"), command=lambda: self.input_athlete_data_meth())
        self.input_athelte_data.grid(row=8, column=2, padx=(20, 0), pady=10)

    def select_athlete_data_meth(self, filetype):
        filenames = filedialog.askopenfilename(title=f'select a .{filetype} file',
                                              filetypes=((f"{filetype} files", f"*.{filetype}"), ("all files", "*.*")), multiple=True)

        if filetype == 'fit':
            self.data=()
            self.data= filenames


        else:
            self.testdata=()
            self.testdata= filenames


        return filenames

    def delete_entries(self):
        self.entry_last_name.delete(0, 'end')
        self.entry_first_name.delete(0, 'end')
        self.max_hr.delete(0, 'end')
        self.rest_hr.delete(0, 'end')
        self.vo2max.delete(0, 'end')

    def input_athlete_data_meth(self):
        try:
            datahand = DataHandeling()
            lastname = self.entry_last_name.get()
            firstname = self.entry_first_name.get()
            max_hr = int(self.max_hr.get())
            rest_hr = int(self.rest_hr.get())
            vo2max = float(self.vo2max.get())
            filelist = self.data
            print(filelist)

            athlete = Athelete(lastname, firstname, max_hr, rest_hr, vo2max, filelist)
            athlete.save_athelte_to_db()
            self.delete_entries()

            filereader = FileReader(self.data)
            athleteid = athlete.get_id_athlete_by_name()

            filereader.writeCsv()
            filereader.saveIntoDb(athleteid)

            table = "trainingdata"
            column = "heart_rate"
            datahand.deleteMissing(table, column)

            calculateEdwarsTrimp = CalculateEdwardsTrimp()
            calculateEdwarsTrimp.EdwardsTRIMP(athleteid)

            CTkMessagebox(message="athlete is succesfully added", title='skibambam',
                          icon="check", option_1="Ok")


        except ValueError as e:
            print(f"Caught ValueError: {e}")
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
        except TypeError as e:
            print(f"Caught TypeError: {e}")
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

