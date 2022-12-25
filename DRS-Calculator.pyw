from tkinter import *
from tkinter import messagebox, filedialog, ttk
from re import match, fullmatch
from os import listdir, mkdir, makedirs, remove, path
from shutil import rmtree, move
from csv import writer, reader
from string import ascii_letters, digits
from random import sample
from filetype import guess_mime


class Account:
    def __init__(self, email, username, password):
        self.__email = email
        self.__username = username
        self.__password = password
        self.add_account()

    def add_account(self):
        self.check_data()
        with open(r"data\account.csv", "a", newline='') as csvfile:
            w = writer(csvfile)
            w.writerow([self.__username, self.__password, self.__email])
        makedirs(r'data\folders_accounts\{}'.format(self.__username))
        messagebox.showinfo(
            'SING UP', 'Your account has been successfully added')

    def check_data(self):
        if 'data' not in listdir():
            makedirs(r'data\folders_accounts')
            with open(r'data\account.csv', 'wt') as file:
                pass
        else:
            if 'folders_accounts' not in listdir(r'data'):
                mkdir(r'data\folders_accounts')
            if 'account.csv' not in listdir(r'data'):
                with open(r'data\account.csv', 'wt') as file:
                    pass

    def exist_username(self, username):
        self.check_data()
        if username in listdir(r'data\folders_accounts'):
            return True

    def try_login(self, username, password):
        self.check_data()
        with open(r'data\account.csv', 'rt') as csvfile:
            for row in reader(csvfile):
                if not row:
                    continue
                if row[0] == username and row[1] == password:
                    return 1
            else:
                if self.exist_username(username):
                    messagebox.showwarning(
                        'Invalide password', 'The password is incorrect')
                    return 0
                else:
                    messagebox.showerror(
                        'Invalide Account', 'This account does not exist')
                    return 0


