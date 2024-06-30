# importing required modules
import tkinter
import tkinter.ttk as ttk
import customtkinter
from PIL import ImageTk, Image
import requests
from models import User, SupplyList
import ctypes
from datetime import datetime, timedelta
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt

from tkinter import Tk, Label, Entry, Button
from tkcalendar import Calendar
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

# backend connection
url = 'http://localhost:5000/'
user = User()
supply_lst = SupplyList()
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # creating custom tkinter window
app.geometry("600x440")
app.title('Login')


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        response = requests.get(url + 'getAllSupply')
        if response.status_code == 200:
            result = response.json()
            if result['message'] == 'successful':
                temp = result['supply']
                supply_lst.insert_list(temp)


        self.title("Supply Solutions")
        # # remove title bar , page reducer and closing page !!!most have a quit button with app.destroy!!! (this app have a quit button so don't worry about that)
        # self.overrideredirect(True)

        # make the app as big as the screen (no mater which screen you use)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), (self.winfo_screenheight() - self.winfo_screenheight()%32)))
        self.state('zoomed')
        # root!
        self.main_container = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        # left side panel -> for frame selection
        self.left_side_panel = customtkinter.CTkFrame(self.main_container, width=150, corner_radius=10)
        self.left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)

        self.left_side_panel.grid_columnconfigure(0, weight=1)
        self.left_side_panel.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
        self.left_side_panel.grid_rowconfigure((5, 6), weight=1)

        # self.left_side_panel WIDGET
        self.logo_label = customtkinter.CTkLabel(self.left_side_panel, text="Welcome! \n",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.scaling_label = customtkinter.CTkLabel(self.left_side_panel, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.left_side_panel,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="s")

        self.bt_Logout = customtkinter.CTkButton(self.left_side_panel, text="Logout", fg_color='#EA0000',
                                               hover_color='#B20000',
                                               command=lambda: back_to_login_page(self))
        self.bt_Logout.grid(row=9, column=0, padx=20, pady=10)


        self.bt_Quit = customtkinter.CTkButton(self.left_side_panel, text="Quit", fg_color='#EA0000',
                                               hover_color='#B20000',
                                               command=self.close_window)
        self.bt_Quit.grid(row=10, column=0, padx=20, pady=10)

        # button to select correct frame IN self.left_side_panel WIDGET
        self.bt_homepage = customtkinter.CTkButton(self.left_side_panel, text="Homepage",
                                                   command=lambda: self.homie(user.id))
        self.bt_homepage.grid(row=1, column=0, padx=20, pady=10)

        self.bt_profile = customtkinter.CTkButton(self.left_side_panel, text="Profile", command=lambda : self.profile(user.id))
        self.bt_profile.grid(row=2, column=0, padx=20, pady=10)
        if user.type == 3:
            self.bt_categories = customtkinter.CTkButton(self.left_side_panel, text="Manager Options",
                                                         command=self.manager)
            self.bt_categories.grid(row=4, column=0, padx=20, pady=10)

        self.bt_noti = customtkinter.CTkButton(self.left_side_panel, text="Notifications",
                                                     command=lambda : self.notification(user.id))
        self.bt_noti.grid(row=3, column=0, padx=20, pady=10)

        # right side panel -> have self.right_dashboard inside it
        self.right_side_panel = customtkinter.CTkFrame(self.main_container, corner_radius=10, fg_color="#000811")
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5)

        self.right_dashboard = customtkinter.CTkFrame(self.main_container, corner_radius=10, fg_color="#ffffff")
        self.right_dashboard.pack(in_=self.right_side_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0,
                                  pady=0)
        self.id = id
        self.homie(id)

    #  self.right_dashboard   ----> dashboard widget
    def homie(self, id):
        self.bt_homepage.configure(fg_color='#b8bda8')
        self.bt_profile.configure(fg_color=['#2CC985', '#2FA572'])
        self.bt_noti.configure(fg_color=['#2CC985', '#2FA572'])
        if user.type ==3:
            self.bt_categories.configure(fg_color=['#2CC985', '#2FA572'])
        self.clear_frame()
        create_table(self, 'supply')



    #  self.right_dashboard   ----> statement widget
    def profile(self, id):
        self.bt_homepage.configure(fg_color=['#2CC985', '#2FA572'])
        self.bt_profile.configure(fg_color='#b8bda8')
        self.bt_noti.configure(fg_color=['#2CC985', '#2FA572'])
        if user.type ==3:
            self.bt_categories.configure(fg_color=['#2CC985', '#2FA572'])
        self.clear_frame()
        create_table(self, 'profile')

        self.name = customtkinter.CTkLabel(master=self.right_dashboard, text="First name: ",
                                           font=('Century Gothic', 18))
        self.name_entry = customtkinter.CTkEntry(master=self.right_dashboard, width=220)
        self.name_entry.insert(0, user.name)

        self.lastname = customtkinter.CTkLabel(master=self.right_dashboard, text="Last name: ",
                                               font=('Century Gothic', 18))
        self.lastname_entry = customtkinter.CTkEntry(master=self.right_dashboard, width=220)
        self.lastname_entry.insert(0, user.lastname)

        self.email = customtkinter.CTkLabel(master=self.right_dashboard, text="E-mail: ",
                                            font=('Century Gothic', 18))
        self.email_entry = customtkinter.CTkEntry(master=self.right_dashboard, width=220)
        self.email_entry.insert(0, user.email)

        def save_changes_func():
            data = {'email': self.email_entry.get(), 'name': self.name_entry.get(),
                    'lastname': self.lastname_entry.get()}
            response = requests.post(url + 'changeInfo', data=data)
            if response.status_code == 200:
                result = response.json()
                if result['message'] == 'change successful':
                    ctypes.windll.user32.MessageBoxW(0, "Your changes have been saved in the system.", "Saved Changes",
                                                     0)
                    user.name = data['name']
                    user.email = data['email']
                    user.lastname = data['lastname']
                else:
                    ctypes.windll.user32.MessageBoxW(0, "Your changes have NOT been saved in the system.", "ERROR", 0)

        self.save_BTN = customtkinter.CTkButton(master=self.right_dashboard, width=60, height=20, text="Save changes",
                                                command=save_changes_func,
                                                corner_radius=6)

        self.name.place(relx=0.3, rely=0.6, anchor=tkinter.CENTER)
        self.name_entry.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        self.lastname.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)
        self.lastname_entry.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        self.email.place(relx=0.3, rely=0.8, anchor=tkinter.CENTER)
        self.email_entry.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        self.save_BTN.place(relx=0.75, rely=0.8, anchor=tkinter.CENTER)


    #  self.right_dashboard   ----> categories widget
    def manager(self):
        self.bt_homepage.configure(fg_color=['#2CC985', '#2FA572'])
        self.bt_profile.configure(fg_color=['#2CC985', '#2FA572'])
        self.bt_noti.configure(fg_color=['#2CC985', '#2FA572'])
        if user.type ==3:
            self.bt_categories.configure(fg_color='#b8bda8')
        self.clear_frame()

        self.toptitle = customtkinter.CTkLabel(self.right_dashboard, text="Supply Solutions - Manager Options \n",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.toptitle.pack(pady=10)

        # The email selection combo box
        email_type = {}  # keys = emails, values = user type
        response = requests.get(url + 'getUsersTypes')
        if response.status_code == 200:
            result = response.json()
            # print(result)
            for x in result['users']:
                email_type[x[0]] = int(x[1])


        def add_definition(n):
            if n == 1:
                return '1 - Student'
            elif n == 2:
                return '2 - Staff'
            else:
                return '3 - Manager'

        def save_callback():
            email_type[combobox1.get()] = int(combobox2.get()[0])

            temp_data = {}
            temp_email = combobox1.get()
            temp_data['email'] = temp_email
            temp_type = int(combobox2.get()[0])
            temp_data['type'] = temp_type

            response = requests.post(url + 'changeType', data=temp_data)
            if response.status_code == 200:
                print(email_type, temp_data)
                result = response.json()

        def delete_callback():

            temp_data = {}
            temp_email = combobox1.get()
            temp_data['email'] = temp_email

            if CTkMessagebox(icon='warning', title="Warning", option_1="Yes", option_2="Cancel",
                             message="Are you sure you want to delete this user?", bg_color='red').get() == 'Yes':
                del email_type[combobox1.get()]
                response = requests.post(url + 'removeUser', data=temp_data)
                if response.status_code == 200:
                    print(email_type, temp_data)
                    result = response.json()

                # combobox1['values'] = list(test_dictionary.keys())
                combobox1.configure(values=list(email_type.keys()))
                if len(email_type) > 0:
                    combobox1.set(list(email_type.keys())[0])
                    update_combobox2()

        def update_combobox2(*args):
            key = combobox1.get()
            value = add_definition(email_type.get(key))
            if email_type.get(key) is not None:
                combobox2.set(str(value))

        def item_stat(self):
            # Check if there's already an active window
            if hasattr(self, "stat_window") and self.stat_window.winfo_exists():
                return

            # Create a new window for acquiring items
            window = customtkinter.CTkToplevel(self)
            window.title("Item Statistics")

            # Set the window size and disable resizing
            window.geometry("600x400")
            window.resizable(False, False)

            # Make the new window appear on top of the parent window
            window.transient(self)

            # Set focus to the new window
            window.grab_set()

            # Save a reference to the window so we can check if it's already open
            self.stat_window = window

            response = requests.get(url + 'plot_borrow')
            result = response.json()
            borrow_data = result['borrow_data']
            num_of_items = result['num_of_items']
            borrow_data = [datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z') for date_str in borrow_data]
            # Extract the hour from borrow_data
            hours = [date.hour for date in borrow_data]
            # Calculate the sum of num_of_items in each hour
            hourly_counts = {}
            for hour, count in zip(hours, num_of_items):
                hourly_counts[hour] = hourly_counts.get(hour, 0) + count
            # Sort the hourly counts by hour
            sorted_hourly_counts = sorted(hourly_counts.items())
            # Separate the hour and count values
            sorted_hours, sorted_counts = zip(*sorted_hourly_counts)

            # Create a figure and plot the graph
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            ax.bar(sorted_hours, sorted_counts)
            ax.set_xlabel('Hour of the Day')
            ax.set_ylabel('Number of Borrowed Items')
            ax.set_title('Borrowed Items by Hour')
            ax.set_xticks(range(8, 24))
            ax.set_xlim(7.5, 23.5)
            ax.grid(True)

            # Embed the figure in a tkinter canvas
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack()



        def order_stuff(self):

            def confirm_order_stuff(window,name,units,type,description):
                data = {
                    'name': name,
                    'units': int(units),
                    'type': type,
                    'description': description,
                }
                response = requests.post(url + 'addItemToSupply', data=data)
                if response.status_code == 200:
                    result = response.json()
                    if result['message'] == 'change successful':
                        item_id = result['id']
                        supply_lst.insert_item(item_id[0][0],type,name,int(units),description,0)
                        print('add item')
                    else:
                        print('err')
                else:
                    print('err2')

                window.destroy()

            def slider_event2(window):
                label_item2.configure(text=slider.get())

            def combolicious(choice):
                if choice == "New Item":
                    textbox.configure(state=tkinter.NORMAL)  # enable textbox
                    textbox2.configure(state=tkinter.NORMAL)  # enable textbox
                    textbox3.configure(state=tkinter.NORMAL)  # enable textbox
                    textbox.focus_set()  # set focus to textbox
                else:
                    textbox.delete(0, tkinter.END)
                    textbox.insert(tkinter.END, "")
                    textbox.configure(state="disabled")  # disable textbox
                    textbox2.delete(0, tkinter.END)
                    textbox2.insert(tkinter.END, "")
                    textbox2.configure(state="disabled")  # disable textbox
                    textbox3.delete(0, tkinter.END)
                    textbox3.insert(tkinter.END, "")
                    textbox3.configure(state="disabled")  # disable textbox


            # Check if there's already an active window
            if hasattr(self, "order_item_window") and self.order_item_window.winfo_exists():
                return

            # Create a new window for acquiring items
            window = customtkinter.CTkToplevel(self)
            window.title("Order Items")

            # Set the window size and disable resizing
            window.geometry("300x330")
            window.resizable(False, False)

            # Make the new window appear on top of the parent window
            window.transient(self)

            # Set focus to the new window
            window.grab_set()

            # Save a reference to the window so we can check if it's already open
            self.order_item_window = window

            # Create a label for the item selection
            label_item = customtkinter.CTkLabel(master=window, text="What item would you like to order?")
            label_item.pack()

            # Create a combo box with the available items
            items = supply_lst.get_items_names()
            items.append("New Item")
            combo_item = customtkinter.CTkComboBox(window, values=items, command=combolicious)
            combo_item.pack()
            combo_item.bind("<<ComboboxSelected>>", lambda event, window=window: combolicious(event))

            # Create a label for the return time selection
            label_units = customtkinter.CTkLabel(master=window, text="How many units?")
            label_units.pack()
            now = datetime.now()
            slider = customtkinter.CTkSlider(window, from_=1, to=200, number_of_steps=199,
                                             command=slider_event2)
            slider.set(1)
            slider.pack()

            label_item2 = customtkinter.CTkLabel(master=window, text=slider.get())
            label_item2.pack()

            textbox = customtkinter.CTkEntry(master=window, width=200, height=10, font=('Century Gothic', 12), placeholder_text="Enter item's name")
            textbox.pack(pady=10)
            textbox.configure(state='disabled')
            textbox2 = customtkinter.CTkEntry(master=window, width=100, height=10, font=('Century Gothic', 12), placeholder_text="Type")
            textbox2.pack(pady=10)
            textbox2.configure(state='disabled')
            textbox3 = customtkinter.CTkEntry(master=window, width=200, height=40, font=('Century Gothic', 12), placeholder_text="Enter item's description")
            textbox3.pack(pady=10)
            textbox3.configure(state='disabled')

            now = datetime.now()


            # Create a button to confirm the acquisition
            button_confirm = customtkinter.CTkButton(window, text="Confirm",
                                                     command=lambda: confirm_order_stuff(window, textbox.get(),slider.get(),textbox2.get(),textbox3.get()) if now.hour < 22 and now.hour > 6 else CTkMessagebox(icon='warning', title="Warning", option_1="Ok", message="You can only order items before 5pm").get())
            button_confirm.pack(pady=10)



        combobox1_var = customtkinter.StringVar(value=list(email_type.keys())[0])
        combobox1 = customtkinter.CTkComboBox(master=self.right_dashboard, values=list(email_type.keys()),
                                              variable=combobox1_var, width=200, height=40,
                                              corner_radius=5, dropdown_font=('Arial', 12), command=update_combobox2)
        combobox1.pack(pady=10)

        combobox2_var = customtkinter.StringVar(value=add_definition(list(email_type.values())[0]))
        combobox2 = customtkinter.CTkComboBox(master=self.right_dashboard,
                                              values=['1 - Student', '2 - Staff', '3 - Manager'],
                                              variable=combobox2_var, width=200, height=40, corner_radius=5,
                                              dropdown_font=('Arial', 12))
        combobox2.pack(pady=10)

        save_button = customtkinter.CTkButton(master=self.right_dashboard, text="Save", font=('Arial', 14),
                                              corner_radius=5,
                                              hover=True, command=save_callback)
        save_button.pack(pady=10)

        delete_button = customtkinter.CTkButton(master=self.right_dashboard, text="Delete User", font=('Arial', 14),
                                                corner_radius=5,
                                                hover=True, command=delete_callback)
        delete_button.pack(pady=10)

        order_button = customtkinter.CTkButton(master=self.right_dashboard, text="Order items", font=('Arial', 14),
                                                corner_radius=5,
                                                hover=True, command=lambda: order_stuff(self))
        order_button.pack(pady=10)  #
        order_button = customtkinter.CTkButton(master=self.right_dashboard, text="Item Statistics", font=('Arial', 14),
                                                corner_radius=5,
                                                hover=True, command=lambda: item_stat(self))
        order_button.pack(pady=10)  #

    def notification(self, id):
        self.bt_homepage.configure(fg_color=['#2CC985', '#2FA572'])
        self.bt_profile.configure(fg_color=['#2CC985', '#2FA572'])
        self.bt_noti.configure(fg_color='#b8bda8')
        if user.type ==3:
            self.bt_categories.configure(fg_color=['#2CC985', '#2FA572'])
        self.clear_frame()
        create_table(self, 'noti')



    # Change scaling of all widget 80% to 120%
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # close the entire window
    def close_window(self):
        App.destroy(self)

    # CLEAR ALL THE WIDGET FROM self.right_dashboard(frame) BEFORE loading the widget of the concerned page
    def clear_frame(self):
        for widget in self.right_dashboard.winfo_children():
            widget.destroy()

    def return_item(self):

        selected_item = self.table.item(self.table.selection())
        if selected_item is None:
            # No item is currently selected
            return

        name = selected_item['values'][0]
        units = selected_item['values'][1]

        id = supply_lst.get_id_by_name(name)
        now = datetime.now()
        dt = datetime(now.year, now.month, now.day, now.hour, now.minute)
        data = {
            'user_id': user.id,
            'item_id': id,
            'num_of_items': int(units),
        }

        response = requests.post(url + 'returnSomeItem', data=data)
        if response.status_code == 200:
            result = response.json()
            if result['message'] == 'change successful':
                supply_lst.return_item_by_id(id, units)
                self.profile(user.id)
            else:
                print('err')
        else:
            print('err2')

    def acquire_item(self):

        def slider_event3(window):
                label_item3.configure(text=slider2.get())
        def combolicious(choice):
            slider2.configure(number_of_steps=supply_lst.get_supply_avl_by_name(choice), to=supply_lst.get_supply_avl_by_name(choice))
            slider2.set(0)
            label_item3.configure(text="0")

        # Check if there's already an active window
        if hasattr(self, "acquire_item_window") and self.acquire_item_window.winfo_exists():
            return

        # Create a new window for acquiring items
        window = customtkinter.CTkToplevel(self)
        window.title("Acquire Item")

        height = 250
        width = 300
        spawn_x = int(self.winfo_width() * .5 + self.winfo_x() - .5 * width + 7)
        spawn_y = int(self.winfo_height() * .5 + self.winfo_y() - .5 * height + 20)
        window.geometry(f"{width}x{height}+{spawn_x}+{spawn_y}")


        # Set the window size and disable resizing
        # window.geometry("300x250")

        # Center the window so it would appear in the middle of the screen

        window.resizable(False, False)

        # Make the new window appear on top of the parent window
        window.transient(self)

        # Set focus to the new window
        window.grab_set()

        # Save a reference to the window so we can check if it's already open
        self.acquire_item_window = window

        # Create a label for the item selection
        label_item = customtkinter.CTkLabel(master=window, text="What item would you like to borrow?")
        label_item.pack()

        # Create a combo box with the available items
        items = supply_lst.get_items_names()
        combo_item = customtkinter.CTkComboBox(window, values=items, command=combolicious)
        combo_item.pack()
        combo_item.bind("<<ComboboxSelected>>", lambda event, window=window: combolicious(event))

        # Create a label for the return time selection
        label_return = customtkinter.CTkLabel(master=window, text="When will you return it?")
        label_return.pack()
        date =[ datetime.now()]
        btn_choose_date = customtkinter.CTkButton(master=window,text='choose date and time',command= lambda:self.choose_date_time(date))
        btn_choose_date.pack()
        self.label_time = customtkinter.CTkLabel(master=window, text=f"return time : {date[0].strftime('%Y-%m-%d %H:%M')}")
        self.label_time.pack()

        label_quantity = customtkinter.CTkLabel(master=window, text="How many would you like to borrow?")
        label_quantity.pack()

        slider2 = customtkinter.CTkSlider(window, from_=0, to=supply_lst.get_supply_avl_by_name(combo_item.get()),
                                          number_of_steps=supply_lst.get_supply_avl_by_name(combo_item.get()), command=slider_event3)
        slider2.set(0)
        slider2.pack()

        # slider2 = customtkinter.CTkSlider(window, from_=100, to=200, number_of_steps=100, command=slider_event3)
        # slider2.pack()

        label_item3 = customtkinter.CTkLabel(master=window, text=slider2.get())
        label_item3.pack()


        # Create a button to confirm the acquisition
        button_confirm = customtkinter.CTkButton(window, text="Confirm",
                                                 command=lambda: self.confirm_acquisition(combo_item.get(),
                                                                                          date[0],
                                                                                          slider2.get()))
        button_confirm.pack()

    def choose_date_time(self,date):
        def on_date_selected(date):
            # Get the selected date and time
            selected_date = cal.selection_get()
            selected_time = time_entry.get()

            # Combine the date and time into a single string
            selected_datetime = f"{selected_date} {selected_time}"

            # Assign the selected datetime to the 'data' variable
            temp_date = selected_datetime
            date[0] = datetime.strptime(temp_date, '%Y-%m-%d %H:%M')
            self.label_time.configure(text=f"return time : {date[0].strftime('%Y-%m-%d %H:%M')}")
            # Close the widget
            root.destroy()

        # Create the root Tkinter window
        root = Tk()
        root.title("Choose Date and Time")
        h = 300
        w = 300
        spawn_x = int(self.winfo_width() * .5 + self.winfo_x() - .5 * w + 7)
        spawn_y = int(self.winfo_height() * .5 + self.winfo_y() - .5 * h + 20)
        root.geometry(f"{w}x{h}+{spawn_x}+{spawn_y}")
        # Create the calendar widget
        cal = Calendar(root, selectmode="day")
        cal.pack()

        # Create a label and entry for the time
        time_label = Label(root, text="Time:")
        time_label.pack()

        time_entry = Entry(root)
        time_entry.insert(0, '00:00')
        time_entry.pack()

        # Create a button to confirm the selection
        confirm_button = Button(root, text="OK", command=lambda: on_date_selected(date))
        confirm_button.pack()

        # Start the Tkinter event loop
        root.mainloop()

    def confirm_acquisition(self, item, return_time, quantity):
        quantity = int(quantity)
        id = supply_lst.get_id_by_name(item)
        remain = supply_lst.borrow_item_by_id(id,quantity)
        if remain :
            data = {
                'user_id' : user.id,
                'item_id' : id,
                'return_time' : return_time,
                'num_of_items_remain' : remain,
                'num_of_items' : quantity
            }

            response = requests.post(url + 'borrowItem', data=data)
            if response.status_code == 200:
                result = response.json()
                if result['message'] == 'change successful':
                    print(supply_lst)
                else:
                    print('shpih')
            else:
                print('shpih2')

        print(f"Acquiring {quantity} of {item} for {return_time} hours")
        self.acquire_item_window.destroy()
        self.homie(user.id)

    def item_description(self):
        selected_item = self.table.item(self.table.selection())
        item_name = selected_item['values'][0]
        all_units = selected_item['values'][1]
        available_units = selected_item['values'][2]
        type = selected_item['values'][3]
        print(f"Showing description for {item_name} ({available_units}/{all_units}) with a type of {type}.")

    def fix_item(self):
        pass

    def report_item(self):
        selected_item = self.table.item(self.table.selection())
        if selected_item['values'][0] == '':
            return

        def report_stuff(self, window):
            data = {
                'user_id' : user.id,
                'id' :supply_lst.get_id_by_name(self.namez),
                'des' :self.textbox.get(),
                'units' :int(self.slider.get())
            }
            response = requests.post(url + 'reportItem',data=data)
            if response.status_code == 200 :
                result = response.json()
                if result['message'] == 'change successful':
                    supply_lst.report_item(self.namez,data['units'])
                else:
                    print('not good')
            else:
                print(f'bad response {response.status_code}')
            window.destroy()
            ctypes.windll.user32.MessageBoxW(0,
                                             f"Reporting: {self.namez}\n A report for the item has been sent to the admins.",
                                             "Help", 0)

        def slider_event2(window):
            label_item2.configure(text=self.slider.get())

        # Check if there's already an active window
        if hasattr(self, "report_item_window") and self.report_item_window.winfo_exists():
            return

        # Create a new window for acquiring items
        window = customtkinter.CTkToplevel(self)
        window.title("Report Item")

        height = 300
        width = 300
        spawn_x = int(self.winfo_width() * .5 + self.winfo_x() - .5 * width + 7)
        spawn_y = int(self.winfo_height() * .5 + self.winfo_y() - .5 * height + 20)
        window.geometry(f"{width}x{height}+{spawn_x}+{spawn_y}")


        # Set the window size and disable resizing
        # window.geometry("300x300")
        window.resizable(False, False)

        # Make the new window appear on top of the parent window
        window.transient(self)

        # Set focus to the new window
        window.grab_set()

        # Save a reference to the window so we can check if it's already open
        self.report_item_window = window

        item_name = selected_item['values'][0]
        all_units = selected_item['values'][1]

        self.namez = item_name

        # Create a label for the item selection
        label_item = customtkinter.CTkLabel(master=window, text="How many items would you like to report?")
        label_item.pack(pady=10)
        self.slider = customtkinter.CTkSlider(window, from_=1, to=all_units, number_of_steps=all_units-1,
                                         command=slider_event2)
        self.slider.set(1)
        self.slider.pack(pady=10)
        label_item2 = customtkinter.CTkLabel(master=window, text=self.slider.get())
        label_item2.pack(pady=10)

        label_item3 = customtkinter.CTkLabel(master=window, text=f"What is the problem with the {item_name}?")
        label_item3.pack(pady=10)
        self.textbox = customtkinter.CTkEntry(master=window, width=200, height=30, font=('Century Gothic', 12),
                                         placeholder_text="Enter problem here")
        self.textbox.pack(pady=10)

        # Create a button to confirm the acquisition
        button_confirm = customtkinter.CTkButton(window, text="Confirm",
                                                 command=lambda: report_stuff(self,
                                                     window) if self.textbox.get()!= '' else CTkMessagebox(
                                                     icon='warning', title="Warning", option_1="Ok", bg_color='red',
                                                     message="Please describe the problem").get())
        button_confirm.pack(pady=10)


def register_in_db(w, entry1, entry2, entry3, entry4):
    data = {
        'email': entry1.get(),
        'password': entry4.get(),
        'firstname': entry2.get(),
        'Last name': entry3.get(),
    }
    response = requests.post(url + 'register', data=data)
    if response.status_code == 200:
        result = response.json()
        if result['message'] == 'register successful':
            w.destroy()
            app = customtkinter.CTk()  # creating custom tkinter window
            app.geometry("600x440")
            app.title('Login')
            login_page(app)
        else:
            print('shpih')
    else:
        print('Failed to authenticate user')


def register_function(app):
    app.destroy()  # destroy current window and creating new one
    w = customtkinter.CTk()
    w.geometry("600x540")
    w.title('Register')
    img1 = ImageTk.PhotoImage(Image.open("pattern.png"))
    l1 = customtkinter.CTkLabel(master=w, image=img1)
    l1.pack()

    # creating custom frame
    frame = customtkinter.CTkFrame(master=l1, width=320, height=400, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="Register to our system", font=('Century Gothic', 20))
    l2.place(x=50, y=45)
    l2.pack(pady=10, padx=30)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
    entry1.place(x=50, y=100)
    entry1.pack(pady=10, padx=30)
    entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='First name')
    entry2.place(x=50, y=155)
    entry2.pack(pady=10, padx=30)
    entry3 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Last name')
    entry3.place(x=50, y=210)
    entry3.pack(pady=10, padx=30)
    entry4 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    entry4.place(x=50, y=265)
    entry4.pack(pady=10, padx=30)
    register_button = customtkinter.CTkButton(master=frame, width=120, height=40, text="Register",
                                              command=lambda: register_in_db(w, entry1, entry2, entry3, entry4),
                                              corner_radius=6)
    register_button.place(x=105, y=325)
    register_button.pack(pady=10, padx=30)

    return_button = customtkinter.CTkButton(master=frame, width=50, height=25, text="Back",
                                           command=lambda: back_to_login_page(w), corner_radius=6)
    return_button.pack(pady=10, padx=30)

    w.mainloop()


def login_function(app, entry1, entry2):
    email, passord = entry1.get(), entry2.get()

    data = {
        'email': email,
        'password': passord
    }

    response = requests.post(url + 'login', data=data)
    if response.status_code == 200:
        result = response.json()
        if result['message'] == 'Login successful':
            app.destroy()  # destroy current window and creating new one
            user.tupple_insert(result['user'])
            w = App()
            w.mainloop()
        else:
            print('shpih')
    else:
        print('Failed to authenticate user')


def login_page(app):
    if app:
        app.destroy()

    app = customtkinter.CTk()  # creating custom tkinter window
    app.geometry("600x580")
    app.title('Login')

    img1 = ImageTk.PhotoImage(Image.open("pattern.png"))
    l1 = customtkinter.CTkLabel(master=app, image=img1)
    l1.pack()

    # creating custom frame
    frame = customtkinter.CTkFrame(master=l1, width=320, height=500, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="Log into your account", font=('Century Gothic', 20))
    l2.place(x=50, y=45)
    l2.pack(pady=10)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
    entry1.place(x=50, y=110)
    entry1.pack(pady=10)

    entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    entry2.place(x=50, y=165)
    entry2.pack(pady=10)

    l3 = customtkinter.CTkButton(master=frame, text="Forget password?", font=('Century Gothic', 12),
                                 command=lambda: forget_password(app))
    l3.place(x=155, y=195)
    l3.pack(pady=10)

    # Create custom button
    login_button = customtkinter.CTkButton(master=frame, width=120, height=40, text="Login",
                                           command=lambda: login_function(app, entry1, entry2), corner_radius=6)
    login_button.place(x=30, y=235)
    login_button.pack(pady=10)

    register_button = customtkinter.CTkButton(master=frame, width=120, height=40, text="Register",
                                              command=lambda: register_function(app), corner_radius=6)
    register_button.place(x=170, y=235)
    register_button.pack(pady=10)

    img3 = customtkinter.CTkImage(Image.open("samilogo.png").resize((40, 40)))

    img3 = customtkinter.CTkButton(master=frame, image=img3, text="Sami Shamoon College of Engineering", width=40,
                                   height=40, compound="left", fg_color='white', text_color='black',
                                   hover_color='#AFAFAF')
    img3.place(x=160, y=320, anchor=tkinter.CENTER)
    img3.pack(pady=10, padx=10)

    def about_func():
        ctypes.windll.user32.MessageBoxW(0, "Made with love by:\n\nAlex, Bar, Aden and Basel", "About Us", 0)

    about_BTN = customtkinter.CTkButton(master=frame, width=60, height=20, text="About us", command=about_func,
                                        corner_radius=6)
    about_BTN.place(x=160, y=370, anchor=tkinter.CENTER)
    about_BTN.pack(pady=10)

    # You can easily integrate authentication system
    app.mainloop()


def back_to_login_page(app):
    app.destroy()
    app = customtkinter.CTk()  # creating custom tkinter window
    login_page(app)


def forget_password(app):
    if app:
        app.destroy()

    app = customtkinter.CTk()  # creating custom tkinter window
    app.geometry("600x540")
    app.title('Login')

    img1 = ImageTk.PhotoImage(Image.open("pattern.png"))
    l1 = customtkinter.CTkLabel(master=app, image=img1)
    l1.pack()

    # creating custom frame
    frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    l2 = customtkinter.CTkLabel(master=frame, text="Forget password", font=('Century Gothic', 20))
    l2.place(x=50, y=45)
    l2.pack(pady=10)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
    entry1.place(x=50, y=100)
    entry1.pack(pady=10)

    b1 = customtkinter.CTkButton(master=frame, text="send new password to this mail", font=('Century Gothic', 12),
                                 command=lambda: generate_new_password(entry1.get().lower()))
    b1.place(x=50, y =135)
    b1.pack(pady=10)


    entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='password we send to your mail', show="*")
    entry2.place(x=50, y=165)
    entry2.pack(pady=10)

    entry3 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='New password', show="*")
    entry3.place(x=50, y=195)
    entry3.pack(pady=10)


    # Create custom button
    login_button = customtkinter.CTkButton(master=frame, width=120, height=40, text="Generate new password",
                                           command=lambda: change_password(app, entry1.get().lower(),
                                                                           entry2.get().lower(),entry3.get().lower()
                                                                           ), corner_radius=6)
    login_button.place(x=30, y=235)
    login_button.pack(pady=10)

    return_button = customtkinter.CTkButton(master=frame, width=50, height=25, text="Back",
                                           command=lambda: back_to_login_page(app), corner_radius=6)
    return_button.pack(pady=10)


    img3 = customtkinter.CTkImage(Image.open("samilogo.png").resize((40, 40), Image.LANCZOS))

    img3 = customtkinter.CTkButton(master=frame, image=img3, text="Sami Shamoon College of Engineering", width=40,
                                   height=40, compound="left", fg_color='white', text_color='black',
                                   hover_color='#AFAFAF')
    img3.place(x=160, y=320, anchor=tkinter.CENTER)
    img3.pack(pady=10, padx=10)

    # You can easily integrate authentication system
    app.mainloop()


