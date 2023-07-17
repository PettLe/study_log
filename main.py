from tkinter import *
from tkinter import ttk
import customtkinter
import sqlite3

# Establish db connection or create new
conn = sqlite3.connect("course_data.db")

# create cursor
c = conn.cursor()

# FIRST TIME create a table
# c.execute(
#     """
#           CREATE TABLE courses (
#               name TEXT,
#               osp INTEGER,
#               grade TEXT,
#               category TEXT
#           )
#           """
# )

# c.execute(
#     """
# CREATE TABLE notes (
#     course_id INTEGER,
#     note TEXT
# )
# """
# )

# If need to clear widgets from overall:
# for child in tab2.grid_slaves():
#     if int(child.grid_info()["row"]) >= 1:
#         child.grid_remove()


# Custom system settings
system_theme = "light"
customtkinter.set_appearance_mode(system_theme)
# customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        width = 500
        height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.title("Kaisan opiskelu log!")
        self.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.grid_columnconfigure((0, 1), weight=1)
        self.tab_view = TabView(master=self)
        self.tab_view.pack(fill="both", expand=True, padx=20, pady=20)
        # self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # self.tab1 = Tab1(master=self.tab_view)


class TabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Lisää kurssi")
        self.add("Näytä kaikki")

        # self.teksti = customtkinter.CTkLabel(master=self.tab("Lisää kurssi"))
        # self.teksti.grid(row=0, column=0, padx=20, pady=10)
        # self.pack(expand=True, fill="both")
        self.tab1 = Tab1(master=self.tab("Lisää kurssi"))
        self.tab1.pack(fill="both", expand=True, padx=0, pady=0)

        self.tab2 = Tab2(master=self.tab("Näytä kaikki"))
        self.tab2.pack(fill="both", expand=True, padx=0, pady=0)
        # self.tab1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        # self.button_1 = customtkinter.CTkButton(self.tab("Lisää kurssi"))
        # self.button_2 = customtkinter.CTkButton(self.tab("Näytä kaikki"))

        # button_1 = customtkinter.CTkButton(self.tab("Lisää kurssi"))
        # button_2 = customtkinter.CTkButton(self.tab("Näytä kaikki"))


