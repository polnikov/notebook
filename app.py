import tkinter as t
from datetime import datetime, timedelta
from tkinter.messagebox import showinfo

from tkcalendar import Calendar


def grad_date():
    ent_date_bd_get.insert(0, cal.get_date())


def update_all_listbox():
    """Обновить список контактов"""
    list_all.delete(0, t.END)
    try:
        with open("contacts.txt", "r", encoding='utf-8') as file:
            for line in file.readlines():
                list_all.insert(t.END, line)
    except Exception as ex:
        showinfo('Ошибка', ex)


def delete_contact():
    """Удалить контакт"""
    selected_index = list_all.curselection()
    if not selected_index:
        showinfo('Внимание', 'Контакт для удаления не выбран')
    else:
        contact_for_del = list_all.get(selected_index[0])
        try:
            with open("contacts.txt", "r", encoding='utf-8') as file:
                contacts = file.readlines()
            with open("contacts.txt", "w", encoding='utf-8') as file:
                for contact in contacts:
                    if contact_for_del not in contact:
                        file.write(contact)
            list_all.delete(selected_index[0])
            update_all_listbox()
            update_remind_listbox()
        except Exception as ex:
            showinfo('Ошибка', ex)


def clear():
    """Очистить поля формы добавления контакта"""
    ent_last_name.delete(0, t.END)
    ent_first_name.delete(0, t.END)
    ent_tel_number.delete(0, t.END)
    ent_date_bd_get.delete(0, t.END)


def add_contact():
    """Добавить контакт"""
    temp = []
    if ent_last_name.get() != '':
        temp.append(ent_last_name.get())
    else:
        temp.append('-')

    if ent_first_name.get() != '':
        temp.append(ent_first_name.get())
    else:
        temp.append('-')

    if ent_tel_number.get() != '':
        temp.append(ent_tel_number.get())
    else:
        temp.append('-')

    if ent_date_bd_get.get() != '':
        temp.append(ent_date_bd_get.get())
    else:
        temp.append('-')

    try:
        with open("contacts.txt", "a", encoding='utf-8') as file:
            file.write(' '.join(temp) + '\n')
        showinfo('Внимание', 'Контакт добавлен')
    except Exception as ex:
        showinfo('Ошибка', ex)
    list_all.insert(t.END, ' '.join(temp) + '\n')
    ent_date_bd_get.delete(0, t.END)


# Окно с заголовком "Контакты"
window = t.Tk()
window.title("Контакты")

# Рамка для списка контактов
frm_list_all_contacts = t.LabelFrame(
    text="Список всех контактов",
    master=window,
    relief=t.FLAT,
    borderwidth=5,
)
frm_list_all_contacts.pack(
    fill=t.Y,
    side=t.LEFT,
    pady=5,
)

# Список контактов
scrollbar = t.Scrollbar(
    frm_list_all_contacts,
    orient="vertical",
)
scrollbar.pack(
    fill=t.Y,
    side=t.RIGHT,
)
list_all = t.Listbox(
    frm_list_all_contacts,
    yscrollcommand=scrollbar.set,
    width=35,
    selectmode=0,
)

scrollbar.config(command=list_all.yview)

# Отображение списка контактов
try:
    with open("contacts.txt", "r", encoding='utf-8') as file:
        for line in file.readlines():
            list_all.insert(t.END, line)
except Exception as ex:
    showinfo('Внимание', ex)

list_all.pack(
    side=t.TOP,
    fill=t.Y,
)

# Кнопка "Удалить"
btn_del_contact = t.Button(
    master=frm_list_all_contacts,
    text="Удалить",
    background="tomato",
    width=10,
    command=delete_contact,
)
btn_del_contact.pack(
    side=t.TOP,
    pady=10,
)

# Рамка для списка напоминаний
frm_list = t.Frame(
    master=frm_list_all_contacts,
    relief=t.FLAT,
    borderwidth=5,
)
frm_list.pack(
    fill=t.Y,
    side=t.TOP,
)

lbl_list = t.Label(
    master=frm_list,
    text="Ближайшие дни рождения"  # 7 дней
)
lbl_list.grid(
    row=2,
    column=0,
    sticky="w",
)