def generate_new_password(email):
    print("mail")
    response =requests.post(url + 'generateTempPassword',data = {'email':email})
    if response.status_code == 200:
        result = response.json()
        if result['message'] == 'change successful':
            print('cool')
        else:
            print('shpih')
    else:
        print('Failed to authenticate user')


def change_password(app, email, temp_password,new_password):
    data = {
        'email': email,
        'new_password': new_password,
        'temp_password' :temp_password
    }

    response = requests.post(url + 'changePassword', data=data)
    if response.status_code == 200:
        result = response.json()
        if result['message'] == 'change successful':
            login_page(app)
        else:
            print('shpih')
    else:
        print('Failed to authenticate user')


def create_table(self, type):
    # response = requests.get(url + 'getAllBorrows')
    # if response.status_code == 200:
    #     result = response.json()
    #     if result['message'] == 'successful':
    #         temp = result['borrows']
    #         print(temp)



    # Create a simple table
    style = ttk.Style()
    style.configure("Treeview", font=("TkDefaultFont", 18))  # Adjust the size as per your requirement
    style.configure("Treeview.Heading",
                    font=("TkDefaultFont", 18, "bold"))  # Adjust the size as per your requirement for column headings
    style.configure("Custom.Treeview", rowheight=40)  # Adjust the row height as per your requirement

    self.table = ttk.Treeview(self.right_dashboard, style="Custom.Treeview")
    if type == 'supply':

        self.toptitle = customtkinter.CTkLabel(self.right_dashboard, text="Supply Solutions - Homepage \n",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.toptitle.pack(pady=10)

        self.table.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        # Define the columns of the table
        self.table["columns"] = ("Item name", "Quantity", "Available", "Type")

        # Set the headings of the columns
        self.table.column("Item name", width=150, anchor="center", stretch=True)
        self.table.heading("Item name", text="Item name")

        self.table.column("Quantity", width=150, anchor="center", stretch=True)
        self.table.heading("Quantity", text="Quantity")

        self.table.column("Available", width=150, anchor="center", stretch=True)
        self.table.heading("Available", text="Available")

        self.table.column("Type", width=150, anchor="center", stretch=True)
        self.table.heading("Type", text="Type")

        # Add some data to the table
        for index, x in enumerate(supply_lst.list):
            self.table.insert("", "end", values=(x.name, x.all_units, x.available_units, x.type), iid=index)

        # Buttons to interact with the selected line of the table
        self.button_acquire = customtkinter.CTkButton(self.right_dashboard, text="Acquire",
                                                      command=self.acquire_item)
        self.button_acquire.pack(side=tkinter.LEFT, padx=10, pady=10)

        def help_func():
            ctypes.windll.user32.MessageBoxW(0,
                                             "Here are the app instructions:\n\n1. Press aquire to choose a product to rent\n2. Choose amount and return date\n3. Press confirm\n4. Enjoy and don't forget to return the product!\n5. Go to your profile to see which products you have rented\n6. Chech the notifications once in a while",
                                             "Help", 0)

        self.help_BTN = customtkinter.CTkButton(master=self.right_dashboard, text="Help",
                                                command=help_func,
                                                corner_radius=6)
        self.help_BTN.pack(side=tkinter.RIGHT, padx=10, pady=10)



    elif type == 'profile':

        self.toptitle = customtkinter.CTkLabel(self.right_dashboard, text="Supply Solutions - Profile \n",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.toptitle.pack(pady=10)

        self.table.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        # Define the columns of the table
        self.table["columns"] = ("Item name", "Quantity", "Borrow date", "Expected return date")

        # Set the headings of the columns
        self.table.column("Item name", width=100, anchor="center", stretch=True)
        self.table.heading("Item name", text="Item name")

        self.table.column("Quantity", width=100, anchor="center", stretch=True)
        self.table.heading("Quantity", text="Quantity")

        self.table.column("Borrow date", width=100, anchor="center", stretch=True)
        self.table.heading("Borrow date", text="Borrow date")

        self.table.column("Expected return date", width=100, anchor="center", stretch=True)
        self.table.heading("Expected return date", text="Expected return date")

        response = requests.post(url + 'getBorrowedItems',data = {'user_id':user.id})
        items = []
        return_time = []
        take_time = []
        quantity = []
        lst = []
        if response.status_code == 200:
            result = response.json()
            if result['message'] == 'successful':
                temp = result['items']
                t = 1
                datez = datetime.now()
                for i in temp:
                    items.append(supply_lst.get_name_by_id(i[1]))
                    return_time.append(i[5])
                    take_time.append(i[4])
                    quantity.append(i[3])
                    given_date = datetime.strptime(i[5], '%a, %d %b %Y %H:%M:%S %Z')

                    # if the user is late so the item will be marked in red
                    if given_date < datez:
                        lst.append(t)
                    t += 1
                print(temp)

        # Add some data to the table
        for i in range(0, len(items)):
            row_values = (items[i], quantity[i], take_time[i], return_time[i])
            tags = () if (i + 1) not in lst else ('red',)  # Add 'red' tag if the row is late
            self.table.insert("", "end", values=row_values, tags=tags)

        # Configure the 'red' tag to set the row background color to red
        self.table.tag_configure('red', background='red')

        # Buttons to interact with the selected line of the table
        self.button_acquire = customtkinter.CTkButton(self.right_dashboard, text="Return Items",
                                                      command=self.return_item)
        self.button_acquire.pack(side=tkinter.LEFT, padx=10, pady=10)

        self.button_item_desc = customtkinter.CTkButton(self.right_dashboard, text="Report Item",
                                                        command=self.report_item)
        self.button_item_desc.pack(side=tkinter.LEFT, padx=10, pady=10)


    elif type == 'noti':

        self.toptitle = customtkinter.CTkLabel(self.right_dashboard, text="Supply Solutions - Notifications \n",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.toptitle.pack(pady=10)

        self.table.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        # Define the columns of the table
        self.table["columns"] = ("Report number", "Item name", "Issue", "Description")

        # Set the headings of the columns
        self.table.column("Report number", width=100, anchor="center", stretch=True)
        self.table.heading("Report number", text="Report number")

        self.table.column("Item name", width=100, anchor="center", stretch=True)
        self.table.heading("Item name", text="Item name")

        self.table.column("Issue", width=100, anchor="center", stretch=True)
        self.table.heading("Issue", text="Issue")

        self.table.column("Description", width=100, anchor="center", stretch=True)
        self.table.heading("Description", text="Description")
        # Add some data to the table
        for x in supply_lst.list:
            self.table.insert("", "end", values=(x.name, x.all_units, x.available_units, x.type))

        # Buttons to interact with the selected line of the table
        self.button_fix = customtkinter.CTkButton(self.right_dashboard, text="Take care of report",
                                                      command=self.fix_item)
        self.button_fix.pack(side=tkinter.LEFT, padx=10, pady=10)

    self.button_item_desc = customtkinter.CTkButton(self.right_dashboard, text="Item Description",
                                                command=lambda:item_desc(self))
    self.button_item_desc.pack(side=tkinter.LEFT, padx=10, pady=10)

    def item_desc(self):
        selected_item = self.table.item(self.table.selection())
        if selected_item is None:
            # No item is currently selected
            return
        des = supply_lst.get_des_by_name(selected_item['values'][0])
        ctypes.windll.user32.MessageBoxW(0,
                                         f"description: {des}\n ",
                                         "Description", 0)



if __name__ == '__main__':
    # Example usage
    # data = None
    # choose_date_time()
    #
    # # Print the selected datetime
    # if data:
    #     print("Selected datetime:", data)
    # else:
    #     print("No datetime selected.")
    login_page(app)