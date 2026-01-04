import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os

patients, appointments, discharged = [], [], []
files = {"patients":"patients.txt", "appointments":"appointments.txt", "discharged":"discharged.txt"}

def load_records():
    for key, fname in files.items():
        if os.path.exists(fname):
            with open(fname) as f:
                for line in f:
                    parts = line.strip().split()
                    if key == "patients":
                        patients.append({"name":parts[0], "age":int(parts[1]), "disease":parts[2]})
                    elif key == "appointments":
                        appointments.append({"id":int(parts[0]), "doctor":parts[1]})
                    elif key == "discharged":
                        discharged.append({"name":parts[0]})

def save_record(key, data):
    with open(files[key], "a") as f:
        if key=="patients":
            f.write(f"{data['name']} {data['age']} {data['disease']}\n")
        elif key=="appointments":
            f.write(f"{data['id']} {data['doctor']}\n")
        elif key=="discharged":
            f.write(f"{data['name']}\n")

def display_list(treeview, data, cols, ref_list=None):
    for row in treeview.get_children(): treeview.delete(row)
    for idx, d in enumerate(data):
        if ref_list:
            treeview.insert("",tk.END,values=(d["id"], ref_list[d["id"]]["name"], d["doctor"]))
        else:
            values = [idx,d["name"],d.get("age",""),d.get("disease","")] if len(cols)>1 else [d["name"]]
            treeview.insert("",tk.END,values=values)

def open_add_patient():
    win = tk.Toplevel(root)
    win.title("Add Patient")

    tk.Label(win,text="Name:").grid(row=0,column=0)
    entry_name = tk.Entry(win); entry_name.grid(row=0,column=1)
    tk.Label(win,text="Age:").grid(row=1,column=0)
    entry_age = tk.Entry(win); entry_age.grid(row=1,column=1)
    tk.Label(win,text="Disease:").grid(row=2,column=0)
    entry_disease = tk.Entry(win); entry_disease.grid(row=2,column=1)

    def add_patient():
        name, age, disease = entry_name.get(), entry_age.get(), entry_disease.get()
        if not name or not age or not disease:
            return messagebox.showwarning("Warning","All fields required")
        p = {"name":name,"age":int(age),"disease":disease}
        patients.append(p)
        save_record("patients",p)
        messagebox.showinfo("Success","Patient added successfully")
        win.destroy()

    tk.Button(win,text="Add Patient",command=add_patient).grid(row=3,column=0,columnspan=2,pady=5)

def open_view_patients():
    win = tk.Toplevel(root); win.title("View Patients")
    tree = ttk.Treeview(win,columns=["ID","Name","Age","Disease"],show="headings")
    for c in ["ID","Name","Age","Disease"]: tree.heading(c,text=c); tree.column(c,width=100)
    tree.pack(padx=10,pady=10)
    display_list(tree, patients, ["ID","Name","Age","Disease"])

def open_book_appointment():
    if not patients:
        return messagebox.showwarning("Warning","No patients available to book appointment.")
    win = tk.Toplevel(root); win.title("Book Appointment")

    tk.Label(win,text="Patient ID (0-indexed):").grid(row=0,column=0)
    entry_pid = tk.Entry(win); entry_pid.grid(row=0,column=1)
    tk.Label(win,text="Doctor Name:").grid(row=1,column=0)
    entry_doctor = tk.Entry(win); entry_doctor.grid(row=1,column=1)

    def book_appointment():
        try:
            pid = int(entry_pid.get())
            if pid < 0 or pid >= len(patients):
                return messagebox.showerror("Error","Invalid Patient ID")
        except:
            return messagebox.showerror("Error","Enter a valid Patient ID")
        doctor = entry_doctor.get()
        if not doctor: return messagebox.showwarning("Warning","Doctor name required")
        a = {"id":pid,"doctor":doctor}
        appointments.append(a)
        save_record("appointments",a)
        messagebox.showinfo("Success",f"Appointment booked for {patients[pid]['name']} with Dr.{doctor}")
        win.destroy()

    tk.Button(win,text="Book Appointment",command=book_appointment).grid(row=2,column=0,columnspan=2,pady=5)

