# ================= BACKEND (UNCHANGED LOGIC) =================

import mysql.connector
import tkinter as tk
from tkinter import messagebox

conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manapoli@123",
    database="curd_nov_2025_mini_project_db")

cur_obj = conn_obj.cursor()


def data_entry_sql(full_name, address, ph_number, user_id, password):
    sql = "INSERT INTO cust_details (full_name, address, ph_no, user_id, password) VALUES (%s, %s, %s, %s, %s)"
    data = (full_name, address, ph_number, user_id, password)
    try:
        cur_obj.execute(sql, data)
        conn_obj.commit()
        return True
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        return False


def data_retrieve(user_id_login):
    query = "select * from cust_details where user_id=%s"
    try:
        cur_obj.execute(query, (user_id_login,))
        result = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        result = None
    return result


def update_data(full_name, user_id):
    query = "Update cust_details set full_name=%s where user_id=%s"
    try:
        cur_obj.execute(query, (full_name, user_id))
        conn_obj.commit()
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))

    query1 = "select * from cust_details where user_id=%s"
    cur_obj.execute(query1, (user_id,))
    return cur_obj.fetchone()


def delete_data(user_id):
    query = "delete from cust_details where user_id=%s"
    try:
        cur_obj.execute(query, (user_id,))
        conn_obj.commit()
        return True
    except mysql.connector.Error as e:
        conn_obj.rollback()
        messagebox.showerror("Database Error", str(e))
        return False


# ================= FRONTEND (Tkinter UI) =================

root = tk.Tk()
root.title("Customer Login Application")
root.geometry("500x500")
root.resizable(False, False)

title_label = tk.Label(root, text="Customer Login System",
                       font=("Arial", 18, "bold"))
title_label.pack(pady=20)

frame = tk.Frame(root)
frame.pack(pady=10)


# ---------- Common Clear Function ----------
def clear_entries():
    for widget in frame.winfo_children():
        widget.destroy()


# ---------- Registration ----------
def show_register():
    clear_entries()

    tk.Label(frame, text="Full Name").grid(row=0, column=0, pady=5)
    tk.Label(frame, text="Address").grid(row=1, column=0, pady=5)
    tk.Label(frame, text="Phone Number").grid(row=2, column=0, pady=5)
    tk.Label(frame, text="User ID").grid(row=3, column=0, pady=5)
    tk.Label(frame, text="Password").grid(row=4, column=0, pady=5)

    full_name = tk.Entry(frame, width=30)
    address = tk.Entry(frame, width=30)
    phone = tk.Entry(frame, width=30)
    user_id = tk.Entry(frame, width=30)
    password = tk.Entry(frame, width=30, show="*")

    full_name.grid(row=0, column=1)
    address.grid(row=1, column=1)
    phone.grid(row=2, column=1)
    user_id.grid(row=3, column=1)
    password.grid(row=4, column=1)

    def register_action():
        result = data_retrieve(user_id.get())
        if result:
            messagebox.showwarning("Warning", "User ID already exists!")
        else:
            success = data_entry_sql(
                full_name.get().strip().upper(),
                address.get().strip().upper(),
                phone.get(),
                user_id.get(),
                password.get()
            )
            if success:
                messagebox.showinfo("Success", "Registration Successful!")

    tk.Button(frame, text="Register", width=20,
              command=register_action).grid(row=6, columnspan=2, pady=10)


# ---------- Login ----------
def show_login():
    clear_entries()

    tk.Label(frame, text="User ID").grid(row=0, column=0, pady=5)
    tk.Label(frame, text="Password").grid(row=1, column=0, pady=5)

    user_id = tk.Entry(frame, width=30)
    password = tk.Entry(frame, width=30, show="*")

    user_id.grid(row=0, column=1)
    password.grid(row=1, column=1)

    def login_action():
        result = data_retrieve(user_id.get())
        if result:
            if result[5] == password.get():
                details = "\n".join([str(i) for i in result])
                messagebox.showinfo("Access Granted", details)
            else:
                messagebox.showerror("Error", "Wrong Password")
        else:
            messagebox.showwarning("Warning", "User not found")

    tk.Button(frame, text="Login", width=20,
              command=login_action).grid(row=3, columnspan=2, pady=10)


# ---------- Update ----------
def show_update():
    clear_entries()

    tk.Label(frame, text="User ID").grid(row=0, column=0, pady=5)
    tk.Label(frame, text="Password").grid(row=1, column=0, pady=5)
    tk.Label(frame, text="New Full Name").grid(row=2, column=0, pady=5)

    user_id = tk.Entry(frame, width=30)
    password = tk.Entry(frame, width=30, show="*")
    new_name = tk.Entry(frame, width=30)

    user_id.grid(row=0, column=1)
    password.grid(row=1, column=1)
    new_name.grid(row=2, column=1)

    def update_action():
        result = data_retrieve(user_id.get())
        if result and result[5] == password.get():
            updated = update_data(new_name.get().strip().upper(),
                                  user_id.get())
            messagebox.showinfo("Success", "Details Updated Successfully")
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    tk.Button(frame, text="Update", width=20,
              command=update_action).grid(row=4, columnspan=2, pady=10)


# ---------- Delete ----------
def show_delete():
    clear_entries()

    tk.Label(frame, text="User ID").grid(row=0, column=0, pady=5)
    user_id = tk.Entry(frame, width=30)
    user_id.grid(row=0, column=1)

    def delete_action():
        success = delete_data(user_id.get())
        if success:
            messagebox.showinfo("Success", "User Deleted Successfully")

    tk.Button(frame, text="Delete", width=20,
              command=delete_action).grid(row=2, columnspan=2, pady=10)


# ---------- Main Buttons ----------
tk.Button(root, text="New User Registration",
          width=30, command=show_register).pack(pady=5)

tk.Button(root, text="Existing User Login",
          width=30, command=show_login).pack(pady=5)

tk.Button(root, text="Update User Data",
          width=30, command=show_update).pack(pady=5)

tk.Button(root, text="Delete User",
          width=30, command=show_delete).pack(pady=5)


# ---------- Close DB on Exit ----------
def on_closing():
    cur_obj.close()
    conn_obj.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()