class Tab1(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # self.pack(fill="both", expand=True, padx=0, pady=0)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.kurssi_label = customtkinter.CTkLabel(self, text="Kurssin nimi")
        self.kurssi_label.grid(row=0, column=0, sticky="ew", pady=5)
        self.osp_label = customtkinter.CTkLabel(self, text="Opintopisteet")
        self.osp_label.grid(row=1, column=0, sticky="ew", pady=5)
        self.arvosana_label = customtkinter.CTkLabel(self, text="Arvosana")
        self.arvosana_label.grid(row=2, column=0, sticky="ew", pady=5)
        self.muistiinpanot_label = customtkinter.CTkLabel(self, text="Muistiinpanot")
        self.muistiinpanot_label.grid(row=3, column=0, sticky="ew", pady=5)
        self.kategoria_label = customtkinter.CTkLabel(self, text="Kategoria")
        self.kategoria_label.grid(row=4, column=0, sticky="ew", pady=5)
        self.kurssi_input = customtkinter.CTkEntry(self)
        self.kurssi_input.grid(row=0, column=1, sticky="ew", pady=5, columnspan=2)
        self.osp_input = customtkinter.CTkEntry(self)
        self.osp_input.grid(row=1, column=1, sticky="ew", pady=5, columnspan=2)
        self.arvosana_input = customtkinter.CTkEntry(self)
        self.arvosana_input.grid(row=2, column=1, sticky="ew", pady=5, columnspan=2)

        self.options = [
            "väkivaltatutkimus",
            "sukupuolentutkimus",
            "digimarkkinointi",
            "vastuullisuus & kestävä kehitys",
            "tilastotiede",
            "tekoäly",
            "muu",
            "hylje-biologia",
            "juuston alkeet",
            "pönkö",
        ]
        clicked = customtkinter.StringVar(value="väkivaltatutkimus")
        clicked.set("väkivaltatutkimus")

        self.kategoria_input = customtkinter.CTkOptionMenu(
            self, values=self.options, command=self.optionmenu_callback
        )
        self.muistiinpanot_input = customtkinter.CTkTextbox(self, height=100)
        self.muistiinpanot_input.grid(
            row=3, column=1, sticky="ew", pady=5, columnspan=2
        )
        self.kategoria_input.grid(row=4, column=1, sticky="w", pady=5, columnspan=2)

        # Save Button
        self.saveBtn = customtkinter.CTkButton(self, text="Lisää", command=self.test)
        self.saveBtn.grid(row=5, column=1, sticky="ew")

    def test(self):
        print("Ohalalalaa")

    def optionmenu_callback(self, choice):
        # updateSort()
        print("optionmenu dropdown clicked:", choice)


class Tab2(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.data = self.fetch_data()

        self.testBtn = customtkinter.CTkButton(self, text="Kokeile", command=self.nappi)
        self.testBtn.grid(row=0, column=1, sticky="ew")

    def fetch_data(self):
        c.execute("SELECT * FROM courses")
        data = c.fetchall()
        return data
        # print(data)

    def nappi(self):
        print(self.data)


# # kurssi_input.get(), osp_input.get(), arvosana_input.get(), clicked.get()
# def save_data():
#     # Insert into table
#     c.execute(
#         "INSERT INTO courses VALUES (:course_name, :osp, :grade, :category)",
#         {
#             "course_name": kurssi_input.get(),
#             "osp": osp_input.get(),
#             "grade": arvosana_input.get(),
#             "category": kategoria_input.get(),
#         },
#     )

#     conn.commit()

#     c.execute(
#         "SELECT oid FROM courses WHERE courses.name = :course_name",
#         {"course_name": kurssi_input.get()},
#     )

#     course_oid = c.fetchall()

#     # print(course_oid[0][0])

#     if len(muistiinpanot_input.get("1.0", "end-1c")) < 1:
#         course_notes = "---"
#     else:
#         course_notes = muistiinpanot_input.get("1.0", "end-1c")

#     c.execute(
#         "INSERT INTO notes VALUES (:course_id, :note)",
#         {
#             "course_id": course_oid[0][0],
#             "note": course_notes,
#         },
#     )

#     kurssi_input.delete(0, END)
#     osp_input.delete(0, END)
#     arvosana_input.delete(0, END)
#     muistiinpanot_input.delete("0.0", END)
#     render_results(fetch_saved_data())
#     # conn.close()


# def fetch_saved_data():
#     c.execute("SELECT *, oid FROM courses")
#     data = c.fetchall()
#     conn.commit()
#     return data


# def delete_course(item):
#     # SQL command to delete based on oid. Then update
#     c.execute(f"DELETE FROM courses WHERE oid = {item[0][4]}")
#     conn.commit()
#     c.execute(f"DELETE FROM notes WHERE course_id = {item[0][4]}")
#     conn.commit()
#     updateSort()


# def update_notes(notesTuple):
#     c.execute(
#         "UPDATE notes SET note = :new_note WHERE course_id = :notes_id",
#         {"new_note": notesTuple[0], "notes_id": notesTuple[1]},
#     )
#     conn.commit()


# # Render the contents of overall tab
# def render_results(courses):
#     c.execute("SELECT SUM(osp) FROM courses")
#     data = c.fetchall()
#     arvosana = 0
#     arvosanat_lasketut = 0
#     osp = data[0][0]
#     op_category = 0
#     # print(courses)

#     for course in courses:
#         op_category += int(course[1])
#         try:
#             arvosana += int(course[2])
#             arvosanat_lasketut += 1
#         except:
#             continue
#     if arvosana == 0:
#         arvosana = str("-----")
#     else:
#         arvosana = arvosana / arvosanat_lasketut
#         arvosana = round(arvosana, 1)

#     columns = ("course_name", "osp", "grade", "category")

#     tree = ttk.Treeview(tab2, columns=columns, show="headings")
#     tree.column("course_name", width=150, anchor=W)
#     tree.column("osp", width=100, anchor=W)
#     tree.column("grade", width=100, anchor=CENTER)
#     tree.column("category", width=150, anchor=CENTER)

#     # define headings
#     tree.heading("course_name", text="Kurssin nimi")
#     tree.heading("osp", text="Op.")
#     tree.heading("grade", text="Arvosana")
#     tree.heading("category", text="Kategoria")

#     # add data to the treeview
#     for course in courses:
#         temp = (
#             course[0],
#             course[1],
#             course[2].capitalize(),
#             course[3].capitalize(),
#             course[4],
#         )
#         tree.insert("", END, values=temp)

#     def item_selected(event):
#         for selected_item in tree.selection():
#             item = tree.item(selected_item)
#             record = item["values"]
#             c.execute(f"SELECT *, oid FROM courses WHERE oid = {record[4]}")
#             tieto = c.fetchall()

#             # Notes section
#             c.execute(
#                 "SELECT note FROM notes WHERE course_id = :course_id",
#                 {"course_id": tieto[0][4]},
#             )
#             notesData = c.fetchall()

#             courseNotesBox = customtkinter.CTkTextbox(controlFrame, height=100)
#             courseNotesBox.grid(row=3, column=0, sticky="ew", pady=(5, 2))
#             courseNotesBox.insert("0.0", notesData[0][0])

#         # Identify UPDATE call and send data forward to be updated in table
#         def identifyClick(event):
#             newNote = courseNotesBox.get("1.0", "end-1c")
#             update_notes((newNote, tieto[0][4]))

#         updateBtn = customtkinter.CTkButton(
#             controlFrame,
#             text="Päivitä",
#             command=lambda id=(): identifyClick(event),
#         )
#         updateBtn.grid(row=4, column=0, sticky="ew", pady=(5, 2))

#         deleteBtn = customtkinter.CTkButton(
#             controlFrame,
#             text="Poista",
#             command=lambda id=tieto: delete_course(id),
#         )
#         deleteBtn.grid(row=0, column=0, sticky="ew", pady=(5, 2))

#     tree.bind("<<TreeviewSelect>>", item_selected)

#     tree.grid(row=0, column=0, sticky="nsew")

#     # add a scrollbar
#     scrollbar = ttk.Scrollbar(tab2, orient=VERTICAL, command=tree.yview)
#     tree.configure(yscroll=scrollbar.set)
#     scrollbar.grid(row=0, column=1, sticky="ns")

#     # EMPTY delete button to hide mistakes, oops
#     deleteBtn = customtkinter.CTkButton(controlFrame, text="Poista")
#     deleteBtn.grid(row=0, column=0, sticky="ew", pady=(5, 2))

#     arvosana_label = customtkinter.CTkLabel(
#         controlFrame, text=f"Keskiarvo: {str(arvosana)}", font=("Helvetica", 10, "bold")
#     )
#     arvosana_label.grid(row=1, column=0, sticky="w", pady=2)

#     osp_label = customtkinter.CTkLabel(
#         controlFrame,
#         text=f"Opintopisteet: {op_category} (yht. {osp})",
#         font=("Helvetica", 10, "bold"),
#     )
#     osp_label.grid(row=1, column=1, sticky="ew", pady=2)


# def updateSort():
#     temp = []
#     data = fetch_saved_data()
#     if lajittelu_input.get() == "kaikki":
#         render_results(fetch_saved_data())
#     else:
#         for course in data:
#             if course[3] == lajittelu_input.get():
#                 temp.append(course)
#             else:
#                 continue
#         render_results(temp)


# tab1 = tab_view.add("Lisää kurssi")
# tab2 = tab_view.add("Näytä kaikki")
# tab_view.pack(expand=True, fill="both")


# View courses tab
# tab2 = customtkinter.CTkFrame(tab_view, width=500, height=500)
# tab2.pack(fill="both", expand=1)
# tab2.grid_columnconfigure((0, 1), weight=1)


# # Frame for courses tabs' control widgets
# controlFrame = customtkinter.CTkFrame(tab2)
# controlFrame.grid(row=1, column=0, columnspan=2, sticky="ew")
# controlFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)


# # Sorting
# options2 = [
#     "kaikki",
#     "väkivaltatutkimus",
#     "sukupuolentutkimus",
#     "digimarkkinointi",
#     "vastuullisuus & kestävä kehitys",
#     "tilastotiede",
#     "tekoäly",
#     "muu",
#     "hylje-biologia",
#     "juuston alkeet",
#     "pönkö",
# ]
# clicked2 = customtkinter.StringVar(value="kaikki")

# # Find the size of the longest word in optionMenu and use it as width to stop widget from resizing
# menu_width = len(max(options2, key=len))


# def optionmenu_callback(choice):
#     updateSort()
#     # print("optionmenu dropdown clicked:", choice)


# lajittelu_input = customtkinter.CTkOptionMenu(
#     controlFrame, values=options2, command=optionmenu_callback
# )
# lajittelu_input.configure(width=menu_width)
# lajittelu_input.grid(row=0, column=2, sticky="ew", pady=(5, 2), columnspan=2)


# def optionmenu_callback(choice):
#     return
#     # print("optionmenu dropdown clicked:", choice)

# render_results(fetch_saved_data())

app = App()
app.mainloop()
