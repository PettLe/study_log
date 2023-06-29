from tkinter import *
from tkinter import ttk
import customtkinter
import sqlite3

# import json

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


# class for courses
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
kurssit_testi = []


# kurssi_input.get(), osp_input.get(), arvosana_input.get(), clicked.get()
def save_data():
    # Insert into table
    c.execute(
        "INSERT INTO courses VALUES (:course_name, :osp, :grade, :category)",
        {
            "course_name": kurssi_input.get(),
            "osp": osp_input.get(),
            "grade": arvosana_input.get(),
            "category": clicked.get(),
        },
    )

    conn.commit()
    for child in tab2.grid_slaves():
        if int(child.grid_info()["row"]) >= 1:
            child.grid_remove()
    kurssi_input.delete(0, END)
    osp_input.delete(0, END)
    arvosana_input.delete(0, END)
    render_results(fetch_saved_data())
    # conn.close()


def fetch_saved_data():
    c.execute("SELECT *, oid FROM courses")
    data = c.fetchall()
    print(data)
    # c.execute("DELETE FROM courses WHERE oid = 1")
    conn.commit()
    return data
    # conn.close()


def delete_course():
    c.execute("SELECT oid FROM courses")
    data = c.fetchall()
    print(data)


# Render the contents of overall tab
def render_results(courses):
    # courses = fetch_saved_data()
    for child in tab2.grid_slaves():
        if int(child.grid_info()["row"]) >= 1:
            child.grid_remove()
    i = 1
    arvosana = 0
    arvosanat_lasketut = 0
    osp = 0
    for course in courses:
        osp += int(course[1])
        try:
            arvosana += int(course[2])
            arvosanat_lasketut += 1
        except:
            continue
    if arvosana == 0:
        arvosana = "-"
    else:
        arvosana = arvosana / arvosanat_lasketut

    # Render labels for each category
    kurssi_label = Label(tab2, text="Kurssin nimi:")
    kurssi_label.grid(row=i, column=0, sticky="ew", pady=(5, 2))

    osp_label = Label(tab2, text="Opintopisteet:")
    osp_label.grid(row=i, column=1, sticky="ew", pady=2)

    arvosana_label = Label(tab2, text="Arvosana:")
    arvosana_label.grid(row=i, column=2, sticky="ew", pady=2)

    kategoria_label = Label(tab2, text="Kategoria:")
    kategoria_label.grid(row=i, column=3, sticky="ew", pady=2)

    for course in courses:
        kurssi_data = Label(tab2, text=course[0])
        kurssi_data.grid(row=i + 1, column=0, sticky="w", pady=(5, 2))
        osp_data = Label(tab2, text=course[1])
        osp_data.grid(row=i + 1, column=1, sticky="ew", pady=2)
        arvosana_data = Label(tab2, text=course[2])
        arvosana_data.grid(row=i + 1, column=2, sticky="ew", pady=2)
        kategoria_data = Label(tab2, text=course[3])
        kategoria_data.grid(row=i + 1, column=3, sticky="w", pady=2)

        # Delete button
        deleteBtn = Button(tab2, text="Del", command=delete_course)
        deleteBtn.grid(row=i + 1, column=4, sticky="w", pady=(5, 2))

        i += 1
    osp_label = Label(tab2, text="Osp yht:", font=("Helvetica", 10, "bold"))
    osp_label.grid(row=i + 1, column=0, sticky="ew", pady=2)

    osp_data = Label(tab2, text=osp, font=("Helvetica", 10, "bold"))
    osp_data.grid(row=i + 1, column=1, sticky="ew", pady=2)

    arvosana_label = Label(tab2, text="Keskiarvo:", font=("Helvetica", 10, "bold"))
    arvosana_label.grid(row=i + 1, column=2, sticky="ew", pady=2)

    if arvosana == 0:
        arvosana = "-"
    arvosana_data = Label(tab2, text=(arvosana), font=("Helvetica", 10, "bold"))
    arvosana_data.grid(row=i + 1, column=3, sticky="ew", pady=2)


