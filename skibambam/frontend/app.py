import customtkinter

from Entryform import Entryform
from Exportdata import Exportdata
from Plotting import Plotting
from settings import Settings
from backend.DbController import DbController

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("version 1.0")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Skibambam",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Athlete entry form",
                                                        command=self.create_entryform)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="plotting", command=self.plotting)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="exporting data",
                                                        command=self.exportdata)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.options_button = customtkinter.CTkButton(self.sidebar_frame, text='settings', command=self.settings)
        self.options_button.grid(row=7, column=0, padx=20, pady=10)

        self.full_frame = customtkinter.CTkFrame(self, width=1040, corner_radius=0)
        self.full_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
        self.full_frame.grid_rowconfigure(0, weight=1)
        self.full_frame.grid_columnconfigure(0, weight=1)

    def create_entryform(self):
        Entryform(self.full_frame)

    def exportdata(self):
        Exportdata(self.full_frame)

    def plotting(self):
        Plotting(self.full_frame)

    def settings(self):
        Settings(self.full_frame)


    dbc = DbController()
    conn = dbc.getConnection()
    conn.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()