import pandas as pd
from glob import glob
import os
import tkinter as tk
import csv

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
        
        path = os.path.join("Attendance", Subject)
        filenames = glob(os.path.join(path, f"{Subject}*.csv"))
        
        if not filenames:
            t = 'No attendance files found for the subject.'
            text_to_speech(t)
            return
        
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        
        # Initialize the Attendance column as string type
        newdf["Attendance"] = ""
        
        for i in range(len(newdf)):
            percentage = int(round(newdf.iloc[i, 2:-1].mean() * 100))
            newdf.at[i, "Attendance"] = f"{percentage}%"
        
        newdf.to_csv(os.path.join(path, "attendance.csv"), index=False)

        root = tk.Tk()
        root.title(f"Attendance of {Subject}")
        root.configure(background="black")
        cs = os.path.join(path, "attendance.csv")
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = tk.Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=row,
                        relief=tk.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()

    subject = tk.Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    
    titl = tk.Label(subject, bg="black", relief=tk.RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=tk.X)
    
    titl = tk.Label(
        subject,
        text="SUBJECT OF ATTENDANCE",
        bg="black",
        fg="cyan",
        font=("arial", 25),
    )
    titl.place(x=80, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(os.path.join("Attendance", sub))

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=tk.RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=tk.RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=tk.RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=tk.RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()