def updateSort():
    # before rendering delete every row except the first one
    for child in tab2.grid_slaves():
        if int(child.grid_info()["row"]) >= 1:
            child.grid_remove()

    temp = []
    data = fetch_saved_data()
    if clicked2.get() == "all":
        render_results(fetch_saved_data())
    else:
        for course in data:
            if course[3] == clicked2.get():
                temp.append(course)
            else:
                continue
        render_results(temp)


# initiate the app
app = Tk()
app.title("Study log")
app.geometry("500x500")

tab_view = ttk.Notebook(app)
tab_view.pack()

tab1 = Frame(tab_view, width=500, height=500)
tab1_2 = Canvas(tab_view, width=500, height=500, scrollregion=(0, 0, 500, 450))

ctk_textbox_scrollbar = customtkinter.CTkScrollbar(tab_view, command=tab1_2.yview)
ctk_textbox_scrollbar.pack(fill="y", side=RIGHT)

tab1.pack(fill="both", expand=1)
tab1_2.pack(fill="both", expand=1)

# Scrollbar
# vbar = Scrollbar(tab_view, orient=VERTICAL, command=tab1_2.yview)
# vbar.pack(side=RIGHT, fill=Y)
# vbar.grid(row=0, column=1, sticky="ns")
# tab1_2.config(yscrollcommand=vbar.set)


tab2 = Frame(tab1_2, width=500, height=1500)
tab2.grid_columnconfigure((0, 1, 2, 3), weight=1)
tab1_2.create_window((500, 500), window=tab2, anchor="nw")
tab1_2.config(scrollregion=tab1_2.bbox("all"))
tab1_2.config(yscrollcommand=ctk_textbox_scrollbar.set)

# ctk_textbox_scrollbar = customtkinter.CTkScrollbar(tab1_2, command=tab1_2.yview)
# ctk_textbox_scrollbar.pack(side=RIGHT)

# connect textbox scroll event to CTk scrollbar

tab_view.add(tab1, text="Add course")
tab_view.add(tab1_2, text="View courses")
tab_view.pack(expand=True, fill="both")

# sort by
options2 = ["all", "väkivaltatutkimus", "hylje-biologia", "juuston alkeet", "pönkö"]
clicked2 = StringVar()
clicked2.set("all")

lajittelu_label = Label(tab2, text="Sort by:")
lajittelu_label.grid(row=0, column=0, sticky="ew", pady=(5, 2))
lajittelu_input = OptionMenu(tab2, clicked2, *options2)
lajittelu_input.grid(row=0, column=1, sticky="w", pady=(5, 2), columnspan=2)

btn2 = Button(tab2, text="Päivitä", command=updateSort)
btn2.grid(row=0, column=3, sticky="w", pady=(5, 2))

# Try this to identify selected tab (and make scrollbar appear only in selected tab)
# print(tab_view.tab(tab_view.select(), "text"))


# Add courses tab
tab1.grid_columnconfigure((0, 1, 2), weight=1)
# tab2.grid_columnconfigure((0, 1, 2), weight=1)
# tab1.grid_rowconfigure(0, weight=1)

options = ["väkivaltatutkimus", "hylje-biologia", "juuston alkeet", "pönkö"]
clicked = StringVar()
clicked.set("väkivaltatutkimus")

# btn1 = Button(tab2, text="Kokeiles", command=add_course).pack()
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

# Normaalisti btn1 ollut command=add_course
btn1 = Button(tab1, text="Lisää", command=save_data)
btn1.grid(row=4, column=1, sticky="ew")
btnTesti = Button(tab1, text="Testaa", command=fetch_saved_data)
btnTesti.grid(row=5, column=1, sticky="ew")
# btn1.place(relx=0.5, rely=0.1)

# View courses tab
tab1_2.grid_columnconfigure((0, 1), weight=1)
# fetch_saved_data()
render_results(fetch_saved_data())

# commit changes
# conn.commit()

# # Close the connection
# conn.close()
app.mainloop()
