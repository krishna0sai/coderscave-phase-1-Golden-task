import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime, timedelta

class App(tk.Tk):
    def __init__(self,):
        super().__init__()

        self.title("Medical Appointment Scheduler")
        self.geometry("800x600")

        self.patient_records = {}

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.patient_name_label = ttk.Label(self, text="Patient Name:")
        self.patient_name_entry = ttk.Entry(self)

        self.patient_email_label = ttk.Label(self, text="Patient Email:")
        self.patient_email_entry = ttk.Entry(self)

        self.create_patient_button = ttk.Button(self, text="Create Patient", command=self.create_patient)

        self.appointment_date_label = ttk.Label(self, text="Appointment Date: [d-m-y]")
        self.appointment_date_entry = ttk.Entry(self)

        self.appointment_time_label = ttk.Label(self, text="Appointment Time: [H:M] ")
        self.appointment_time_entry = ttk.Entry(self)

        self.schedule_appointment_button = ttk.Button(self, text="Schedule Appointment", command=self.schedule_appointment)

        self.patient_records_tree = ttk.Treeview(self, columns=("Name", "Email", "Appointments"), show="headings")
        self.patient_records_tree.heading("Name", text="Name")
        self.patient_records_tree.heading("Email", text="Email")
        self.patient_records_tree.heading("Appointments", text="Appointments")

        self.send_reminder_button = ttk.Button(self, text="Send Reminder", command=self.send_reminder)

    def create_layout(self):
        self.patient_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.patient_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.patient_email_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.patient_email_entry.grid(row=1, column=1, padx=10, pady=10)

        self.create_patient_button.grid(row=2, column=0, padx=10, pady=10)

        self.appointment_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.appointment_date_entry.grid(row=3, column=1, padx=10, pady=10)

        self.appointment_time_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.appointment_time_entry.grid(row=4, column=1, padx=10, pady=10)

        self.schedule_appointment_button.grid(row=5, column=0, padx=10, pady=10)

        self.patient_records_tree.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

        self.send_reminder_button.grid(row=6, column=0, padx=10, pady=10)

    def create_patient(self):
        name = self.patient_name_entry.get()
        email = self.patient_email_entry.get()

        if not name:
            print("Error: Patient name cannot be empty.")
            return

        if not email:
            print("Error: Patient email cannot be empty.")
            return

        if email not in self.patient_records:
            try:
                self.patient_records[email] = PatientRecord(name, email)
                self.update_patient_records_tree()
            except Exception as e:
                print(f"Error: Failed to create patient record. {e}")
                return

    def schedule_appointment(self):
        email = self.patient_email_entry.get()
        date_str = self.appointment_date_entry.get()
        time_str = self.appointment_time_entry.get()

        if not email:
            print("Error: Patient email cannot be empty.")
            return

        if not date_str:
            print("Error: Appointment date cannot be empty.")
            return

        if not time_str:
            print("Error: Appointment time cannot be empty.")
            return

        try:
            date = datetime.strptime(date_str, "%d-%m-%Y")
            time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            print("Error: Invalid date or time format. Please use DD-MM-YYYY for date and HH:MM for time.")
            return

        if email in self.patient_records:
            appointment = Appointment(date, time)
            self.patient_records[email].schedule_appointment(appointment)
            self.update_patient_records_tree()
        else:
            print("Error: Patient not found.")

    def send_reminder(self):
        email = self.patient_email_entry.get()

        if not email:
            print("Error: Patient email cannot be empty.")
            return

        if email in self.patient_records:
            self.patient_records[email].send_reminder()
        else:
            print("Error: Patient not found.")
    def display_reminders(self, email):
        if email in self.patient_records:
            reminders_text = "\n".join(f"{reminder.date.date()} at {reminder.time.strftime('%H:%M')}" for reminder in self.patient_records[email].appointments)
            self.reminder_text.delete(1.0, tk.END)
            self.reminder_text.insert(tk.END, reminders_text)
        else:
            print("Error: Patient not found.")

    def update_patient_records_tree(self):
        self.patient_records_tree.delete(*self.patient_records_tree.get_children())

        for email, patient_record in self.patient_records.items():
            appointments = [f"{appointment.date.date()} {appointment.time.strftime('%H:%M')}" for appointment in patient_record.appointments]
            self.patient_records_tree.insert("", "end", values=(patient_record.name, email, ", ".join(appointments)))

class PatientRecord:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.appointments = []

    def schedule_appointment(self, appointment):
        self.appointments.append(appointment)

    def send_reminder(self):
        for appointment in self.appointments:
            messagebox.showinfo("Remainder",f"Reminder for {self.name}: {appointment.date.date()} at {appointment.time.strftime('%H:%M')}")

class Appointment:
    def __init__(self, date, time):
        self.date = date
        self.time = time

if __name__ == "__main__":
    app = App()
    app.mainloop()