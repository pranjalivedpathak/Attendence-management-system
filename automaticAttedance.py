import tkinter as tk
from tkinter import *
import os
import cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join("TrainingImageLabel", "Trainner.yml")
trainimage_path = "TrainingImage"
studentdetail_path = os.path.join("StudentDetails", "studentdetails.csv")
attendance_path = "Attendance"

def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get().strip()
        now = time.time()
        future = now + 20
        
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                if not os.path.exists(trainimagelabel_path):
                    raise FileNotFoundError("Model not found, please train the model.")

                recognizer.read(trainimagelabel_path)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)

                while time.time() <= future:
                    ret, im = cam.read()
                    if not ret:
                        print("Failed to grab frame")
                        break
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                    for (x, y, w, h) in faces:
                        Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                        if conf < 70:
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values[0]
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [Id, aa]
                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.putText(im, str(tt), (x + w, y), font, 1, (255, 255, 255), 2)
                        else:
                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 0, 255), 2)
                            cv2.putText(im, "Unknown", (x + w, y), font, 1, (0, 0, 255), 2)

                    attendance.drop_duplicates(subset="Enrollment", inplace=True)
                    cv2.imshow("Filling Attendance...", im)
                    if cv2.waitKey(30) & 0xFF == 27:
                        break

                # Saving Attendance
                date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime("%H-%M-%S")
                attendance[date] = 1

                path = os.path.join(attendance_path, sub)
                os.makedirs(path, exist_ok=True)
                fileName = os.path.join(path, f"{sub}_{date}_{timeStamp}.csv")
                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully for " + sub
                Notifica.configure(text=m, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
                text_to_speech(m)
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                # Display Attendance in a Tkinter window
                root = tk.Tk()
                root.title("Attendance of " + sub)
                root.configure(background="black")

                with open(fileName, newline="") as file:
                    reader = csv.reader(file)
                    for r, row in enumerate(reader):
                        for c, col in enumerate(row):
                            label = tk.Label(root, width=10, height=1, fg="yellow", font=("times", 15, " bold "), bg="black", text=col, relief=tk.RIDGE)
                            label.grid(row=r, column=c)
                root.mainloop()

            except FileNotFoundError as fnf_error:
                text_to_speech(str(fnf_error))
                Notifica.configure(text=str(fnf_error), bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                cam.release()
                cv2.destroyAllWindows()
            except Exception as e:
                text_to_speech(str(e))
                Notifica.configure(text="No Face found for attendance", bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                cam.release()
                cv2.destroyAllWindows()

    subject = tk.Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = tk.Label(subject, bg="black", relief=tk.RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=tk.X)

    titl = tk.Label(subject, text="ENTER THE SUBJECT", bg="black", fg="cyan", font=("arial", 25))
    titl.place(x=140, y=12)

    Notifica = tk.Label(subject, text="Attendance filled Successfully", bg="yellow", fg="black", width=33, height=2, font=("times", 15, "bold"))

    def Attf():
        sub = tx.get().strip()
        if sub == "":
            text_to_speech("Please enter the subject name!")
        else:
            os.startfile(os.path.join(attendance_path, sub))

    attf = tk.Button(subject, text="Check Sheets", command=Attf, bd=7, font=("times new roman", 15), bg="black", fg="yellow", height=2, width=10, relief=tk.RIDGE)
    attf.place(x=360, y=170)

    sub = tk.Label(subject, text="Enter Subject", width=10, height=2, bg="black", fg="yellow", bd=5, relief=tk.RIDGE, font=("times new roman", 15))
    sub.place(x=50, y=100)

    tx = tk.Entry(subject, width=15, bd=5, bg="black", fg="yellow", relief=tk.RIDGE, font=("times", 30, "bold"))
    tx.place(x=190, y=100)

    fill_a = tk.Button(subject, text="Fill Attendance", command=FillAttendance, bd=7, font=("times new roman", 15), bg="black", fg="yellow", height=2, width=12, relief=tk.RIDGE)
    fill_a.place(x=195, y=170)

    subject.mainloop()
