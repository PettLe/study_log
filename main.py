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

# If need to clear widgets from overall:
# for child in tab2.grid_slaves():
#     if int(child.grid_info()["row"]) >= 1:
#         child.grid_remove()


# Custom system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


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


# kurssi_input.get(), osp_input.get(), arvosana_input.get(), clicked.get()
def save_data():
    # Insert into table
    c.execute(
        "INSERT INTO courses VALUES (:course_name, :osp, :grade, :category)",
        {
            "course_name": kurssi_input.get(),
            "osp": osp_input.get(),
            "grade": arvosana_input.get(),
            "category": kategoria_input.get(),
        },
    )

    conn.commit()
    kurssi_input.delete(0, END)
    osp_input.delete(0, END)
    arvosana_input.delete(0, END)
    render_results(fetch_saved_data())
    # conn.close()


def fetch_saved_data():
    c.execute("SELECT *, oid FROM courses")
    data = c.fetchall()
    # print(data)
    conn.commit()
    return data


def delete_course(item):
    # SQL command to delete based on oid. Then update
    c.execute(f"DELETE FROM courses WHERE oid = {item[0][4]}")
    conn.commit()
    updateSort()


# Render the contents of overall tab
def render_results(courses):
    c.execute("SELECT SUM(osp) FROM courses")
    data = c.fetchall()
    arvosana = 0
    arvosanat_lasketut = 0
    osp = data[0][0]

    for course in courses:
        try:
            arvosana += int(course[2])
            arvosanat_lasketut += 1
        except:
            continue
    if arvosana == 0:
        arvosana = str("-----")
    else:
        arvosana = arvosana / arvosanat_lasketut
        arvosana = round(arvosana, 1)

    columns = ("course_name", "osp", "grade", "category")

    tree = ttk.Treeview(tab2, columns=columns, show="headings")
    tree.column("course_name", width=150, anchor=W)
    tree.column("osp", width=100, anchor=W)
    tree.column("grade", width=100, anchor=CENTER)
    tree.column("category", width=150, anchor=CENTER)

    # define headings
    tree.heading("course_name", text="Kurssin nimi")
    tree.heading("osp", text="Op.")
    tree.heading("grade", text="Arvosana")
    tree.heading("category", text="Kategoria")

    # add data to the treeview
    for course in courses:
        temp = (
            course[0],
            course[1],
            course[2].capitalize(),
            course[3].capitalize(),
            course[4],
        )
        tree.insert("", END, values=temp)

    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item["values"]
            c.execute(f"SELECT *, oid FROM courses WHERE oid = {record[4]}")
            tieto = c.fetchall()
            # Notes section
            testiInfo = customtkinter.CTkTextbox(controlFrame, height=100)
            testiInfo.grid(row=3, column=0, sticky="ew", pady=(5, 2))
            testiInfo.insert("0.0", tieto[0][0])

            updateBtn = customtkinter.CTkButton(
                controlFrame,
                text="Päivitä",
                command=lambda id=tieto: print(id),
            )
            updateBtn.grid(row=4, column=0, sticky="ew", pady=(5, 2))

        deleteBtn = customtkinter.CTkButton(
            controlFrame,
            text="Poista",
            command=lambda id=tieto: delete_course(id),
        )
        deleteBtn.grid(row=0, column=0, sticky="ew", pady=(5, 2))

    tree.bind("<<TreeviewSelect>>", item_selected)

    tree.grid(row=0, column=0, sticky="nsew")

    # add a scrollbar
    scrollbar = ttk.Scrollbar(tab2, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # EMPTY delete button to hide mistakes, oops
    deleteBtn = customtkinter.CTkButton(controlFrame, text="Poista")
    deleteBtn.grid(row=0, column=0, sticky="ew", pady=(5, 2))

    arvosana_label = customtkinter.CTkLabel(
        controlFrame, text=f"Keskiarvo: {str(arvosana)}", font=("Helvetica", 10, "bold")
    )
    arvosana_label.grid(row=1, column=0, sticky="w", pady=2)

    osp_label = customtkinter.CTkLabel(
        controlFrame, text=f"Op (yht.): {osp}", font=("Helvetica", 10, "bold")
    )
    osp_label.grid(row=1, column=1, sticky="w", pady=2)


def updateSort():
    temp = []
    data = fetch_saved_data()
    if lajittelu_input.get() == "kaikki":
        render_results(fetch_saved_data())
    else:
        for course in data:
            if course[3] == lajittelu_input.get():
                temp.append(course)
            else:
                continue
        render_results(temp)


# initiate the app
app = customtkinter.CTk()
app.title("Kaisan opiskelu log!")

width = 500
height = 500
screen_width = app.winfo_screenwidth()  # Width of the screen
screen_height = app.winfo_screenheight()  # Height of the screen
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)

