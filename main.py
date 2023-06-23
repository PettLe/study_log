from tkinter import *
from tkinter import ttk
import customtkinter


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


# Render the contents of overall tab
def render_results(kurssit):
    i = 1
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
    render_results(kurssit)
    # tab2.config(tab1_2, height=tab1_2.height)


def updateSort():
    # before rendering delete every row except the first one
    for child in tab2.grid_slaves():
        if int(child.grid_info()["row"]) >= 1:
            # print(child.grid_info()["row"])
            child.grid_remove()

    temp = []
    if clicked2.get() == "all":
        render_results(kurssit)
    else:
        for kurssi in kurssit:
            if kurssi.kategoria == clicked2.get():
                temp.append(kurssi)
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
tab2.grid_columnconfigure((0, 1, 2), weight=1)
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
lajittelu_input.grid(row=0, column=1, sticky="w", pady=(5, 2))

btn2 = Button(tab2, text="Päivitä", command=updateSort)
btn2.grid(row=0, column=2, sticky="w", pady=(5, 2))

# Try this to identify selected tab (and make scrollbar appea only in selected tab)
# print(tab_view.tab(tab_view.select(), "text"))


# Add courses tab
tab1.grid_columnconfigure((0, 1, 2), weight=1)
# tab2.grid_columnconfigure((0, 1, 2), weight=1)
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
tab1_2.grid_columnconfigure((0, 1), weight=1)

app.mainloop()
