from tkinter import *
from tkinter import ttk
import customtkinter


class Kurssi:
    def __init__(self, nimi, osp, arvosana, kategoria):
        self.nimi = nimi
        self.osp = osp
        self.arvosana = arvosana
        self.kategoria = kategoria

    def __str__(self):
        return (
            f"{self.nimi}, {self.osp} osp, arvosana {self.arvosana}, {self.kategoria}"
        )


# Hardcoded values for testing
kurssiX = Kurssi("Apex-maantiede", "22", "4", "väkivaltatutkimus")
kurssiY = Kurssi("Koistisen psyyke", "33", "5", "väkivaltatutkimus")
kurssiZ = Kurssi("Miragen lounas", "2", "hylätty", "juuston alkeet")

kurssit = [kurssiX, kurssiY, kurssiZ]


def render_results():
    i = 0
    for course in kurssit:
        # tab2.grid_columnconfigure((0, 1), weight=1)

        kurssi_label = Label(tab2, text="Kurssin nimi:")
        kurssi_label.grid(row=i, column=0, sticky="ew", pady=(5, 2))

        osp_label = Label(tab2, text="Opintopisteet:")
        osp_label.grid(row=i + 1, column=0, sticky="ew", pady=2)

        arvosana_label = Label(tab2, text="Arvosana:")
        arvosana_label.grid(row=i + 2, column=0, sticky="ew", pady=2)

        kategoria_label = Label(tab2, text="Kategoria:")
        kategoria_label.grid(row=i + 3, column=0, sticky="ew", pady=2)
        # print(course)
        kurssi_data = Label(tab2, text=course.nimi)
        kurssi_data.grid(row=i, column=1, sticky="w", pady=(5, 2), columnspan=2)
        osp_data = Label(tab2, text=course.osp)
        osp_data.grid(row=i + 1, column=1, sticky="w", pady=2, columnspan=2)
        arvosana_data = Label(tab2, text=course.arvosana)
        arvosana_data.grid(row=i + 2, column=1, sticky="w", pady=2, columnspan=2)
        kategoria_data = Label(tab2, text=course.kategoria)
        kategoria_data.grid(row=i + 3, column=1, sticky="w", pady=2, columnspan=2)
        i += 4


def testi():
    kurssi = Kurssi(
        kurssi_input.get(), osp_input.get(), arvosana_input.get(), clicked.get()
    )
    kurssit.append(kurssi)
    # print(kurssi)
    # for x in kurssit:
    #     print(x)
    render_results()


app = Tk()
app.title("Study log")
app.geometry("500x500")

tab_view = ttk.Notebook(app)
tab_view.pack()

tab1 = Frame(tab_view, width=500, height=500)
tab2 = Frame(tab_view, width=500, height=500)

tab1.pack(fill="both", expand=1)
tab2.pack(fill="both", expand=1)

tab_view.add(tab1, text="Add course")
tab_view.add(tab2, text="View courses")
tab_view.pack(expand=True, fill="both")

# Add courses tab
tab1.grid_columnconfigure((0, 1, 2), weight=1)
# tab1.grid_rowconfigure(0, weight=1)

options = ["väkivaltatutkimus", "hylje-biologia", "juuston alkeet", "pönkö"]
clicked = StringVar()
clicked.set("väkivaltatutkimus")

# btn1 = Button(tab2, text="Kokeiles", command=testi).pack()
kurssi_label = Label(tab1, text="Kurssin nimi")
kurssi_label.grid(row=0, column=0, sticky="ew", pady=5)
osp_label = Label(tab1, text="Opintopisteet")
osp_label.grid(row=1, column=0, sticky="ew", pady=5)
arvosana_label = Label(tab1, text="Arvosana")
arvosana_label.grid(row=2, column=0, sticky="ew", pady=5)
kategoria_label = Label(tab1, text="Kategoria")
kategoria_label.grid(row=3, column=0, sticky="ew", pady=5)
kurssi_input = Entry(tab1)
kurssi_input.grid(row=0, column=1, sticky="ew", pady=5, columnspan=2)
osp_input = Entry(tab1)
osp_input.grid(row=1, column=1, sticky="ew", pady=5, columnspan=2)
arvosana_input = Entry(tab1)
arvosana_input.grid(row=2, column=1, sticky="ew", pady=5, columnspan=2)
kategoria_input = OptionMenu(tab1, clicked, *options)
kategoria_input.grid(row=3, column=1, sticky="ew", pady=5, columnspan=2)

btn1 = Button(tab1, text="Lisää", command=testi)
btn1.grid(row=4, column=1, sticky="ew")
# btn1.place(relx=0.5, rely=0.1)

# View courses tab
tab2.grid_columnconfigure((0, 1), weight=1)

# kurssi_label = Label(tab2, text="Kurssin nimi:")
# kurssi_label.grid(row=0, column=0, sticky="ew", pady=5)

# osp_label = Label(tab2, text="Opintopisteet:")
# osp_label.grid(row=1, column=0, sticky="ew", pady=5)

# arvosana_label = Label(tab2, text="Arvosana:")
# arvosana_label.grid(row=2, column=0, sticky="ew", pady=5)