app.geometry("%dx%d+%d+%d" % (width, height, x, y))

tab_view = customtkinter.CTkTabview(app)
tab_view.pack()

tab1 = tab_view.add("Lisää kurssi")
tab2 = tab_view.add("Näytä kaikki")
tab_view.pack(expand=True, fill="both")

button_1 = customtkinter.CTkButton(tab_view.tab("Lisää kurssi"))
button_2 = customtkinter.CTkButton(tab_view.tab("Näytä kaikki"))

# Add courses tab
# tab1 = customtkinter.CTkFrame(tab_view, width=500, height=500)
# tab1.pack(fill="both", expand=1)
tab1.grid_columnconfigure((0, 1, 2), weight=1)

# View courses tab
# tab2 = customtkinter.CTkFrame(tab_view, width=500, height=500)
# tab2.pack(fill="both", expand=1)
tab2.grid_columnconfigure((0, 1), weight=1)


# Frame for courses tabs' control widgets
controlFrame = customtkinter.CTkFrame(tab2)
controlFrame.grid(row=1, column=0, columnspan=2, sticky="ew")
controlFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)


# Sorting
options2 = [
    "kaikki",
    "väkivaltatutkimus",
    "sukupuolentutkimus",
    "digimarkkinointi",
    "vastuullisuus ja kestävä kehitys työelämässä",
    "tilastotiede",
    "tekoäly",
    "muu",
    "hylje-biologia",
    "juuston alkeet",
    "pönkö",
]
clicked2 = customtkinter.StringVar(value="kaikki")

# Find the size of the longest word in optionMenu and use it as width to stop widget from resizing
menu_width = len(max(options2, key=len))


def optionmenu_callback(choice):
    updateSort()
    # print("optionmenu dropdown clicked:", choice)


lajittelu_input = customtkinter.CTkOptionMenu(
    controlFrame, values=options2, command=optionmenu_callback
)
lajittelu_input.configure(width=menu_width)
lajittelu_input.grid(row=0, column=2, sticky="ew", pady=(5, 2), columnspan=2)

options = [
    "väkivaltatutkimus",
    "sukupuolentutkimus",
    "digimarkkinointi",
    "vastuullisuus ja kestävä kehitys työelämässä",
    "tilastotiede",
    "tekoäly",
    "muu",
    "hylje-biologia",
    "juuston alkeet",
    "pönkö",
]
clicked = customtkinter.StringVar(value="väkivaltatutkimus")
clicked.set("väkivaltatutkimus")

# Widgets for add form
kurssi_label = customtkinter.CTkLabel(tab1, text="Kurssin nimi")
kurssi_label.grid(row=0, column=0, sticky="ew", pady=5)
osp_label = customtkinter.CTkLabel(tab1, text="Opintopisteet")
osp_label.grid(row=1, column=0, sticky="ew", pady=5)
arvosana_label = customtkinter.CTkLabel(tab1, text="Arvosana")
arvosana_label.grid(row=2, column=0, sticky="ew", pady=5)
muistiinpanot_label = customtkinter.CTkLabel(tab1, text="Muistiinpanot")
muistiinpanot_label.grid(row=3, column=0, sticky="ew", pady=5)
kategoria_label = customtkinter.CTkLabel(tab1, text="Kategoria")
kategoria_label.grid(row=4, column=0, sticky="ew", pady=5)
kurssi_input = customtkinter.CTkEntry(tab1)
kurssi_input.grid(row=0, column=1, sticky="ew", pady=5, columnspan=2)
osp_input = customtkinter.CTkEntry(tab1)
osp_input.grid(row=1, column=1, sticky="ew", pady=5, columnspan=2)
arvosana_input = customtkinter.CTkEntry(tab1)
arvosana_input.grid(row=2, column=1, sticky="ew", pady=5, columnspan=2)


def optionmenu_callback(choice):
    return
    # print("optionmenu dropdown clicked:", choice)


kategoria_input = customtkinter.CTkOptionMenu(
    tab1, values=options, command=optionmenu_callback
)
muistiinpanot_input = customtkinter.CTkTextbox(tab1, height=100)
muistiinpanot_input.grid(row=3, column=1, sticky="ew", pady=5, columnspan=2)
kategoria_input.grid(row=4, column=1, sticky="w", pady=5, columnspan=2)

# Save Button
btn1 = customtkinter.CTkButton(tab1, text="Lisää", command=save_data)
btn1.grid(row=5, column=1, sticky="ew")

render_results(fetch_saved_data())

app.mainloop()
