from tkinter import *
from tkinter import ttk
import customtkinter
import sqlite3

# Establish db connection or create new
conn = sqlite3.connect("course_data.db")

# create cursor
c = conn.cursor()

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

        width = 600
        height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        # self.configure(fg_color="lightgrey")
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
        self.configure(fg_color="lightgrey")

        self.tab1 = Tab1(master=self.tab("Lisää kurssi"))
        self.tab1.pack(fill="both", expand=True, padx=0, pady=0)

        self.tab2 = Tab2(master=self.tab("Näytä kaikki"))
        self.tab2.pack(fill="both", expand=True, padx=0, pady=0)
        # self.button_1 = customtkinter.CTkButton(self.tab("Lisää kurssi"))
        # self.button_2 = customtkinter.CTkButton(self.tab("Näytä kaikki"))


class Tab1(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # self.pack(fill="both", expand=True, padx=50, pady=50)
        self.configure(fg_color="lightgrey")
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
        self.saveBtn = customtkinter.CTkButton(
            self, text="Lisää", command=self.save_data
        )
        self.saveBtn.grid(row=5, column=1, sticky="ew")

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    def save_data(self):
        # Insert into table
        c.execute(
            "INSERT INTO courses VALUES (:course_name, :osp, :grade, :category)",
            {
                "course_name": self.kurssi_input.get(),
                "osp": self.osp_input.get(),
                "grade": self.arvosana_input.get(),
                "category": self.kategoria_input.get(),
            },
        )

        conn.commit()

        c.execute(
            "SELECT oid FROM courses WHERE courses.name = :course_name",
            {"course_name": self.kurssi_input.get()},
        )

        course_oid = c.fetchall()

        # print(course_oid[0][0])

        if len(self.muistiinpanot_input.get("1.0", "end-1c")) < 1:
            course_notes = "---"
        else:
            course_notes = self.muistiinpanot_input.get("1.0", "end-1c")

        c.execute(
            "INSERT INTO notes VALUES (:course_id, :note)",
            {
                "course_id": course_oid[0][0],
                "note": course_notes,
            },
        )
        conn.commit()

        self.kurssi_input.delete(0, END)
        self.osp_input.delete(0, END)
        self.arvosana_input.delete(0, END)
        self.muistiinpanot_input.delete("0.0", END)
        # render_results(fetch_saved_data())


#     # conn.close()


class Tab2(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1), weight=1)
        self.data = self.fetch_data()
        self.configure(fg_color="lightgrey")
        self.arvosana = self.fetch_grade()
        # self.arvosana = 0
        self.arvosanat_lasketut = 0
        self.osp = self.fetch_osp()
        self.op_category = 0

        # self.testBtn = customtkinter.CTkButton(self, text="Kokeile", command=self.nappi)
        # self.testBtn.grid(row=2, column=0, sticky="ew")

        self.columns = ("course_name", "osp", "grade", "category")

        self.tree = ttk.Treeview(master=self, columns=self.columns, show="headings")
        self.tree.column("course_name", width=150, anchor=W)
        self.tree.column("osp", width=100, anchor=W)
        self.tree.column("grade", width=100, anchor=CENTER)
        self.tree.column("category", width=150, anchor=CENTER)

        # define headings
        self.tree.heading("course_name", text="Kurssin nimi")
        self.tree.heading("osp", text="Op.")
        self.tree.heading("grade", text="Arvosana")
        self.tree.heading("category", text="Kategoria")

        # add data to the treeview
        for course in self.data:
            temp = (
                course[0],
                course[1],
                course[2].capitalize(),
                course[3].capitalize(),
                course[4],
            )
            self.tree.insert("", END, values=temp)

        self.tree.bind("<<TreeviewSelect>>", self.item_selected)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Frame for courses tabs' control widgets
        self.controlFrame = customtkinter.CTkFrame(self)
        self.controlFrame.configure(fg_color="lightgrey")
        self.controlFrame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.controlFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.arvosana_label = customtkinter.CTkLabel(
            self.controlFrame,
            text=f"Keskiarvo: {str(self.arvosana)}",
            font=("Helvetica", 10, "bold"),
        )
        self.arvosana_label.grid(row=1, column=0, sticky="w", pady=2)

        self.osp_label = customtkinter.CTkLabel(
            self.controlFrame,
            text=f"Opintopisteet: {self.op_category} (yht. {self.osp})",
            font=("Helvetica", 10, "bold"),
        )
        self.osp_label.grid(row=1, column=1, sticky="ew", pady=2)
        self.deleteBtn = customtkinter.CTkButton(self.controlFrame, text="Poista")

        self.deleteBtn.grid(row=0, column=0, sticky="ew", pady=(5, 2))
        self.deleteBtn.bind("<Button-1>", self.delete_course)
        # self.tree.bind("<<TreeviewSelect>>", self.delete_course)

        self.courseNotesBox = customtkinter.CTkTextbox(self.controlFrame, height=100)
        self.courseNotesBox.grid(row=3, column=0, sticky="ew", pady=(5, 2))
        # self.courseNotesBox.insert("0.0", notesData[0][0])

        # Sorting
        self.options = [
            "kaikki",
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
        self.clicked = customtkinter.StringVar(value="kaikki")

        # Find the size of the longest word in optionMenu and use it as width to stop widget from resizing
        self.menu_width = len(max(self.options, key=len))

        self.lajittelu_input = customtkinter.CTkOptionMenu(
            self.controlFrame, values=self.options, command=self.optionmenu_callback
        )
        self.lajittelu_input.configure(width=self.menu_width)
        self.lajittelu_input.grid(
            row=0, column=2, sticky="ew", pady=(5, 2), columnspan=2
        )

        self.updateBtn = customtkinter.CTkButton(self.controlFrame, text="Päivitä")
        self.updateBtn.grid(row=4, column=0, sticky="ew", pady=(5, 200))
        self.updateBtn.bind("<Button-1>", self.updateNotes)

    def optionmenu_callback(self, event):
        print("optionmenu dropdown clicked:", event)
        # return
        # updateSort()

    def fetch_data(self):
        c.execute("SELECT *, oid FROM courses")
        data = c.fetchall()
        return data
        # print(data)

    def fetch_osp(self):
        c.execute("SELECT SUM(osp) FROM courses")
        data = c.fetchall()
        return data[0][0]

    def nappi(self):
        print(self.osp)
        print(self.data)

    def delete_course(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item["values"]
            c.execute(f"SELECT *, oid FROM courses WHERE oid = {record[4]}")
            data = c.fetchall()

            # SQL command to delete based on oid. Then update
            c.execute(f"DELETE FROM courses WHERE oid = {data[0][4]}")
            conn.commit()
            c.execute(f"DELETE FROM notes WHERE course_id = {data[0][4]}")
            conn.commit()

            #     updateSort()

    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item["values"]
            c.execute(f"SELECT *, oid FROM courses WHERE oid = {record[4]}")
            tieto = c.fetchall()

            # Notes section
            c.execute(
                "SELECT note FROM notes WHERE course_id = :course_id",
                {"course_id": tieto[0][4]},
            )
            notesData = c.fetchall()
            self.courseNotesBox.delete("0.0", END)
            try:
                self.courseNotesBox.insert("0.0", notesData[0][0])
            except:
                continue

    # Identify UPDATE call and send data forward to be updated in table
    def updateNotes(self, event):
        # print(event)
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item["values"]
            newNote = self.courseNotesBox.get("1.0", "end-1c")

            c.execute(f"SELECT * FROM notes WHERE course_id = {record[4]}")
            existingNote = c.fetchall()

            if len(existingNote) < 1:
                c.execute(
                    "INSERT INTO notes VALUES (:course_id, :note)",
                    {
                        "course_id": record[4],
                        "note": newNote,
                    },
                )
                conn.commit()
            else:
                c.execute(
                    "UPDATE notes SET note = :new_note WHERE course_id = :notes_id",
                    {"new_note": newNote, "notes_id": record[4]},
                )
                conn.commit()

    def fetch_grade(self):
        grades = []
        c.execute("SELECT grade FROM courses")
        data = c.fetchall()
        for grade in data:
            try:
                grades.append(int(grade[0]))
            except:
                continue
        return round(sum(grades) / len(grades), 1)

    # def render_results(self, courses):
    #     for course in courses:
    #         self.op_category += int(course[1])
    #         try:
    #             self.arvosana += int(course[2])
    #             self.arvosanat_lasketut += 1
    #         except:
    #             continue
    #     if self.arvosana == 0:
    #         self.arvosana = str("-----")
    #     else:
    #         self.arvosana = self.arvosana / self.arvosanat_lasketut
    #         self.arvosana = round(self.arvosana, 1)

    # self.render_results(self.fetch_data())


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

# render_results(fetch_saved_data())

app = App()
app.mainloop()