# Список напоминания
list_remind = t.Listbox(
    master=frm_list,
    width=35,
    selectmode=0,
)
list_remind.grid(
    row=3,
    column=0,
    sticky="w",
)

# Отоборажение списка напоминания


def update_remind_listbox():
    """Обновить список напоминания"""
    soon_bd = []
    today = datetime.today()
    end_period = datetime.today() + timedelta(days=7)

    try:
        with open("contacts.txt", "r", encoding='utf-8') as file:
            for line in file.readlines():

                bd_date = datetime.strptime(line.split()[3], '%d.%m.%Y')

                if today.year == end_period.year:
                    new_bd_date = datetime(
                        today.year, bd_date.month, bd_date.day)
                    if today <= new_bd_date <= end_period:
                        soon_bd.append(
                            f"{' '.join(line.split()[0:2])}: осталось {(new_bd_date - today).days + 1} дней")
                else:
                    new_bd_date = datetime(
                        end_period.year, bd_date.month, bd_date.day)
                    if today <= new_bd_date <= end_period:
                        soon_bd.append(
                            f"{' '.join(line.split()[0:2])}: осталось {(new_bd_date - today).days + 1} дней")
        list_remind.delete(0, t.END)
        for contact in soon_bd:
            list_remind.insert(t.END, contact)
    except Exception as ex:
        showinfo('Ошибка', ex)


update_remind_listbox()

# Рамка для формы добавления контакта
frm_form = t.Frame(
    relief=t.FLAT,
    borderwidth=2,
)

frm_form.pack(
    fill=t.Y,
    side=t.LEFT,
    padx=5,
)

lbl_last_name = t.Label(
    master=frm_form,
    text="Фамилия",
)
ent_last_name = t.Entry(
    master=frm_form,
    width=31,
)

lbl_last_name.grid(
    row=0,
    column=0,
    sticky="w",
)
ent_last_name.grid(
    row=1,
    column=0,
)

lbl_first_name = t.Label(
    master=frm_form,
    text="Имя"
)
ent_first_name = t.Entry(
    master=frm_form,
    width=31,
)

lbl_first_name.grid(
    row=2,
    column=0,
    sticky="w",
)
ent_first_name.grid(
    row=3,
    column=0,
)

lbl_tel_number = t.Label(
    master=frm_form,
    text="Номер телефона",
)
ent_tel_number = t.Entry(
    master=frm_form,
    width=31,
)

lbl_tel_number.grid(
    row=4,
    column=0,
    sticky="w",
)
ent_tel_number.grid(
    row=5,
    column=0,
)

lbl_date_bd = t.Label(
    master=frm_form,
    text="Дата рождения"
)
ent_date_bd_get = t.Entry(
    master=frm_form,
    width=15,
)

lbl_date_bd.grid(
    row=6,
    column=0,
    sticky="w",
)
ent_date_bd_get.grid(
    row=7,
    column=0,
    sticky="w",
)

# Календарь
cal = Calendar(
    frm_form,
    selectmode='day',
    year=2020,
    month=5,
    day=22
)
cal.grid(
    row=8,
    column=0,
    pady=10,
)

# Кнопка "Выбрать дату"
btn_get_date = t.Button(
    frm_form,
    text="Выбрать дату",
    background="PaleGreen1",
    command=grad_date
)
btn_get_date.grid(
    row=7,
    column=0,
    sticky="e",
)


# Кнопка "Добавить"
btn_add_contact = t.Button(
    master=frm_form,
    text="Добавить",
    background="PaleGreen1",
    width=10,
    command=add_contact,
)
btn_add_contact.grid(
    row=9,
    column=0,
    sticky="w",
    padx=10,
    pady=5,
)

# Кнопка "Очистить"
btn_clear = t.Button(
    master=frm_form,
    text="Очистить",
    background="tomato",
    width=10,
    command=clear,
)
btn_clear.grid(
    row=9,
    column=0,
    sticky="e",
    padx=10,
    pady=5,
)

# Запуск приложения.
window.mainloop()