# kategoria_label = Label(tab2, text="Kategoria:")
# kategoria_label.grid(row=3, column=0, sticky="ew", pady=5)
# if len(kurssit) > 0:
#     kurssi_data = Label(tab2, text=kurssi.nimi)
#     kurssi_label.grid(row=0, column=1, sticky="ew", pady=5, columnspan=2)

app.mainloop()

# class MyCheckboxFrame(customtkinter.CTkScrollableFrame):
#     def __init__(self, master, title, values):
#         super().__init__(master)
#         self.grid_columnconfigure(0, weight=1)
#         self.values = values
#         self.title = title
#         self.checkboxes = []

#         self.title = customtkinter.CTkLabel(
#             self, text=self.title, fg_color="gray30", corner_radius=6
#         )
#         self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

#         for i, value in enumerate(self.values):
#             checkbox = customtkinter.CTkCheckBox(self, text=value)
#             checkbox.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
#             self.checkboxes.append(checkbox)

#     def get(self):
#         checked_checkboxes = []
#         for checkbox in self.checkboxes:
#             if checkbox.get() == 1:
#                 checked_checkboxes.append(checkbox.cget("text"))
#         return checked_checkboxes


# class MyRadiobuttonFrame(customtkinter.CTkFrame):
#     def __init__(self, master, title, values):
#         super().__init__(master)
#         self.grid_columnconfigure(0, weight=1)
#         self.values = values
#         self.title = title
#         self.radiobuttons = []
#         self.variable = customtkinter.StringVar(value="")

#         self.title = customtkinter.CTkLabel(
#             self, text=self.title, fg_color="gray30", corner_radius=6
#         )
#         self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

#         for i, value in enumerate(self.values):
#             radiobutton = customtkinter.CTkRadioButton(
#                 self, text=value, value=value, variable=self.variable
#             )
#             radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
#             self.radiobuttons.append(radiobutton)

#     def get(self):
#         return self.variable.get()

#     def set(self, value):
#         self.variable.set(value)


# class MyTabView(customtkinter.CTkTabview):
#     def __init__(self, master):
#         super().__init__(master)
#         self.grid_columnconfigure((0, 1), weight=1)
#         self.grid_rowconfigure(0, weight=1)

#         self.add("YKKÖNEN")
#         self.add("KAKKONEN")

#         self.label = customtkinter.CTkLabel(master, text="YKKÖNEN")
#         self.label.grid(row=0, column=0, padx=20, pady=10)


# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("my app")
#         self.geometry("780x400")

#         self.grid_columnconfigure((0, 1), weight=1)
#         self.grid_rowconfigure(0, weight=1)

#         self.tab_view = MyTabView(master=self)
#         self.tab_view.grid(row=0, column=0, padx=20, pady=20)

#     self.checkbox_frame_1 = MyCheckboxFrame(
#         self,
#         "Values",
#         values=["value 1", "value 2", "value 3"],
#     )
#     self.checkbox_frame_1.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsw")
#     self.button = customtkinter.CTkButton(
#         self, text="my button", command=self.button_callback
#     )
#     self.radiobutton_frame = MyRadiobuttonFrame(
#         self, "Options", values=["option 1", "option 2"]
#     )
#     self.radiobutton_frame.grid(
#         row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=2
#     )
#     self.button = customtkinter.CTkButton(
#         self, text="my button", command=self.button_callback
#     )

#     self.button.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

# def button_callback(self):
#     print("checkbox_frame", self.checkbox_frame_1.get())
#     print("radiobutton_frame", self.radiobutton_frame.get())


# app = App()
# app.mainloop()

# customtkinter.set_appearance_mode("System")
# customtkinter.set_default_color_theme("blue")

# app = customtkinter.CTk()
# app.geometry("720x480")
# app.grid_columnconfigure((0, 1), weight=1)
# app.title("Study log")

# Create tabs
# tabview = customtkinter.CTkTabview(app)
# tabview.pack(padx=0, pady=0)

# tabview.add("Add course")  # add tab at the end
# tabview.add("View courses")  # add tab at the end
# tabview.set("View courses")  # set currently visible tab

# button_1 = customtkinter.CTkButton(tabview.tab("Add course"))
# button_1.pack(padx=20, pady=20)


# def button_function():
#     print("button pressed")


# # Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# button.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
# # button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

# checkbox_1 = customtkinter.CTkCheckBox(app, text="checkbox 1")
# checkbox_1.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
# checkbox_2 = customtkinter.CTkCheckBox(app, text="checkbox 2")
# checkbox_2.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")

# teksti = customtkinter.CTkLabel(app, text="ASDFASDF")
# teksti.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)
# teksti.pack()

# app.mainloop()


# class MyTabView(customtkinter.CTkTabview):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

#         # create tabs
#         self.add("Add course")
#         self.add("View courses")

#         # add widgets on tabs
#         self.label = customtkinter.CTkLabel(master=self.tab("Add course"))
#         self.label.grid(row=0, column=0, padx=20, pady=10)


# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()

#         self.tab_view = MyTabView(master=self)
#         self.tab_view.grid(row=0, column=0, padx=20, pady=20)
#         teksti = customtkinter.CTkLabel(self, text="ASDFASDF")
#         teksti.pack()


# app = App()
# app.mainloop()