class Secret_interface(Account):
    def __init__(self):
        self.window = Tk()
        self.window.title('DRS-Secret_interface')
        self.window.geometry('1000x700+350+100')
        self.window.resizable('0', '0')

        self.menu = Frame(self.window)
        self.menu.place(x=0, y=0, width=1000, height=150)

        self.btn_login = Button(self.menu, text='LOG IN', font=(
            'verdana', 50, 'bold'), relief=SUNKEN, command=self.show_frame_login)
        self.btn_login.place(x=0, y=0, width=500, height=150)

        self.btn_singup = Button(self.menu, text='SING UP', font=(
            'verdana', 50, 'bold'), relief=GROOVE, bg="#d3d3d3", command=self.show_frame_singup)
        self.btn_singup.place(x=500, y=0, width=500, height=150)

        # Frame Log in -----------------------------------------------------------------
        self.frame_login = Frame(self.window)
        self.frame_login.place(x=0, y=150, height=500, width=1000)

        Label(self.frame_login, text="Usename : ", font=(
            'curier', 30, 'bold')).place(x=50, y=100)
        var_username_login = StringVar()
        self.entry_username_login = Entry(self.frame_login, textvariable=var_username_login, border=0, font=(
            'Mycrosoft YaHei UI Light', 30, 'bold'))
        self.entry_username_login.place(x=300, y=100, width=600)

        Label(self.frame_login, text="Password : ", font=(
            'curier', 30, 'bold')).place(x=50, y=200)
        var_password_login = StringVar()
        self.entry_password_login = Entry(self.frame_login, textvariable=var_password_login, border=0, font=(
            'Mycrosoft YaHei UI Light', 30, 'bold'))
        self.entry_password_login.place(x=300, y=200, width=600)

        Button(self.frame_login, text='Log in', font=(
            'curier', 35, 'bold'), command=self.login, relief=GROOVE).place(x=300, y=300)
        Button(self.frame_login, text='Reset', font=('curier', 35, 'bold'),
               command=self.resret_frame_login, relief=GROOVE).place(x=500, y=300)
        # ---------------------------------------------------------------------------------------

        # Frame Sing up ------------------------------------------------------------------------
        self.frame_singup = Frame(self.window)

        Label(self.frame_singup, text="Email : ", font=(
            'curier', 30, 'bold')).place(x=50, y=100)
        var_email_singup = StringVar()
        self.entry_email_singup = Entry(self.frame_singup, textvariable=var_email_singup, border=0, font=(
            'Mycrosoft YaHei UI Light', 30, 'bold'))
        self.entry_email_singup.place(x=300, y=100, width=600)
        Label(self.frame_singup, text="Usename : ", font=(
            'curier', 30, 'bold')).place(x=50, y=200)

        var_username_singup = StringVar()
        self.entry_username_singup = Entry(self.frame_singup, textvariable=var_username_singup, border=0, font=(
            'Mycrosoft YaHei UI Light', 30, 'bold'))
        self.entry_username_singup.place(x=300, y=200, width=600)

        Label(self.frame_singup, text="Password : ", font=(
            'curier', 30, 'bold')).place(x=50, y=300)
        var_password_singup = StringVar()
        self.entry_password_singup = Entry(self.frame_singup, textvariable=var_password_singup, border=0, font=(
            'Mycrosoft YaHei UI Light', 30, 'bold'))
        self.entry_password_singup.place(x=300, y=300, width=600)

        Button(self.frame_singup, text='Sing up', font=(
            'curier', 35, 'bold'), command=self.singup, relief=GROOVE).place(x=300, y=400)
        Button(self.frame_singup, text='Reset', font=('curier', 35, 'bold'),
               command=self.resret_frame_singup, relief=GROOVE).place(x=530, y=400)
        # -----------------------------------------------------------------------------------

    def show_frame_login(self):
        self.frame_singup.place_forget()
        self.frame_login.place(x=0, y=150, height=500, width=1000)
        self.btn_login.config(relief=SUNKEN, bg="SystemButtonFace")
        self.btn_singup.config(relief=GROOVE, bg="#d3d3d3")

    def show_frame_singup(self):
        self.frame_login.place_forget()
        self.frame_singup.place(x=0, y=150, height=500, width=1000)
        self.btn_login.config(relief=GROOVE, bg="#d3d3d3")
        self.btn_singup.config(relief=SUNKEN, bg="SystemButtonFace")

    def login(self):
        username = self.entry_username_login.get()
        password = self.entry_password_login.get()
        if self.try_login(username, password):
            self.window.destroy()
            Gallery(username)

    def singup(self):
        if self.exist_username(self.entry_username_singup.get()):
            return messagebox.showerror('Existing account', 'This username is a user !!')
        if fullmatch("\w+@[A-z]+\.\w+", self.entry_email_singup.get()) == None:
            return messagebox.showwarning('Invalid Email', 'The email you entered is invalid')

        if fullmatch("\w{6,}", self.entry_username_singup.get()) == None:
            return messagebox.showwarning('Invalid Username', 'The username you entered is invalid')

        if fullmatch("\w{8,}", self.entry_password_singup.get()) == None:
            return messagebox.showwarning('Invalid Password', 'The password you entered is invalid')

        super().__init__(self.entry_email_singup.get(),
                         self.entry_username_singup.get(), self.entry_password_singup.get())

    def resret_frame_login(self):
        self.entry_username_login.delete(0, END)
        self.entry_password_login.delete(0, END)

    def resret_frame_singup(self):
        self.entry_email_singup.delete(0, END)
        self.entry_username_singup.delete(0, END)
        self.entry_password_singup.delete(0, END)

    def loop(self):
        self.window.mainloop()


