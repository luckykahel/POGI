import tkinter as tk
import customtkinter
from customtkinter import *
from PIL import Image
from tkinter import ttk
import database
import re
import tkinter.messagebox as messagebox
from customtkinter import CTk
from datetime import datetime

db = database.DatabaseManager('database.db')

root = customtkinter.CTk()
root.title("SMIKE BIKE RENTAL")
window_height = 834
window_width = 1194

current_canvas = None
current_frame = None

def curr_time():
    current_time = datetime.now().strftime("%I:%M %p") #12 hour format
    #current_time = datetime.now().strftime("%H:%M") #24 hour format
    return current_time

def time_to_seconds():
    current_time = datetime.now().strftime("%I:%M") #12 hour format
    
    # Split the time string into hours and minutes
    hours_str, minutes_str = current_time.split(':')

    #Convert hours and minutes to integers
    hours = int(hours_str)
    minutes = int(minutes_str)

    #Calculate the total number of seconds
    total_seconds = hours * 3600 + minutes * 60

    return total_seconds

#print(time_to_seconds())

def center_screen():
    global screen_height, screen_width, x_cordinate, y_cordinate
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

center_screen()

def nameValidation():
    name = name_entry.get()

    if not name:
        messagebox.showwarning("Empty Name", "Please enter your name.")
        return False
    return True 

def phoneNumValidation():
    phoneNum = number_entry.get()
    pattern = re.compile(r'^09\d{9}$')
    
    if not bool(pattern.match(phoneNum)):
        messagebox.showwarning("Number Invalid", "Mobile Number Invalid")
        return False
    return True

def add_rental_reg():
    cell_num = int(number_entry.get())
    bikeID = int(bike_number_entry.get())
    type = 'regular'
    db.add_rental(name_entry.get(), curr_time(), cell_num, bikeID, type)

def add_rental_prem():
    cell_num = int(number_entry.get())
    bikeID = int(bike_number_entry.get())
    type = 'premium'
    db.add_rental(name_entry.get(), curr_time(), cell_num, bikeID, type)

def when_confirmed():
    global current_canvas, current_frame
    if current_canvas:
        current_canvas.destroy()
    if current_frame:
        current_frame.destroy()

def bikeAvail():
    if bike_number_entry.get() == "No Bikes Available":
        return False
    else:
        return True
    
def rent_bike():
    if not bikeAvail():
        name_entry.configure(state='disabled')
        number_entry.configure(state='disabled')
        return

    if nameValidation() and phoneNumValidation():
        add_rental_reg()
        add_rental_prem()
        when_confirmed()
        if current_canvas:
            current_canvas.destroy()

