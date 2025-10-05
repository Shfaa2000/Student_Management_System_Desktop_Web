from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from students_models import StudentModel, session, create_tables
from sqlalchemy import func, cast, String, or_
from sqlalchemy.exc import IntegrityError
import re

class Student:
    # create the window of the programme
    def __init__(self, root):
        self.root = root
        # to take the fill of screen
        self.root.geometry('1350x690+1+1')
        self.root.title('Students Management Programme')
        self.root.configure(background='silver')
        create_tables()
        # not increse or decrese the screen
        self.root.resizable(False, False)
        title = Label(
        self.root,
        text="Student Registration System",
        bg="#24659C",
        font=("monospace", 14, "bold"),
        fg="white",
        justify='center'
        )
        title.pack(fill=X, ipady=20)  # ipady لزيادة الارتفاع الداخلي

        # variables as the number of entery
        self.id_var = StringVar()
        self.name_var = StringVar()
        self.email_var = StringVar()
        self.phone_var = StringVar()
        self.certi_var = StringVar()
        self.gender_var = StringVar()
        self.address_var = StringVar()
        self.search_var = StringVar()
        self.delete_var = StringVar()

        # Search Manage
        Search_Frame = Frame(self.root, bg="white")
        Search_Frame.place(x=1137, y=70, width=210, height=400)
        lbl_search = Label(Search_Frame, text="Search Student", bg='white')
        lbl_search.place(x=40, y=10, width=150, height=30)
        search_Entry = Entry(Search_Frame, textvariable=self.search_var, justify='left', bd='2')
        search_Entry.place(x=40, y=40, width=150, height=30)
        # to work directly while writing
        search_Entry.bind("<KeyRelease>", self.search_student)
        lbl_delete = Label(Search_Frame, text="Delete By Name or ID", bg='white', fg='red')
        lbl_delete.place(x=40, y=70, width=150, height=30)
        delete_Entry = Entry(Search_Frame, textvariable=self.delete_var, bd='2', justify='center')
        delete_Entry.place(x=40, y=100, width=150, height=30)

        # buttons
        button_Frame = Frame(self.root, bg='white')
        button_Frame.place(x=1137, y=300, width=210, height=400)
        title1 = Label(button_Frame, text='Control Board', font=("Deco", 14), fg='white', bg='#24659C')
        title1.pack(fill=X)

        add_button = Button(button_Frame, text='Add Student', bg='#42c6ff', command=self.show_add_window)
        add_button.place(x=33, y=50, width=150, height=30)
        delete_button = Button(button_Frame, text='Delete Student', bg='#42c6ff', command=self.delete_student)
        delete_button.place(x=33, y=85, width=150, height=30)
        about_button = Button(button_Frame, text='About Us', bg='#42c6ff', command=self.show_about)
        about_button.place(x=33, y=120, width=150, height=30)
        # you can use root.quit to close the programme without asking
        exit_button = Button(button_Frame, text='Exit', bg='#42c6ff', command=self.exit)
        exit_button.place(x=33, y=155, width=150, height=30)

        # show details
        details_Frame = Frame(self.root, bg='white')
        details_Frame.place(x=1, y=70, width=1134, height=620)
        # scroll
        scroll_x = Scrollbar(details_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(details_Frame, orient=VERTICAL)
        # treeview
        self.student_table = ttk.Treeview(details_Frame, columns=('Address',
                                        'Gender', 'Certification', 'Phone', 'Email', 'Name', 'ID' ),
                                        xscrollcommand=scroll_x.set,
                                        yscrollcommand=scroll_y.set)
        self.student_table.place(x=15, y=1, width=1115, height=600)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=LEFT, fill=Y)
        # if also no scrolling
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table['show'] = 'headings'
        self.student_table.heading('Address', text='Student Address')
        self.student_table.heading('Gender', text='Student Gender')
        self.student_table.heading('Certification', text='Certification')
        self.student_table.heading('Phone', text='Student Phone')
        self.student_table.heading('Email', text='Student Email')
        self.student_table.heading('Name', text='Student Name')
        self.student_table.heading('ID', text='Student ID')
        # control the size of columns
        self.student_table.column('Address', width=130, anchor="center")
        self.student_table.column('Gender', width=30, anchor="center")
        self.student_table.column('Certification', width=65, anchor="center")
        self.student_table.column('Phone', width=65, anchor="center")
        self.student_table.column('Email', width=70, anchor="center")
        self.student_table.column('Name', width=100, anchor="center")
        self.student_table.column('ID', width=15, anchor="center")
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.student_table.bind("<Double-1>", self.show_update_window)

        self.student_table.tag_configure("hover", background="#a2cef7")
        self.student_table.tag_configure("odd", background="white")
        self.student_table.tag_configure("even", background="#f5f5f5")
        self.last_hovered = None
        self.last_hovered_prev_tags = ("normal",)

        self.student_table.bind("<Motion>", self.row_on_hover)
        self.student_table.bind("<Leave>", self.row_on_leave)

        self.fetch_data()
    def fetch_data(self):
        data=session.query(StudentModel).all()
        self.student_table.delete(*self.student_table.get_children())
        for idx,student in enumerate(data):
            base_tag = "odd" if idx%2 == 0 else "even"
            self.student_table.insert('','end', values=(
                student.address,student.gender, student.certification, student.phone, student.email, student.name, student.id), tags=(base_tag))
            
    def delete_student(self):
        toDelete = self.delete_var.get().strip()
        if not toDelete:
            messagebox.showwarning("Warring","Please Write The ID or Name of Student")
            return
        students = session.query(StudentModel).filter(or_(StudentModel.name.ilike(f"%{toDelete}%"),
                                                    cast(StudentModel.id, String).ilike(f"%{toDelete}%"))).all()
        if not students:
            messagebox.showwarning("Warring","No Student in this ID or Name")
            return
        for student in students:
            session.delete(student)
            session.commit()
            self.fetch_data()
        self.delete_var.set("")
    
    def show_about(self):
        messagebox.showinfo("About Us", "Student Management System v1.0\n\nDeveloped by: [Shfaa]" \
        "\nEmail: nakourshfaa@email.com\n\nThis app helps manage student data easily using Python, tkinter and SQLAlchemy." \
        "also this Database store students from my webpage that developed by pywebio")

    def exit(self):
        confirm = messagebox.askyesno("Exit", "Are yoy sure you want to exit?")
        if confirm:
            self.root.destroy()
    
    def search_student(self, event=None):
        search_text = self.search_var.get().strip()

        for s in self.student_table.get_children():
            self.student_table.delete(s)

        if not search_text:
            self.fetch_data()
            return

        else:
            results = session.query(StudentModel).filter(or_(StudentModel.name.ilike(f"%{search_text}%"),
                                                    StudentModel.email.ilike(f"%{search_text}%"),
                                                    StudentModel.address.ilike(f"%{search_text}%"),
                                                    cast(StudentModel.id, String).ilike(f"%{search_text}%"))).all()

            print(results)
            for student in results:
                self.student_table.insert("","end", values=(
                student.address, student.gender, student.certification, student.phone, student.email, student.name, student.id
            ))
        
    def get_cursor(self, details):
        cursor_row = self.student_table.focus()
        informaition = self.student_table.item(cursor_row)
        row = informaition['values']
        self.id_var.set(row[6])
        self.name_var.set(row[5])
        self.email_var.set(row[4])
        self.phone_var.set(row[3])
        self.certi_var.set(row[2])
        self.gender_var.set(row[1])
        self.address_var.set(row[0])
    
    def clear_fields(self):
            self.name_var.set("")
            self.email_var.set("")
            self.phone_var.set("")
            self.certi_var.set("")
            self.gender_var.set("")
            self.address_var.set("")
    
    def show_add_window(self):
        self.clear_fields()
        add_Frame = Toplevel(self.root, bg="white")
        add_Frame.title("Add New Student")
        add_Frame.resizable(False, False)
        add_Frame.grab_set()
        min_width = 400
        min_height = 500
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        pos_x = root_x + (root_width // 2) - (min_width // 2)
        pos_y = root_y + (root_height // 2) - (min_height // 2)
        add_Frame.geometry(f"{min_width}x{min_height}+{pos_x}+{pos_y}")

        add_Frame.focus_force()
        add_Frame.protocol("WM_DELETE_WINDOW", lambda: None)

        last_student = session.query(StudentModel).order_by(StudentModel.id.desc()).first()
        if last_student:
            next_id = last_student.id + 1
        else:
            next_id = 1

        id_var = StringVar(value=str(next_id))
        print(type(id_var))

        lbl_ID = Label(add_Frame, text="Student ID", bg='white')
        lbl_ID.pack()
        ID_Entry = Entry(add_Frame, textvariable=id_var, bd='2', justify='center')
        ID_Entry.pack()
        ID_Entry.bind("<Return>", lambda e:name_Entry.focus())

        lbl_name = Label(add_Frame, text="Student Name", bg='white')
        lbl_name.pack()
        name_Entry = Entry(add_Frame, textvariable=self.name_var, bd='2', justify='center')
        name_Entry.pack()
        name_Entry.bind("<Return>", lambda e:email_Entry.focus())

        lbl_email = Label(add_Frame, text="Student Email", bg='white')
        lbl_email.pack()
        email_Entry = Entry(add_Frame, textvariable=self.email_var, bd='2', justify='center')
        email_Entry.pack()
        email_Entry.bind("<Return>", lambda e:phone_Entry.focus())

        lbl_Phone = Label(add_Frame, text="Student Phone", bg='white')
        lbl_Phone.pack()
        phone_Entry = Entry(add_Frame, textvariable=self.phone_var, bd='2', justify='center')
        phone_Entry.pack()
        phone_Entry.bind("<Return>", lambda e:cetri_Entry.focus())

        lbl_cetri = Label(add_Frame, text="Student cetrificatition", bg='white')
        lbl_cetri.pack()
        cetri_Entry = ttk.Combobox(add_Frame, textvariable=self.certi_var, justify='center')
        cetri_Entry['value']= ("Word", "Excel", "Powerpoint")
        cetri_Entry.pack()
        cetri_Entry.bind("<Return>", lambda e:Gender_Compo.focus())

        lbl_gender = Label(add_Frame, text="Student Gender", bg='white')
        lbl_gender.pack()
        Gender_Compo = ttk.Combobox(add_Frame, textvariable=self.gender_var, justify='center')
        Gender_Compo['value']= ("Male", "Female")
        Gender_Compo.pack()

        lbl_address = Label(add_Frame, text="Student Address", bg='white')
        lbl_address.pack()
        address_Entry = Entry(add_Frame, textvariable=self.address_var, bd='2', justify='center')
        address_Entry.pack()
        address_Entry.bind("<Return>", lambda e:confirm().focus())

        def confirm():
            email_value = self.email_var.get().strip()
            phone_value = self.phone_var.get().strip()
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern,email_value):
                messagebox.showerror("Invalid Email, Please Enter a valid Email")
                return
            if not re.match(r'^\+?\d{8,15}$', phone_value):
                messagebox.showerror("Invalid Phone", "Phone must be 8-15 digits only.")
                return
            try:
                student = StudentModel(id=int(id_var.get()),
                                name=self.name_var.get(),
                                email=self.email_var.get(),
                                phone=self.phone_var.get(),
                                certification=self.certi_var.get(),
                                gender=self.gender_var.get(),
                                address=self.address_var.get())
                session.add(student)
                session.commit()
                self.fetch_data()
                messagebox.showinfo("Success", "Student added successfully")
            except Exception as e:
                messagebox.showinfo("Error", f"Faild to add student: \n {e}")
            add_Frame.destroy()
        def cancel():
            add_Frame.destroy()
        Button(add_Frame, text='Confirm', bg='green', fg='white', command=confirm).pack(padx=5,pady=10)
        Button(add_Frame, text='Cancel', bg='red', fg='white', command=cancel).pack(padx=15, pady=10)

    def show_update_window(self, event):
        Update_Frame = Toplevel(self.root, bg="white")
        Update_Frame.title("Update Student")
        Update_Frame.resizable(False, False)
        Update_Frame.grab_set()
        min_width = 400
        min_height = 500
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        pos_x = root_x + (root_width // 2) - (min_width // 2)
        pos_y = root_y + (root_height // 2) - (min_height // 2)
        Update_Frame.geometry(f"{min_width}x{min_height}+{pos_x}+{pos_y}")

        def validate_email(*args):
            email_value = self.email_var.get().strip()
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_pattern,email_value):
                email_Entry.config(bg='lightgreen')
            else:
                email_Entry.config(bg='lightcoral')
        def validate_phone(*args):
            phone_value = self.phone_var.get().strip()
            if re.match(r'^\+?\d{8,15}$', phone_value):
                phone_Entry.config(bg='lightgreen')
            else:
                phone_Entry.config(bg='lightcoral')
        lbl_ID = Label(Update_Frame, text="Student ID", bg='white')
        lbl_ID.pack()
        ID_Entry = Entry(Update_Frame, textvariable=self.id_var, bd='2', justify='center', state="readonly")
        ID_Entry.pack()
        ID_Entry.bind("<Return>", lambda e:name_Entry.focus())

        lbl_name = Label(Update_Frame, text="Student Name", bg='white')
        lbl_name.pack()
        name_Entry = Entry(Update_Frame, textvariable=self.name_var, bd='2', justify='center')
        name_Entry.pack()
        name_Entry.bind("<Return>", lambda e:email_Entry.focus())

        lbl_email = Label(Update_Frame, text="Student Email", bg='white')
        lbl_email.pack()
        email_Entry = Entry(Update_Frame, textvariable=self.email_var, bd='2', justify='center')
        email_Entry.pack()
        self.email_var.trace_add('write',validate_email)
        email_Entry.bind("<Return>", lambda e:phone_Entry.focus())

        lbl_Phone = Label(Update_Frame, text="Student Phone", bg='white')
        lbl_Phone.pack()
        phone_Entry = Entry(Update_Frame, textvariable=self.phone_var, bd='2', justify='center')
        phone_Entry.pack()
        self.phone_var.trace_add('write',validate_phone)
        phone_Entry.bind("<Return>", lambda e:cetri_Entry.focus())

        lbl_cetri = Label(Update_Frame, text="Student cetrificatition", bg='white')
        lbl_cetri.pack()
        cetri_Entry = Entry(Update_Frame, textvariable=self.certi_var, bd='2', justify='center')
        cetri_Entry.pack()
        cetri_Entry.bind("<Return>", lambda e:Gender_Compo.focus())

        lbl_gender = Label(Update_Frame, text="Student Gender", bg='white')
        lbl_gender.pack()
        Gender_Compo = ttk.Combobox(Update_Frame, textvariable=self.gender_var, justify='center')
        Gender_Compo['value']= ("Male", "Female")
        Gender_Compo.pack()
        Gender_Compo.bind("<Return>", lambda e:address_Entry.focus())

        lbl_address = Label(Update_Frame, text="Student Address", bg='white')
        lbl_address.pack()
        address_Entry = Entry(Update_Frame, textvariable=self.address_var, bd='2', justify='center')
        address_Entry.pack()
        address_Entry.bind("<Return>", lambda e:confirm().focus())

        def confirm():
            try:
                student_id = int(self.id_var.get())
            except Exception as e:
                messagebox.showinfo("Error", f"Faild to add student: \n {e}")
            student = session.query(StudentModel).filter(StudentModel.id == student_id).first()
            if not student:
                print("No Student")
                return
            student.name = self.name_var.get()
            student.email = self.email_var.get()
            student.phone = self.phone_var.get()
            student.certification = self.certi_var.get()
            student.gender = self.gender_var.get()
            student.address = self.address_var.get()
            session.commit()
            self.fetch_data()
            messagebox.showinfo("Success", "Student Updated successfully")
            Update_Frame.destroy()
        def cancel():
            Update_Frame.destroy()
        def clear_fields():
            self.name_var.set("")
            self.email_var.set("")
            self.phone_var.set("")
            self.certi_var.set("")
            self.gender_var.set("")
            self.address_var.set("")
        Button(Update_Frame, text='Confirm', bg='green', fg='white', command=confirm).pack(padx=5,pady=10)
        Button(Update_Frame, text='Clear', bg='red', fg='white', command=clear_fields).pack(padx=15, pady=10)
        Button(Update_Frame, text='Cancel', bg='red', fg='white', command=cancel).pack(padx=25, pady=10)
    
    def row_on_hover(self, event):
        row_id = self.student_table.identify_row(event.y)
        if row_id == self.last_hovered:
            return
        if self.last_hovered and self.student_table.exists(self.last_hovered):
            self.student_table.item(self.last_hovered, tags=self.last_hovered_prev_tags)
        if row_id:
            self.last_hovered_prev_tags = self.student_table.item(row_id, "tags") or ("normal",)
            self.student_table.item(row_id, tags=("hover"))
            self.last_hovered = row_id
        else:
            self.last_hovered = None
            self.last_hovered_prev_tags = ("normal",)
    def row_on_leave(self, event):
        if self.last_hovered and self.student_table.exists(self.last_hovered):
            self.student_table.item(self.last_hovered, tags=self.last_hovered_prev_tags)
            self.last_hovered = None
            self.last_hovered_prev_tags = ("normal",)


root = Tk()
ob = Student(root)
root.mainloop()