import tkinter as tk
from tkinter import messagebox, scrolledtext
import shelve
import time
from datetime import datetime

# Initialize the shelve database
with shelve.open('atm_shelve.db') as db:
    if 'users' not in db:
        db['users'] = {}  # Initialize users dictionary
    if 'transactions' not in db:
        db['transactions'] = {}  # Initialize transactions dictionary

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.current_user = None  # Add current_user attribute
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for f in (startPage, MenuPage, create_ac, withdrawPage, depositePage, balancePage, transactionPage, accountPage, resetPage, deletPage):
            page_name = f.__name__
            frame = f(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("startPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class startPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#002699')
        self.controller = controller
        self.controller.title('ATM MANAGEMENT SYSTEM')
        self.controller.state('zoomed')

        localtime = time.asctime(time.localtime(time.time()))
        lb2 = tk.Label(self, text=localtime, fg="black", font="orbiton 15 ", bd=5, bg="#002699", anchor='w')
        lb2.pack()

        headinglbl = tk.Label(self, text="WELCOME TO BANK OF PYTHON", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglbl.pack(pady=25)

        space_label = tk.Label(self, height=4, width=100, bg='#002699')
        space_label.pack(pady=20)

        user_label = tk.Label(self, text='Enter your username', font="comicsans 15 bold", bg='#002699', fg='white')
        user_label.pack(pady=10)

        username = tk.StringVar()
        username_entry_box = tk.Entry(self, textvariable=username, font=("comicsans 15 bold"), width=35)
        username_entry_box.pack(ipady=7)

        password_label = tk.Label(self, text='Enter your password', font="comicsans 15 bold", bg='#002699', fg='white')
        password_label.pack(pady=10)

        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self, show="*", textvariable=my_password, font=("comicsans 15 bold"), width=35)
        password_entry_box.pack(ipady=7)

        def menu():
            controller.show_frame("MenuPage")
            username.set('')
            my_password.set('')

        def verify_login():
            user = username.get()
            pin = my_password.get()
            with shelve.open('atm_shelve.db') as db:
                users = db['users']
                if user in users and users[user]['pin'] == my_password.get():
                    messagebox.showinfo("Success", "Login successful.")
                    controller.current_user = user  # Set current_user
                    menu()
                else:
                    messagebox.showerror("Error", "Invalid username or PIN.")

        enter_button = tk.Button(self, text='check your account', command=verify_login, relief='raised', borderwidth=3, width=40, height=3)
        enter_button.pack(pady=10)

        def create_account():
            controller.show_frame("create_ac")
            username.set('')
            my_password.set('')

        create_account_button = tk.Button(self, text='create new account', command=create_account, relief='raised', borderwidth=3, width=20, height=1)
        create_account_button.pack(padx=10, pady=20)

        def manage_account():
            controller.show_frame("accountPage")
            username.set('')
            my_password.set('')

        manage_account_button = tk.Button(self, text='manage account', command=manage_account, relief='raised', borderwidth=3, width=20, height=1)
        manage_account_button.pack(padx=10, pady=20)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(fill="x", side='bottom')

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#002699')
        self.controller = controller

        headinglb = tk.Label(self, text=" ATM MACHINE SERVICE", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglb.pack(pady=25)

        main_menu_label = tk.Label(self, text='Main Menu', font=('area', 15), fg='white', bg='#002699')
        main_menu_label.pack()

        selection_label = tk.Label(self, text='please make a selection', font=('area', 15), fg='white', bg='#002699', anchor='w')
        selection_label.pack(fill='x')

        button_frame = tk.Frame(self, bg='#000066')
        button_frame.pack(fill='both', expand=True)

        def withdraw():
            controller.show_frame("withdrawPage")

        withdraw_button = tk.Button(button_frame, text="Withdraw", command=withdraw, relief='raised', borderwidth=3, width=50, height=5)
        withdraw_button.grid(row=0, column=0, pady=5)

        def deposite():
            controller.show_frame("depositePage")

        deposite_button = tk.Button(button_frame, text="deposite", command=deposite, relief='raised', borderwidth=3, width=50, height=5)
        deposite_button.grid(row=1, column=0, pady=5)

        def balance():
            controller.show_frame("balancePage")

        balance_button = tk.Button(button_frame, text="balance", command=balance, relief='raised', borderwidth=3, width=50, height=5)
        balance_button.grid(row=3, column=0, pady=5)

        def transaction():
            controller.show_frame("transactionPage")

        transaction_button = tk.Button(button_frame, text="transaction history", command=transaction, relief='raised', borderwidth=3, width=50, height=5)
        transaction_button.grid(row=4, column=0, pady=5)

        def exit():
            controller.show_frame("startPage")

        exit_button = tk.Button(button_frame, text="Exit", command=exit, relief='raised', borderwidth=3, width=50, height=5)
        exit_button.grid(row=5, column=0, pady=5)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(side='bottom', fill="x")

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

class create_ac(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#002699")
        self.controller = controller
        headinglb = tk.Label(self, text=" ATM MACHINE SERVICE", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglb.pack(pady=25)

        space_label = tk.Label(self, height=4, width=100, bg='#002699')
        space_label.pack(pady=20)

        user_name_label = tk.Label(self, text='Enter username', font="comicsans 15 bold", bg='#002699', fg='white')
        user_name_label.pack(pady=10)

        username = tk.StringVar()
        username_entry_box = tk.Entry(self, textvariable=username, font=("comicsans 15 bold"), width=35)
        username_entry_box.pack(ipady=7)

        user_name_label = tk.Label(self, text='Enter password', font="comicsans 15 bold", bg='#002699', fg='white')
        user_name_label.pack(pady=10)

        password = tk.StringVar()
        password_entry_box = tk.Entry(self, show='*', textvariable=password, font=("comicsans 15 bold"), width=35)
        password_entry_box.pack(ipady=10)

        def exit():
            controller.show_frame("startPage")
            username.set('')
            password.set('')

        def save_account():
            user = username.get()
            pin = password.get()
            with shelve.open('atm_shelve.db') as db:
                users = db['users']
                transactions = db['transactions']
                if user in users:
                    messagebox.showerror("Error", "Username already exists.")
                else:
                    users[user] = {'pin': password.get(), 'balance': 0}
                    transactions[user] = []  # Initialize transaction history
                    db['users'] = users
                    db['transactions'] = transactions
                    messagebox.showinfo("Success", "Account created successfully.")

        create_account_button = tk.Button(self, text='Create', command=save_account, relief='raised', borderwidth=3, width=40, height=3)
        create_account_button.pack(pady=10)

        exit_button = tk.Button(self, text="Exit", command=exit, relief='raised', borderwidth=3, width=40, height=3)
        exit_button.pack(pady=10)

        two_tone_label = tk.Label(self, bg="#000066")
        two_tone_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(side='bottom', fill="x")

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

class withdrawPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#002699')
        self.controller = controller

        headinglb = tk.Label(self, text=" ATM MACHINE SERVICE", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglb.pack(pady=25)

        space_label = tk.Label(self, height=10, width=100, bg='#002699')
        space_label.pack(pady=20)

        password_label = tk.Label(self, text='Enter your amount to withdraw', font="comicsans 15 bold", bg='#002699', fg='white')
        password_label.pack(pady=10)

        my_amount = tk.StringVar()
        username_entry_box = tk.Entry(self, textvariable=my_amount, font=("comicsans 15 bold"), width=35)
        username_entry_box.pack(ipady=7)

        def withdraw():
            user = controller.current_user
            amount = float(my_amount.get())
            with shelve.open('atm_shelve.db') as db:
                users = db['users']
                transactions = db['transactions']
                if users[user]['balance'] >= amount:
                    users[user]['balance'] -= amount
                    transactions[user].append(f"{datetime.now()} - Withdrew: Rs{amount}")
                    db['users'] = users
                    db['transactions'] = transactions
                    messagebox.showinfo("Success", f"Withdrawal successful. New balance: {users[user]['balance']}")
                else:
                    messagebox.showerror("Error", "Insufficient balance.")

        enter_button = tk.Button(self, text='Withdraw', command=withdraw, relief='raised', borderwidth=3, width=40, height=3)
        enter_button.pack(pady=10)

        def exit():
            controller.show_frame("startPage")
            my_amount.set('')

        def menu():
            controller.show_frame("MenuPage")
            my_amount.set('')

        button_frame = tk.Frame(self, bg='#000066')
        button_frame.pack(fill='none', expand=True)

        menu_button = tk.Button(button_frame, text="Menu", command=menu, relief='raised', borderwidth=3, width=50, height=2)
        menu_button.grid(row=0, column=0, pady=5)

        exit_button = tk.Button(button_frame, text="Exit", command=exit, relief='raised', borderwidth=3, width=50, height=2)
        exit_button.grid(row=0, column=1, pady=5)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(side='bottom', fill="x")

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

class depositePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#002699')
        self.controller = controller

        headinglbl = tk.Label(self, text=" ATM MACHINE SERVICE", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglbl.pack(pady=25)

        space_label = tk.Label(self, height=4, width=100, bg='#002699')
        space_label.pack(pady=20)

        password_label = tk.Label(self, text='Enter your amount to deposite', font="comicsans 15 bold", bg='#002699', fg='white')
        password_label.pack(pady=10)

        my_amount = tk.StringVar()
        username_entry_box = tk.Entry(self, textvariable=my_amount, font=("comicsans 15 bold"), width=35)
        username_entry_box.pack(ipady=7)

        def perform_deposit():
            amount = float(my_amount.get())
            user = controller.current_user
            with shelve.open('atm_shelve.db') as db:
                users = db['users']
                transactions = db['transactions']
                users[user]['balance'] += amount
                transactions[user].append(f"{datetime.now()} - Deposited: Rs{amount}")
                db['users'] = users
                db['transactions'] = transactions
                messagebox.showinfo("Success", f"Deposit successful. New balance: {users[user]['balance']}")

        enter_button = tk.Button(self, text='Deposite', command=perform_deposit, relief='raised', borderwidth=3, width=40, height=3)
        enter_button.pack(pady=10)

        def exit():
            controller.show_frame("startPage")
            my_amount.set('')

        def menu():
            controller.show_frame("MenuPage")
            my_amount.set('')

        button_frame = tk.Frame(self, bg='#000066')
        button_frame.pack(fill='none', expand=True)

        menu_button = tk.Button(button_frame, text="Menu", command=menu, relief='raised', borderwidth=3, width=50, height=2)
        menu_button.grid(row=0, column=0, pady=5)

        exit_button = tk.Button(button_frame, text="Exit", command=exit, relief='raised', borderwidth=3, width=50, height=2)
        exit_button.grid(row=0, column=1, pady=5)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(side='bottom', fill="x")

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

class balancePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#002699')
        self.controller = controller

        headinglb = tk.Label(self, text=" ATM MACHINE SERVICE", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglb.pack(pady=25)

        space_label = tk.Label(self, height=10, width=100, bg='#002699')
        space_label.pack(pady=20)

        def balance():
            user = controller.current_user
            with shelve.open('atm_shelve.db') as db:
                users = db['users']
                transactions = db['transactions']
                db['users'] = users
                db['transactions'] = transactions
                messagebox.showinfo("Success", f"{user} your account balance: {users[user]['balance']}")

        enter_button = tk.Button(self, text='Fetch Balance', command=balance, relief='raised', borderwidth=3, width=40, height=3)
        enter_button.pack(pady=10)

        def exit():
            controller.show_frame("startPage")

        def menu():
            controller.show_frame("MenuPage")

        button_frame = tk.Frame(self, bg='#000066')
        button_frame.pack(fill='none', expand=True)

        menu_button = tk.Button(button_frame, text="Menu", command=menu, relief='raised', borderwidth=3, width=50, height=2)
        menu_button.grid(row=0, column=0, pady=5)

        exit_button = tk.Button(button_frame, text="Exit", command=exit, relief='raised', borderwidth=3, width=50, height=2)
        exit_button.grid(row=0, column=1, pady=5)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(side='bottom', fill="x")

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

class transactionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#002699')
        self.controller = controller

        headinglb = tk.Label(self, text=" ATM MACHINE SERVICE", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglb.pack(pady=25)

        space_label = tk.Label(self, height=10, width=100, bg='#002699')
        space_label.pack(pady=20)

        def view_transactions():
            user = controller.current_user
            with shelve.open('atm_shelve.db') as db:
                transactions = db['transactions'][user]

            transaction_text = scrolledtext.ScrolledText(self, width=50, height=20)
            transaction_text.pack(pady=10)
            for transaction in transactions:
                transaction_text.insert(tk.END, transaction + "\n")

        enter_button = tk.Button(self, text='Get passbook', command=view_transactions, relief='raised', borderwidth=3, width=40, height=3)
        enter_button.pack(pady=10)

        button_frame = tk.Frame(self, bg='#000066')
        button_frame.pack(fill='none', expand=True)

        def exit():
            controller.show_frame("startPage")

        def menu():
            controller.show_frame("MenuPage")

        menu_button = tk.Button(button_frame, text="Menu", command=menu, relief='raised', borderwidth=3, width=50, height=2)
        menu_button.grid(row=0, column=0, pady=5)

        exit_button = tk.Button(button_frame, text="Exit", command=exit, relief='raised', borderwidth=3, width=50, height=2)
        exit_button.grid(row=0, column=1, pady=5)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(side='bottom', fill="x")

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

class resetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#002699')
        self.controller = controller

        headinglbl = tk.Label(self, text="WELCOME TO BANK OF PYTHON", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglbl.pack(pady=25)

        space_label = tk.Label(self, height=4, width=100, bg='#002699')
        space_label.pack(pady=20)

        user_label = tk.Label(self, text='Enter your username', font="comicsans 15 bold", bg='#002699', fg='white')
        user_label.pack(pady=10)

        username = tk.StringVar()
        username_entry_box = tk.Entry(self, textvariable=username, font=("comicsans 15 bold"), width=35)
        username_entry_box.pack(ipady=7)

        password_label = tk.Label(self, text='Enter your password', font="comicsans 15 bold", bg='#002699', fg='white')
        password_label.pack(pady=10)

        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self, show="*", textvariable=my_password, font=("comicsans 15 bold"), width=35)
        password_entry_box.pack(ipady=7)

        def menu():
            controller.show_frame("MenuPage")
            username.set('')
            my_password.set('')

        def verify_login():
            user = username.get()
            pin = my_password.get()
            with shelve.open('atm_shelve.db') as db:
                users = db['users']
                if user in users and users[user]['pin'] == my_password.get():
                    messagebox.showinfo("Success", "Login successful.")
                    reset_pass()
                else:
                    messagebox.showerror("Error", "Invalid username or PIN.")

        password_label = tk.Label(self, text='Enter new password', font="comicsans 15 bold", bg='#002699', fg='white')
        password_label.pack(pady=10)

        new_password = tk.StringVar()
        password_entry_box = tk.Entry(self, show="*", textvariable=new_password, font=("comicsans 15 bold"), width=35)
        password_entry_box.pack(ipady=7)

        def reset_pass():
            user = username.get()
            pin = new_password.get()
            with shelve.open('atm_shelve.db') as db:
                users = db['users']
                users[user]['pin'] = pin
                db['users'] = users
                messagebox.showinfo("Success", "Password reset successful.")

        enter_button = tk.Button(self, text='Reset password', command=verify_login, relief='raised', borderwidth=3, width=40, height=3)
        enter_button.pack(pady=10)

        def exit():
            controller.show_frame("startPage")
            username.set('')
            my_password.set('')

        button_frame = tk.Frame(self, bg='#000066')
        button_frame.pack(fill='none', expand=True)

        exit_button = tk.Button(button_frame, text="Exit", command=exit, relief='raised', borderwidth=3, width=50, height=2)
        exit_button.grid(row=0, column=1, pady=5)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(side='bottom', fill="x")

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

class deletPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#002699')
        self.controller = controller

        headinglbl = tk.Label(self, text="WELCOME TO BANK OF PYTHON ", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglbl.pack(pady=25)

        space_label = tk.Label(self, height=4, width=100, bg='#002699')
        space_label.pack(pady=20)

        user_label = tk.Label(self, text='Enter your username', font="comicsans 15 bold", bg='#002699', fg='white')
        user_label.pack(pady=10)

        username = tk.StringVar()
        username_entry_box = tk.Entry(self, textvariable=username, font=("comicsans 15 bold"), width=35)
        username_entry_box.pack(ipady=7)

        password_label = tk.Label(self, text='Enter your password', font="comicsans 15 bold", bg='#002699', fg='white')
        password_label.pack(pady=10)

        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self, show="*", textvariable=my_password, font=("comicsans 15 bold"), width=35)
        password_entry_box.pack(ipady=7)

        def verify_login():
            user = username.get()
            pin = my_password.get()
            with shelve.open('atm_shelve.db') as db:
                users = db['users']
                if user in users and users[user]['pin'] == my_password.get():
                    messagebox.showinfo("Success", "Login successful.")
                    delet_account()
                else:
                    messagebox.showerror("Error", "Invalid username or PIN.")

        def delet_account():
            user = username.get()
            pin = my_password.get()
            with shelve.open('atm_shelve.db') as db:
                users = db['users']
                transactions = db['transactions']
                if user in users:
                    del users[user]
                    del transactions[user]
                    db['users'] = users
                    db['transactions'] = transactions
                    messagebox.showinfo("Success", "Account deleted successfully.")
                else:
                    messagebox.showerror("Error", "Account not found.")

        enter_button = tk.Button(self, text='Delet Account', command=verify_login, relief='raised', borderwidth=3, width=40, height=3)
        enter_button.pack(pady=10)

        def exit():
            controller.show_frame("startPage")
            username.set('')
            my_password.set('')

        button_frame = tk.Frame(self, bg='#000066')
        button_frame.pack(fill='none', expand=True)

        exit_button = tk.Button(button_frame, text="Exit", command=exit, relief='raised', borderwidth=3, width=50, height=2)
        exit_button.grid(row=0, column=1, pady=5)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(side='bottom', fill="x")

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

class accountPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#002699')
        self.controller = controller

        headinglbl = tk.Label(self, text="WELCOME TO BANK OF PYTHON", font="comicsans 45 bold", fg="white", bg="#002699")
        headinglbl.pack(pady=25)

        space_label = tk.Label(self, height=4, width=100, bg='#002699')
        space_label.pack(pady=20)

        def reset_Page():
            controller.show_frame("resetPage")

        reset_button = tk.Button(self, text="Reset password", command=reset_Page, relief='raised', borderwidth=3, width=50, height=2)
        reset_button.pack(pady=5)

        def delet_page():
            controller.show_frame("deletPage")

        delet_button = tk.Button(self, text="Delet account", command=delet_page, relief='raised', borderwidth=3, width=50, height=2)
        delet_button.pack(pady=5)

        def exit():
            controller.show_frame("startPage")

        exit_button = tk.Button(self, text="Exit", command=exit, relief='raised', borderwidth=3, width=50, height=2)
        exit_button.pack(pady=5)

        bottom_frame = tk.Frame(self, width=200, height=100, bg="white", borderwidth=3)
        bottom_frame.pack(side='bottom', fill="x")

        def tick():
            current_time = time.strftime('%H:%M:%p')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('area', 12))
        time_label.pack(side='right')
        tick()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