def rent_page():
    global current_canvas, current_frame, number_entry, name_entry, bike_number_entry
    when_confirmed()
    #if current_canvas:
    #    current_canvas.destroy()

    canvas1 = customtkinter.CTkCanvas(leftframe, height=834, width=730, background="#F6F4EE")
    canvas1.pack()
    rent_frame = customtkinter.CTkFrame(canvas1, fg_color="#F6F4EE", width=730, height=834)
    rent_page = customtkinter.CTkLabel(rent_frame, text='RENT REGULAR', text_color="#FFD64D", font=('Montserrat',60), fg_color='transparent')
    rent_page.grid(column=0 ,row=0, columnspan=2, pady=10, padx=10)

    bike_number = customtkinter.CTkLabel(rent_frame, text='BIKE NUMBER', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    bike_number.grid(column=0 ,row=1, pady=10, padx=10, sticky='w')

    bike_number_entry = customtkinter.CTkEntry(rent_frame, width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)
    bike_number_entry.grid(column=1, row=1, pady=10, padx=10)
    biketype = 'Regular'
    bike_number_entry.insert(0, db.generate_id(biketype))
    bike_number_entry.configure(state='disabled') 


    time_in = customtkinter.CTkLabel(rent_frame, text='TIME IN', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    time_in.grid(column=0 ,row=2, pady=10, padx=10, sticky='w')

    time_in_entry = customtkinter.CTkEntry(rent_frame, width=200, height=35, text_color="#000000",font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)
    time_in_entry.grid(column=1, row=2, pady=10, padx=10)
    #time in 
    time_in_entry.insert(0, curr_time())
    time_in_entry.configure(state='disabled') 

    name = customtkinter.CTkLabel(rent_frame, text='NAME', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    name.grid(column=0 ,row=3, pady=10, padx=10, sticky='w')

    name_entry = customtkinter.CTkEntry(rent_frame, placeholder_text='enter name', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)

    name_entry.grid(column=1, row=3, pady=10, padx=10)

    number = customtkinter.CTkLabel(rent_frame, text='NUMBER', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    number.grid(column=0 ,row=4, pady=10, padx=10, sticky='w')

    number_entry = customtkinter.CTkEntry(rent_frame, placeholder_text='enter number', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10,border_width=0)
    number_entry.grid(column=1, row=4, pady=10, padx=10)
    number_entry.insert(0, "09")
    rent_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    confirm_button = customtkinter.CTkButton(rent_frame, text='confirm', width=120, height=40, corner_radius=20, fg_color="#FFD64D", font=('Montserrat',15), text_color="#000000", hover_color="#D9AC15", command=rent_bike)
    confirm_button.grid(column=0 ,row=5, columnspan=2, pady=10, padx=10)
    current_canvas = canvas1
    current_frame = rent_frame

def rent_prem_page():
    global current_canvas, current_frame, number_entry, name_entry, bike_number_entry
    when_confirmed()
    #if current_canvas:
    #    current_canvas.destroy()

    canvas11 = customtkinter.CTkCanvas(leftframe, height=834, width=730, background="#F6F4EE")
    canvas11.pack()
    rent_prem_frame = customtkinter.CTkFrame(canvas11, fg_color="#F6F4EE", width=730, height=834)
    rent_prem_page = customtkinter.CTkLabel(rent_prem_frame, text='RENT PREMIUM', text_color="#FFD64D", font=('Montserrat',60), fg_color='transparent')
    rent_prem_page.grid(column=0 ,row=0, columnspan=2, pady=10, padx=10)

    bike_number = customtkinter.CTkLabel(rent_prem_frame, text='BIKE NUMBER', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    bike_number.grid(column=0 ,row=1, pady=10, padx=10, sticky='w')

    bike_number_entry = customtkinter.CTkEntry(rent_prem_frame, width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)
    bike_number_entry.grid(column=1, row=1, pady=10, padx=10)
    biketype = 'Premium'
    bike_number_entry.insert(0, db.generate_id(biketype))
    bike_number_entry.configure(state='disabled') 

    time_in = customtkinter.CTkLabel(rent_prem_frame, text='TIME IN', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    time_in.grid(column=0 ,row=2, pady=10, padx=10, sticky='w')
    

    time_in_entry = customtkinter.CTkEntry(rent_prem_frame, width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)
    time_in_entry.grid(column=1, row=2, pady=10, padx=10)
    #time in 
    time_in_entry.insert(0, curr_time())
    time_in_entry.configure(state='disabled') 

    name = customtkinter.CTkLabel(rent_prem_frame, text='NAME', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    name.grid(column=0 ,row=3, pady=10, padx=10, sticky='w')

    name_entry = customtkinter.CTkEntry(rent_prem_frame, placeholder_text='enter name', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)
    name_entry.grid(column=1, row=3, pady=10, padx=10)

    number = customtkinter.CTkLabel(rent_prem_frame, text='NUMBER', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    number.grid(column=0 ,row=4, pady=10, padx=10, sticky='w')

    number_entry = customtkinter.CTkEntry(rent_prem_frame, placeholder_text='enter number', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10,border_width=0)
    number_entry.grid(column=1, row=4, pady=10, padx=10)
    number_entry.insert(0, "09")
    rent_prem_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    confirm_button = customtkinter.CTkButton(rent_prem_frame, text='confirm', width=120, height=40, corner_radius=20, fg_color="#FFD64D", font=('Montserrat',15), text_color="#000000", hover_color="#D9AC15", command=rent_bike)
    confirm_button.grid(column=0 ,row=5, columnspan=2, pady=10, padx=10)

    current_canvas = canvas11
    current_frame = rent_prem_frame

def return_page():
    global current_canvas, current_frame
    when_confirmed()
    #if current_canvas:
    #    current_canvas.destroy()

    canvas2 = customtkinter.CTkCanvas(leftframe, height=834, width=730, background="#F6F4EE")
    canvas2.pack()
    return_frame = customtkinter.CTkFrame(canvas2, fg_color="#F6F4EE")
    return_page = customtkinter.CTkLabel(return_frame, text='RETURN', text_color="#FFD64D", font=('Montserrat',80), fg_color='transparent')
    return_page.grid(column=0 ,row=0, columnspan=2, pady=10, padx=10)

    return_bike_number = customtkinter.CTkLabel(return_frame, text='BIKE NUMBER', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    return_bike_number.grid(column=0 ,row=1, pady=10, padx=10, sticky='w')
    return_bike_number_entry = customtkinter.CTkEntry(return_frame, placeholder_text='enter bike number', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)
    return_bike_number_entry.grid(column=1, row=1, pady=10, padx=10)

    return_name = customtkinter.CTkLabel(return_frame, text='NAME', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    return_name.grid(column=0 ,row=2, pady=10, padx=10, sticky='w')
    return_name_entry = customtkinter.CTkEntry(return_frame, placeholder_text='enter name', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0, state=DISABLED)
    return_name_entry.grid(column=1, row=2, pady=10, padx=10)

    return_number = customtkinter.CTkLabel(return_frame, text='NUMBER', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    return_number.grid(column=0 ,row=3, pady=10, padx=10, sticky='w')
    return_number_entry = customtkinter.CTkEntry(return_frame, placeholder_text='enter name', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0, state=DISABLED)
    return_number_entry.grid(column=1, row=3, pady=10, padx=10)

    #time in //lagyan mo na kukunin yung time mula sa database
    time_in = customtkinter.CTkLabel(return_frame, text='TIME IN', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    time_in.grid(column=0 ,row=4, pady=10, padx=10, sticky='w')
    return_time_in_entry = customtkinter.CTkEntry(return_frame, width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)
    return_time_in_entry.grid(column=1, row=4, pady=10, padx=10)

    time_out = customtkinter.CTkLabel(return_frame, text='TIME OUT', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    time_out.grid(column=0 ,row=5, pady=10, padx=10, sticky='w')
    return_time_out_entry = customtkinter.CTkEntry(return_frame, width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)
    return_time_out_entry.grid(column=1, row=5, pady=10, padx=10)
    #time out
    return_time_out_entry.insert(0, curr_time())
    return_time_out_entry.configure(state='disabled')

    total_price = customtkinter.CTkLabel(return_frame, text='TOTAL PRICE', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    total_price.grid(column=0 ,row=6, pady=10, padx=10, sticky='w')
    total_price_entry = customtkinter.CTkEntry(return_frame, placeholder_text='enter name', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0, state=DISABLED)
    total_price_entry.grid(column=1, row=6, pady=10, padx=10)

    payment_method = customtkinter.CTkLabel(return_frame, text='PAYMENT METHOD', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    payment_method.grid(column=0 ,row=7, pady=10, padx=10, sticky='w')
    def combobox_callback(choice):
        print('combobox dropdown clicked:', choice)
    
    combobox_var = customtkinter.StringVar(value='CASH')
    payment_method = customtkinter.CTkComboBox(return_frame, values=['CASH', 'ALIPAY', 'CARD'],
                                         width=200, height=28,
                                         command=combobox_callback, variable=combobox_var,text_color="#000000", font=('Montserrat',20), dropdown_font=('Montserrat',20),corner_radius=10, border_width=0,dropdown_fg_color="#FFD64D", dropdown_hover_color="#D9AC15", button_color="#D9AC15", button_hover_color="#FFD64D",fg_color="#FFD64D", state='readonly')
    combobox_var.set('CASH')
    payment_method.grid(column=1, row=7)

    return_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    confirm_button2 = customtkinter.CTkButton(return_frame, text='confirm', width=120, height=40, corner_radius=20, fg_color="#FFD64D", font=('Montserrat',15), text_color="#000000", hover_color="#D9AC15", command=when_confirmed)
    confirm_button2.grid(column=0 ,row=8, columnspan=2, pady=10, padx=10)

    current_canvas = canvas2
    current_frame = return_frame

def update_page():
    global current_canvas, current_frame, add_entry 
    when_confirmed()
    #if current_canvas:
    #     current_canvas.destroy()

    canvas3 = customtkinter.CTkCanvas(leftframe, height=834, width=730, background="#F6F4EE")
    canvas3.pack()
    update_frame = customtkinter.CTkFrame(canvas3, fg_color="#F6F4EE")
    update_page = customtkinter.CTkLabel(update_frame, text='UPDATE', text_color="#FFD64D", font=('Montserrat',60), fg_color='transparent')
    update_page.grid(column=0 ,row=0, columnspan=2, pady=10, padx=10)

    def radiobutton_event():
        numofbikes = int(add_entry.get())
        radio_value = radio_var.get()
        if radio_value.lower() == 'regular' and numofbikes != 0:
                count = 0
                while True:
                    if count != numofbikes:
                        db.add_bike(radio_value)
                        count += 1
                    if count == numofbikes:
                        break

        elif radio_value.lower() == 'premium' and numofbikes != 0:
                count = 0
                while True:
                    if count != numofbikes:
                        db.add_bike(radio_value)
                        count += 1
                    if count == numofbikes:
                        break

    def updateRate():
        print(price_entry.get())
        db.update_rate(radio_var.get(),price_entry.get())
           
    add = customtkinter.CTkLabel(update_frame, text='ADD BIKE', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    add.grid(column=0 ,row=2, pady=10, padx=10, sticky='w')
    add_entry = customtkinter.CTkEntry(update_frame, placeholder_text='no. of bikes to add', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10, border_width=0)
    add_entry.grid(column=1, row=2, pady=10, padx=10)
    add_entry.insert(0,0)

    radio_var = customtkinter.StringVar(value='regular')
    radiobutton_regular= customtkinter.CTkRadioButton(update_frame, text='REGULAR',
                                                 width=100 , height=22 , radiobutton_width=22, radiobutton_height=22,
                                                 variable= radio_var, value='regular', font=('Montserrat',20), text_color="#000000", border_width_checked=6, border_width_unchecked=4, border_color="#FFD64D", fg_color="#D9AC15", command=lambda:[price_entry.delete(0,END),price_entry.insert(0, db.generate_rate(radio_var.get()))])
    radiobutton_prem= customtkinter.CTkRadioButton(update_frame, text='PREMIUM',
                                                 width=100 , height=22 , radiobutton_width=22, radiobutton_height=22,
                                                 variable= radio_var, value='premium', font=('Montserrat',20), text_color="#000000", border_width_checked=6, border_width_unchecked=4, border_color="#FFD64D", fg_color="#D9AC15", command=lambda:[price_entry.delete(0,END),price_entry.insert(0, db.generate_rate(radio_var.get()))])

    radiobutton_regular.grid(column=0, row=1, pady=10, padx=10)
    radiobutton_prem.grid(column=1, row=1, pady=10, padx=10)

    remove = customtkinter.CTkLabel(update_frame, text='REMOVE', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    remove.grid(column=0 ,row=4, pady=10, padx=10, sticky='w')
    remove_entry = customtkinter.CTkEntry(update_frame, placeholder_text='enter bike ID to remove', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10,border_width=0)
    remove_entry.grid(column=1, row=4, pady=10, padx=10)

    price = customtkinter.CTkLabel(update_frame, text='NEW RATE', text_color="#000000", font=('Montserrat',25), fg_color='transparent')
    price.grid(column=0 ,row=3, pady=10, padx=10, sticky='w')
    price_entry = customtkinter.CTkEntry(update_frame, placeholder_text='enter new rate', width=200, height=35,text_color="#000000", font=('Montserrat',15), fg_color=("#FFD64D"), corner_radius=10,border_width=0)
    price_entry.grid(column=1, row=3, pady=10, padx=10)
    price_entry.insert(0, db.generate_rate(radio_var.get()))

    update_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    confirm_button3 = customtkinter.CTkButton(update_frame, text='confirm', width=120, height=40, corner_radius=20, fg_color="#FFD64D", font=('Montserrat',15), text_color="#000000", hover_color="#D9AC15", command=lambda: [radiobutton_event(), updateRate(),when_confirmed()])
    confirm_button3.grid(column=0 ,row=5, columnspan=2, pady=10, padx=10)
    current_canvas = canvas3
    current_frame = update_frame

def transactions_page():
    global current_canvas, current_frame
    if current_canvas:
        current_canvas.destroy()

    canvas4 = customtkinter.CTkCanvas(leftframe, height=834, width=730, background="#F6F4EE")
    canvas4.pack()
    transactions_frame = customtkinter.CTkFrame(canvas4, fg_color="#F6F4EE")
    transactions_page = customtkinter.CTkLabel(transactions_frame, text='TRANSACTION\nHISTORY', text_color="#FFD64D", font=('Montserrat',55), fg_color='transparent')
    transactions_page.grid(column=0, row=0, pady=10, padx=10)
    
    columns = ('BIKE NUM', 'CUSTOMER NAME', 'TIME IN', 'TIME OUT', 'CUSTOMER NUMBER', 'BIKE TYPE', 'RATE', 'TOTAL PAID')
    treeview = ttk.Treeview(transactions_frame, height=20, columns=columns, show='headings')
    treeview.grid(column=0, row=1, padx=10)

    treeview.heading('BIKE NUM', text='BIKE NUM')
    treeview.heading('CUSTOMER NAME', text='CUSTOMER NAME')
    treeview.heading('TIME IN', text='TIME IN')
    treeview.heading('TIME OUT', text='TIME OUT')
    treeview.heading('CUSTOMER NUMBER', text='CUSTOMER NUMBER')
    treeview.heading('BIKE TYPE', text='BIKE TYPE')
    treeview.heading('RATE', text='RATE')
    treeview.heading('TOTAL PAID', text='TOTAL PAID')
    #width per column
    treeview.column('BIKE NUM', width=70, minwidth=70)
    treeview.column('CUSTOMER NAME', width=130, minwidth=130)
    treeview.column('TIME IN', width=60, minwidth=60)
    treeview.column('TIME OUT', width=60, minwidth=60)
    treeview.column('CUSTOMER NUMBER', width=120, minwidth=120)
    treeview.column('BIKE TYPE', width=80, minwidth=80)
    treeview.column('RATE', width=60, minwidth=60)
    treeview.column('TOTAL PAID', width=80, minwidth=80)

    #sample ONLY
    #contacts = []
    #for n in range(1, 51):
    #    contacts.append((f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}'))

    #for n in data:
    #    contacts.append((f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}', f'{n}'))

    #data to tree
    #for contact in contacts:
    #    treeview.insert('', customtkinter.END, values=contact)

    #    transactions_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    cursor= db.cursor
    cursor.execute("SELECT rental.bike_id, rental.name, rental.clock_start, rental.clock_end, rental.cell_num, bikes.bikeType, rental.rate, rental.total_price FROM rental INNER JOIN bikes ON rental.bike_id = bikes.bike_id;")
    data = cursor.fetchall()

    for row in data:
        treeview.insert('', 'end', values=row)

        transactions_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    #
    current_canvas = canvas4
    current_frame = transactions_frame

def indicate(page):
    page()

menu = customtkinter.CTkFrame(root, fg_color="#3C9C0B", bg_color="#3C9C0B")

insideframe = customtkinter.CTkFrame(menu, fg_color='transparent')
insideframe.place(relx = 0.5, rely = 0.5, anchor = CENTER)

brand = customtkinter.CTkLabel(insideframe, text='SMIKE', text_color="#FFD64D", font=('Montserrat',80), fg_color='transparent')
brand.pack()

brand_sub = customtkinter.CTkLabel(insideframe, text='BIKE RENTAL', text_color="#FFD64D", font=('Montserrat',25), fg_color='transparent')
brand_sub.pack(pady=10)

rent_button = customtkinter.CTkButton(insideframe, text='RENT REGULAR', width=230, height=50, corner_radius=20, fg_color="#FFD64D", hover_color="#D9AC15", text_color="#000000", font=('Montserrat',20), command=lambda:indicate(rent_page))
rent_button.pack(pady=15)

rent_prem_button = customtkinter.CTkButton(insideframe, text='RENT PREMIUM', width=230, height=50, corner_radius=20, fg_color="#FFD64D", hover_color="#D9AC15", text_color="#000000", font=('Montserrat',20), command=lambda:indicate(rent_prem_page))
rent_prem_button.pack(pady=15)

return_button = customtkinter.CTkButton(insideframe, text='RETURN', width=230, height=50, corner_radius=20, fg_color="#FFD64D", hover_color="#D9AC15", text_color="#000000", font=('Montserrat',20), command=lambda:indicate(return_page))
return_button.pack(pady=10)

update_button = customtkinter.CTkButton(insideframe, text='UPDATE', width=230, height=50, corner_radius=20, fg_color="#FFD64D", hover_color="#D9AC15", text_color="#000000", font=('Montserrat',20), command=lambda: indicate(update_page))
update_button.pack(pady=10)

transactions_button = customtkinter.CTkButton(insideframe, text='TRANSACTION HISTORY', width=180, height=50, corner_radius=20, fg_color="#FFD64D", hover_color="#D9AC15", text_color="#000000", font=('Montserrat',15), command=lambda: indicate(transactions_page))
transactions_button.pack(pady=10)

menu.pack(side=RIGHT)
menu.pack_propagate(False)
menu.configure(width=464, height=834)

leftframe = customtkinter.CTkFrame(root)
leftframe.pack(side=LEFT)
leftframe.pack_propagate(False)
leftframe.configure(width=730, height=834)
bike = CTkImage(dark_image=Image.open("Frame 2.png"), light_image=Image.open("Frame 2.png"), size=(730,834))
left = customtkinter.CTkLabel(leftframe, text='', image=bike)
left.grid(row=0, column=0)

root.resizable(0, 0)
root.mainloop()