def open_view_appointments():
    win = tk.Toplevel(root); win.title("View Appointments")
    tree = ttk.Treeview(win,columns=["Patient ID","Patient Name","Doctor"],show="headings")
    for c in ["Patient ID","Patient Name","Doctor"]: tree.heading(c,text=c); tree.column(c,width=100)
    tree.pack(padx=10,pady=10)
    display_list(tree, appointments, ["Patient ID","Patient Name","Doctor"], patients)

def open_complete_appointment():
    if not appointments:
        return messagebox.showinfo("Info","No appointments to complete")
    a = appointments.pop(0)
    d = {"name":patients[a["id"]]["name"]}
    discharged.append(d)
    save_record("discharged",d)
    with open(files["appointments"],"w") as f:
        for ap in appointments:
            f.write(f"{ap['id']} {ap['doctor']}\n")
    messagebox.showinfo("Success",f"Patient {d['name']} discharged")

def open_view_discharged():
    win = tk.Toplevel(root); win.title("Discharged Patients")
    tree = ttk.Treeview(win,columns=["Name"],show="headings")
    tree.heading("Name",text="Name"); tree.column("Name",width=150)
    tree.pack(padx=10,pady=10)
    display_list(tree, discharged, ["Name"])

def open_search_patient():
    win = tk.Toplevel(root); win.title("Search Patient")
    pname = simpledialog.askstring("Patient Name","Enter patient name",parent=win)
    if not pname: return
    results = [p for p in patients if p["name"].lower()==pname.lower()]
    if not results:
        return messagebox.showinfo("Not Found",f"No patient named {pname}",parent=win)
    tree = ttk.Treeview(win,columns=["ID","Name","Age","Disease"],show="headings")
    for c in ["ID","Name","Age","Disease"]: tree.heading(c,text=c); tree.column(c,width=100)
    tree.pack(padx=10,pady=10)
    display_list(tree, results, ["ID","Name","Age","Disease"])

def open_search_doctor():
    win = tk.Toplevel(root); win.title("Search Doctor")
    doctor = simpledialog.askstring("Doctor Name","Enter doctor name",parent=win)
    if not doctor: return
    results = [a for a in appointments if a["doctor"].lower()==doctor.lower()]
    if not results:
        return messagebox.showinfo("Not Found",f"No patients under Dr.{doctor}",parent=win)
    tree = ttk.Treeview(win,columns=["Patient ID","Patient Name","Doctor"],show="headings")
    for c in ["Patient ID","Patient Name","Doctor"]: tree.heading(c,text=c); tree.column(c,width=100)
    tree.pack(padx=10,pady=10)
    display_list(tree, results, ["Patient ID","Patient Name","Doctor"], patients)

root = tk.Tk()
root.title("Hospital Management")
tk.Label(root,text="HOSPITAL MANAGEMENT SYSTEM",font=("Arial",16)).pack(pady=10)

btn_frame = tk.Frame(root); btn_frame.pack(pady=20)

tk.Button(btn_frame,text="Add Patient",width=25,command=open_add_patient).grid(row=0,column=0,padx=10,pady=5)
tk.Button(btn_frame,text="View Patients",width=25,command=open_view_patients).grid(row=1,column=0,padx=10,pady=5)
tk.Button(btn_frame,text="Book Appointment",width=25,command=open_book_appointment).grid(row=2,column=0,padx=10,pady=5)
tk.Button(btn_frame,text="View Appointments",width=25,command=open_view_appointments).grid(row=3,column=0,padx=10,pady=5)
tk.Button(btn_frame,text="Complete Appointment",width=25,command=open_complete_appointment).grid(row=4,column=0,padx=10,pady=5)
tk.Button(btn_frame,text="View Discharged Patients",width=25,command=open_view_discharged).grid(row=5,column=0,padx=10,pady=5)
tk.Button(btn_frame,text="Search Patient by Name",width=25,command=open_search_patient).grid(row=6,column=0,padx=10,pady=5)
tk.Button(btn_frame,text="Search Patient by Doctor",width=25,command=open_search_doctor).grid(row=7,column=0,padx=10,pady=5)

load_records()
root.mainloop()