class Gallery:
    def __init__(self, username):
        self._username = username
        self.gallery = Tk()
        self.gallery.title(f'DRS-->{username}')
        self.gallery.geometry('1200x700+300+100')
        self.gallery.resizable('0', '0')

        self.menu = Frame(bg="#c1c1c1",)
        self.menu.place(x=0, y=0, width=350, height=700)

        Button(self.menu, text='Show File', font=('verdana', 25, 'bold'),
               relief=GROOVE, command=self.show_frame_show_files).place(x=0, y=0, width=350, height=100)
        Button(self.menu, text='Add File', font=('verdana', 25, 'bold'),
               relief=GROOVE, command=self.show_frame_add_file).place(x=0, y=100, width=350, height=100)
        Button(self.menu, text='Eject File', font=('verdana', 25, 'bold'),
               relief=GROOVE, command=self.try_eject_file).place(x=0, y=200, width=350, height=100)
        Button(self.menu, text='Change password', font=('verdana', 25,
               'bold'), relief=GROOVE, command=self.show_frame_change_password).place(x=0, y=300, width=350, height=100)
        Button(self.menu, text='Change email', font=('verdana', 25, 'bold'),
               relief=GROOVE, command=self.show_frame_change_email).place(x=0, y=400, width=350, height=100)
        Button(self.menu, text='Delete account', font=('verdana', 25,
               'bold'), relief=GROOVE, command=self.show_frame_delate_account).place(x=0, y=500, width=350, height=100)
        Button(self.menu, text='Exite', font=('verdana', 25, 'bold'), relief=GROOVE,
               command=self.gallery.destroy).place(x=0, y=600, width=350, height=100)

        self.__captcha = ''.join(sample(ascii_letters + '_' + digits, 6))

        # frame show Files -------------------------------------------------------------------
        self.frame_show_files = Frame()
        self.frame_show_files.place(x=350, y=0, width=850, height=700)

        self.update_treeview()

        Button(self.frame_show_files, text='Delet File', font=('Curier', 30),
               command=self.try_delete_file, relief=GROOVE).place(x=250, y=600, width=400, height=60)
        #scrollbar = ttk.Scrollbar(self.frame_show_files, orient=tk.VERTICAL, command=self.tree.yview)
        # self.tree.configure(yscroll=scrollbar.set)
        #scrollbar.grid(row=0, column=1, sticky='ns')

        # -------------------------------------------------------------------------------------

        # frame add file ---------------------------------------------------------------------
        self.frame_add_photo = Frame()
        Label(self.frame_add_photo, text="Photo : ",
              font=('ariel', 30)).place(x=40, y=250, height=60)

        self.var_photo_frame_add_photo = StringVar()
        self.entry_photo_frame_add_photo = Entry(self.frame_add_photo, state=DISABLED, relief=SOLID,
                                                 textvariable=self.var_photo_frame_add_photo, font=('ariel', 25))
        self.entry_photo_frame_add_photo.place(
            x=190, y=250, width=450, height=60)

        Button(self.frame_add_photo, text='Select photo', font=('ariel', 18), relief=GROOVE,
               command=lambda: self.var_photo_frame_add_photo.set(filedialog.askopenfilename())).place(x=640, y=250, height=60)

        Button(self.frame_add_photo, text='Add File', font=(
            'ariel', 30, 'bold'), command=self.try_add_photo, relief=RIDGE).place(x=100, y=500, width=310)
        Button(self.frame_add_photo, text='Reset', font=('ariel', 30, 'bold'),
               command=lambda: self.var_photo_frame_add_photo.set(''), relief=RIDGE).place(x=450, y=500, width=310)
        # -------------------------------------------------------------------------------------

        # frame change password ---------------------------------------------------------------
        self.frame_change_password = Frame(self.gallery)

        Label(self.frame_change_password, text="Username : ",
              font=('ariel', 25)).place(x=40, y=150)
        Label(self.frame_change_password, text="Current password : ",
              font=('ariel', 25)).place(x=40, y=250)
        Label(self.frame_change_password, text="New password : ",
              font=('ariel', 25)).place(x=40, y=350)

        var_username_frame_change_password = StringVar()
        entry_username_frame_change_password = Entry(self.frame_change_password,
                                                     textvariable=var_username_frame_change_password, font=('ariel', 25))
        entry_username_frame_change_password.place(x=350, y=150, width=450)
        entry_username_frame_change_password.insert(0, username)
        entry_username_frame_change_password.config(state=DISABLED)

        var_current_password_frame_change_password = StringVar()
        self.entry_current_password_frame_change_password = Entry(
            self.frame_change_password, textvariable=var_current_password_frame_change_password, font=('ariel', 25))
        self.entry_current_password_frame_change_password.place(
            x=350, y=250, width=450)

        var_new_password = StringVar()
        self.entry_new_password_frame_change_password = Entry(
            self.frame_change_password, textvariable=var_new_password, font=('ariel', 25))
        self.entry_new_password_frame_change_password.place(
            x=350, y=350, width=450)

        Button(self.frame_change_password, text='Save change', font=(
            'ariel', 30, 'bold'), command=self.try_change_password, relief=RIDGE).place(x=100, y=500, width=310)
        Button(self.frame_change_password, text='Reset', font=('ariel', 30, 'bold'),
               command=self.reset_frame_change_password, relief=RIDGE).place(x=450, y=500, width=310)
        # -------------------------------------------------------------------------------------

        # frame change email ------------------------------------------------------------------
        self.frame_change_email = Frame()

        Label(self.frame_change_email, text="Username : ",
              font=('ariel', 25)).place(x=40, y=150)
        Label(self.frame_change_email, text="Password : ",
              font=('ariel', 25)).place(x=40, y=250)
        Label(self.frame_change_email, text="New Email : ",
              font=('ariel', 25)).place(x=40, y=350)

        var_username_frame_change_email = StringVar()
        entry_username_frame_change_email = Entry(self.frame_change_email,
                                                  textvariable=var_username_frame_change_email, font=('ariel', 25))
        entry_username_frame_change_email.place(x=350, y=150, width=450)
        entry_username_frame_change_email.insert(0, username)
        entry_username_frame_change_email.config(state=DISABLED)

        var_password_frame_change_email = StringVar()
        self.entry_password_frame_change_email = Entry(
            self.frame_change_email, textvariable=var_password_frame_change_email, font=('ariel', 25))
        self.entry_password_frame_change_email.place(x=350, y=250, width=450)

        var_new_email_frame_change_email = StringVar()
        self.entry_new_email_frame_change_email = Entry(
            self.frame_change_email, textvariable=var_new_email_frame_change_email, font=('ariel', 25))
        self.entry_new_email_frame_change_email.place(x=350, y=350, width=450)

        Button(self.frame_change_email, text='Save change', font=(
            'ariel', 30, 'bold'), command=self.try_change_email, relief=RIDGE).place(x=100, y=500, width=310)
        Button(self.frame_change_email, text='Reset', font=('ariel', 30, 'bold'),
               command=self.reset_frame_change_email, relief=RIDGE).place(x=450, y=500, width=310)
        # -------------------------------------------------------------------------------------

        # frame delete account ----------------------------------------------------------------
        self.frame_delate_account = Frame()

        Label(self.frame_delate_account, text="Username : ",
              font=('ariel', 25)).place(x=40, y=50)
        Label(self.frame_delate_account, text="Password : ",
              font=('ariel', 25)).place(x=40, y=150)
        Label(self.frame_delate_account, text="CAPTCHA : ",
              font=('ariel', 25)).place(x=40, y=250)
        Label(self.frame_delate_account, text="Characters : ",
              font=('ariel', 25)).place(x=40, y=350)

        var_username_frame_delate_account = StringVar()
        entry_username_frame_delate_account = Entry(self.frame_delate_account,
                                                    textvariable=var_username_frame_delate_account, font=('ariel', 25))
        entry_username_frame_delate_account.place(x=350, y=50, width=450)
        entry_username_frame_delate_account.insert(0, username)
        entry_username_frame_delate_account.config(state=DISABLED)

        var_password_frame_delate_account = StringVar()
        self.entry_password_frame_delate_account = Entry(
            self.frame_delate_account, textvariable=var_password_frame_delate_account, font=('ariel', 25))
        self.entry_password_frame_delate_account.place(x=350, y=150, width=450)

        var_captcha_frame_delate_account = StringVar()
        self.entry_captcha_frame_delate_account = Entry(
            self.frame_delate_account, textvariable=var_captcha_frame_delate_account, font=('Segoe Print', 25, 'bold'))
        self.entry_captcha_frame_delate_account.place(
            x=350, y=250, width=450, height=45)
        self.entry_captcha_frame_delate_account.insert(0, self.__captcha)
        self.entry_captcha_frame_delate_account.config(state=DISABLED)

        var_write_captcha_frame_delate_account = StringVar()
        self.entry_write_captcha_frame_delate_account = Entry(
            self.frame_delate_account, textvariable=var_write_captcha_frame_delate_account, font=('ariel', 25))
        self.entry_write_captcha_frame_delate_account.place(
            x=350, y=350, width=450)

        Button(self.frame_delate_account, text='Delete account', font=(
            'ariel', 30, 'bold'), command=self.try_delate_accout, relief=RIDGE).place(x=100, y=500, width=310)
        Button(self.frame_delate_account, text='Reset', font=('ariel', 30, 'bold'),
               command=self.reset_frame_delate_account, relief=RIDGE).place(x=450, y=500, width=310)

        # -------------------------------------------------------------------------------------
    def update_treeview(self):

        columns = ('ID', 'File_Name', 'File_Type', 'File_Size')
        self.tree = ttk.Treeview(
            self.frame_show_files, columns=columns, show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('File_Name', text='Name File')
        self.tree.heading('File_Type', text='File Type')
        self.tree.heading('File_Size', text='File Size')

        folders = []
        id = 1
        for folder in listdir(r'data\folders_accounts\{}'.format(self._username)):
            fileType = guess_mime(
                r'data\folders_accounts\{}\{}'.format(self._username, folder))
            fileSize = str(path.getsize(r'data\folders_accounts\{}\{}'.format(
                self._username, folder))) + ' bytes'
            folders.append((str(id), folder, fileType, fileSize))
            id += 1
        for folder in folders:
            self.tree.insert('', END, values=folder)

        self.tree.place(x=0, y=0, width=850, height=600)

    def get_password(self, username):
        with open(r'data\account.csv', 'rt') as csvfile:
            for acc in reader(csvfile):
                if not acc:
                    continue
                if acc[0] == username:
                    return acc[1]

    def set_password(self, username, password):
        with open(r'data\account.csv', 'rt') as csvfile:
            list_acc = []
            for acc in reader(csvfile):
                if not acc:
                    continue
                if acc[0] == username:
                    list_acc.append([acc[0], password, acc[2]])
                    continue
                list_acc.append(acc)
        with open(r'data\account.csv', 'wt', newline='') as csvfile:
            w = writer(csvfile)
            for acc in list_acc:
                w.writerow(acc)
        messagebox.showinfo('Change Password', 'Password changed successfully')

    def get_email(self, username):
        with open(r'data\account.csv', 'rt') as csvfile:
            for acc in reader(csvfile):
                if not acc:
                    continue
                if acc[0] == username:
                    return acc[2]

    def set_email(self, username, email):
        with open(r'data\account.csv', 'rt') as csvfile:
            list_acc = []
            for acc in reader(csvfile):
                if not acc:
                    continue
                if acc[0] == username:
                    list_acc.append([acc[0], acc[1], email])
                    continue
                list_acc.append(acc)
        with open(r'data\account.csv', 'wt', newline='') as csvfile:
            w = writer(csvfile)
            for acc in list_acc:
                w.writerow(acc)
        messagebox.showinfo('Change Email', 'Email changed successfully')

    def try_delete_file(self):
        try:
            nameFile = self.tree.item(self.tree.focus())['values'][1]
        except:
            return messagebox.showwarning('Undefined File', 'Please select a file')
        if messagebox.askyesno('Confirm the deletion', 'Do you really want to delete this file'):
            remove(r'data\folders_accounts\{}\{}'.format(
                self._username, nameFile))
            self.update_treeview()

    def try_add_photo(self):
        if not len(self.entry_photo_frame_add_photo.get()):
            return messagebox.showwarning('Empty Path', 'Please choose a path for the file you want to add')
        name_photo = self.entry_photo_frame_add_photo.get().split('/')[-1]
        move(self.entry_photo_frame_add_photo.get(),
             r'data\folders_accounts\{}\{}'.format(self._username, name_photo))
        self.update_treeview()
        messagebox.showinfo(
            'Add successful', 'The file has been added successfully')
        self.var_photo_frame_add_photo.set('')

    def try_change_password(self):
        if self.entry_current_password_frame_change_password.get() == self.get_password(self._username):
            if fullmatch("\w{8,}", self.entry_new_password_frame_change_password.get()) == None:
                return messagebox.showwarning('Invalid Password', 'The new password you entered is invalid')
            else:
                self.set_password(
                    self._username, self.entry_new_password_frame_change_password.get())
        else:
            return messagebox.showwarning('Invalid Password', 'The password you entered is incorrect')

    def try_delate_accout(self):
        if self.entry_password_frame_delate_account.get() == self.get_password(self._username):
            if self.entry_write_captcha_frame_delate_account.get() != self.__captcha:
                return messagebox.showwarning('Invalid Captcha', 'The captcha you entered is incorrect, please try again')
            else:
                self.delete_account(self._username)
        else:
            return messagebox.showwarning('Invalid Password', 'The password you entered is incorrect')

    def try_change_email(self):
        if self.entry_password_frame_change_email.get() == self.get_password(self._username):
            if fullmatch("\w+@[A-z]+\.\w+", self.entry_new_email_frame_change_email.get()) == None:
                return messagebox.showwarning('Invalid Email', 'The new email you entered is incorrect')
            else:
                self.set_email(
                    self._username, self.entry_new_email_frame_change_email.get())
        else:
            return messagebox.showwarning('Invalid Password', 'The password you entered is incorrect')

    def delete_account(self, username):
        with open(r'data\account.csv', 'rt') as csvfile:
            list_acc = []
            for acc in reader(csvfile):
                if not acc:
                    continue
                if acc[0] == username:
                    continue
                list_acc.append(acc)
        with open(r'data\account.csv', 'wt', newline='') as csvfile:
            w = writer(csvfile)
            for acc in list_acc:
                w.writerow(acc)
        rmtree(r'data\folders_accounts\{}'.format(self._username))
        messagebox.showinfo(
            'Delete Account', 'Your account has been successfully deleted')
        self.gallery.destroy()
        return Secret_interface()

    def try_eject_file(self):
        try:
            nameFile = self.tree.item(self.tree.focus())['values'][1]
        except:
            return messagebox.showwarning('Undefined File', 'Please select a file')
        new_path = filedialog.askdirectory()
        if len(str(new_path)) != 0:
            move(r'data\folders_accounts\{}\{}'.format(
                self._username, nameFile), new_path + '\\' + nameFile)
            self.update_treeview()
            messagebox.showinfo(
                'Eject File', 'Transfer completed successfully')

    def reset_frame_change_email(self):
        self.entry_password_frame_change_email.delete(0, END)
        self.entry_new_email_frame_change_email.delete(0, END)

    def reset_frame_delate_account(self):
        self.entry_password_frame_delate_account.delete(0, END)
        self.entry_write_captcha_frame_delate_account.delete(0, END)
        self.change_captcha()

    def reset_frame_change_password(self):
        self.entry_current_password_frame_change_password.delete(0, END)
        self.entry_new_password_frame_change_password.delete(0, END)

    def show_frame_show_files(self):
        self.frame_show_files.place(x=350, y=0, width=850, height=700)
        self.frame_add_photo.place_forget()
        self.frame_change_password.place_forget()
        self.frame_change_email.place_forget()
        self.frame_delate_account.place_forget()

    def show_frame_add_file(self):
        self.frame_show_files.place_forget()
        self.frame_add_photo.place(x=350, y=0, width=850, height=700)
        self.frame_change_password.place_forget()
        self.frame_change_email.place_forget()
        self.frame_delate_account.place_forget()

    def show_frame_change_password(self):
        self.frame_show_files.place_forget()
        self.frame_add_photo.place_forget()
        self.frame_change_password.place(x=350, y=0, width=850, height=700)
        self.frame_change_email.place_forget()
        self.frame_delate_account.place_forget()

    def show_frame_change_email(self):
        self.frame_show_files.place_forget()
        self.frame_add_photo.place_forget()
        self.frame_change_password.place_forget()
        self.frame_change_email.place(x=350, y=0, width=850, height=700)
        self.frame_delate_account.place_forget()

    def show_frame_delate_account(self):
        self.frame_show_files.place_forget()
        self.frame_add_photo.place_forget()
        self.frame_change_password.place_forget()
        self.frame_change_email.place_forget()
        self.frame_delate_account.place(x=350, y=0, width=850, height=700)

        self.change_captcha()  # update captcha

    def change_captcha(self):
        self.__captcha = ''.join(sample(ascii_letters + '_' + digits, 6))
        self.entry_captcha_frame_delate_account.config(state=NORMAL)
        self.entry_captcha_frame_delate_account.delete(0, END)
        self.entry_captcha_frame_delate_account.insert(0, self.__captcha)
        self.entry_captcha_frame_delate_account.config(state=DISABLED)

    def loop(self):
        self.gallery.mainloop()


class Style:
    large_font_style = ("Arial", 40, "bold")
    small_font_style = ("Arial", 16)
    digits_font_style = ("Arial", 50, "bold")
    default_font_style = ("Arial", 40)

    off_white = "#F8FAFF"
    white = "#FFFFFF"
    light_blue = "#CCEDFF"
    light_gray = "#F5F5F5"
    label_color = "#25265E"


class Calculator(Style):

    def __init__(self):
        self.app = Tk()
        self.app.title('DRS-Calculator')
        self.app.geometry('768x655+450+150')
        self.app.resizable('0', '0')
        self.expression = ""
        self.screen_frame = Frame(self.app, height=150, bg=self.light_gray)
        self.screen_frame.pack(fill=X)

        self.buttons_frame = Frame(self.app, bg='#cfcfcf')
        self.buttons_frame.pack(expand=True, fill="both")

        # Laber screen ----- -------------------------------------------------------------------------
        self.screen = Label(self.screen_frame, text=self.expression, bg=self.light_gray,
                            fg="#383838", padx=24, font=self.digits_font_style)
        self.screen.place(x=0, y=40)
        # --------------------------------------------------------------------------------------------

        # buttons delete--------------------------------------------------------------
        Button(self.buttons_frame, text="C", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=self.clear).grid(row=0, column=0, columnspan=2, sticky=NSEW)

        Button(self.buttons_frame, text="←", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=self.delLast).grid(row=0, column=2, sticky=NSEW)

        # --------------------------------------------------------------------------------------------

        # buttons operators and equal-----------------------------------------------------------------
        Button(self.buttons_frame, text="\u00F7", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.operator("/"), width=6).grid(row=0, column=3, sticky=NSEW)
        Button(self.buttons_frame, text="\u00D7", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.operator("*")).grid(row=1, column=3, sticky=NSEW)
        Button(self.buttons_frame, text="-", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.operator("-")).grid(row=2, column=3, sticky=NSEW)
        Button(self.buttons_frame, text="+", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.operator("+")).grid(row=3, column=3, sticky=NSEW)

        Button(self.buttons_frame, text="=", bg=self.light_blue, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=self.equal).grid(row=4, column=2, columnspan=2, sticky=NSEW)
        # --------------------------------------------------------------------------------------------

        # buttons numbers and point-----------------------------------------------------------------------------
        Button(self.buttons_frame, text="7", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(7), width=6).grid(row=1, column=0, sticky=NSEW)
        Button(self.buttons_frame, text="8", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(8), width=6).grid(row=1, column=1, sticky=NSEW)
        Button(self.buttons_frame, text="9", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(9), width=6).grid(row=1, column=2, sticky=NSEW)
        Button(self.buttons_frame, text="4", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(4)).grid(row=2, column=0, sticky=NSEW)
        Button(self.buttons_frame, text="5", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(5)).grid(row=2, column=1, sticky=NSEW)
        Button(self.buttons_frame, text="6", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(6)).grid(row=2, column=2, sticky=NSEW)
        Button(self.buttons_frame, text="1", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(1)).grid(row=3, column=0, sticky=NSEW)
        Button(self.buttons_frame, text="2", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(2)).grid(row=3, column=1, sticky=NSEW)
        Button(self.buttons_frame, text="3", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(3)).grid(row=3, column=2, sticky=NSEW)
        Button(self.buttons_frame, text="0", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=lambda: self.number(0)).grid(row=4, column=1, sticky=NSEW)

        Button(self.buttons_frame, text=".", bg=self.off_white, fg=self.label_color, font=self.default_font_style,
               borderwidth=0, command=self.point).grid(row=4, column=0, sticky=NSEW)
        # --------------------------------------------------------------------------------------------

        self.active_keyboard()

    def active_keyboard(self):
        self.app.bind('<Return>', lambda e: self.equal())

        self.app.bind('0', lambda n: self.number(0))
        self.app.bind('1', lambda n: self.number(1))
        self.app.bind('2', lambda n: self.number(2))
        self.app.bind('3', lambda n: self.number(3))
        self.app.bind('4', lambda n: self.number(4))
        self.app.bind('5', lambda n: self.number(5))
        self.app.bind('6', lambda n: self.number(6))
        self.app.bind('7', lambda n: self.number(7))
        self.app.bind('8', lambda n: self.number(8))
        self.app.bind('9', lambda n: self.number(9))

        self.app.bind('.', lambda n: self.point())

        self.app.bind('+', lambda n: self.operator("+"))
        self.app.bind('-', lambda n: self.operator("-"))
        self.app.bind('*', lambda n: self.operator("*"))
        self.app.bind('/', lambda n: self.operator("/"))

        #self.app.bind('Backspace', lambda n: self.delLast())

    def clear(self):
        self.screen.config(text="")
        self.expression = ""

    def operator(self, op):
        if len(self.expression) == 19:
            return None
        list_op = ['+', '-', '*', '/']
        if len(self.expression) >= 1:
            if self.expression[-1] in list_op:
                self.expression = self.expression[:-1] + op
            else:
                self.expression += op
            self.update_screen()

    def number(self, nb):
        if len(self.expression) == 19:
            return None
        self.expression += str(nb)
        self.update_screen()

    def point(self):
        if len(self.expression) == 19:
            return None
        if len(self.expression) >= 1:
            if self.expression[-1] != '.':
                self.expression = self.expression + '.'
            self.update_screen()

    def delLast(self):
        self.expression = self.expression[:-1]
        self.update_screen()

    def equal(self):
        if self.expression == '0000':
            self.app.destroy()  # close calculator
            return Secret_interface()
        if len(self.expression) >= 1:
            try:
                result = eval(self.expression)
                # test for delete '.0'
                if result % 1 == 0:
                    result = int(result)
                self.expression = str(result)
                self.update_screen()
            except Exception:
                self.screen.config(text='Error')
                self.expression = ''

    def update_screen(self):
        self.screen.config(text=self.expression)

    def loop(self):
        self.app.mainloop()


#a = Gallery('driss_25')
# a.loop()
#a = Secret_interface()
# a.loop()
Calculator().loop()
