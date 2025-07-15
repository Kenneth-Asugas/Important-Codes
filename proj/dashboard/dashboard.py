import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
import lms_backend as backend

# USER CONTEXT
role = sys.argv[1] if len(sys.argv) > 1 else "STUDENT"
user_id = sys.argv[2] if len(sys.argv) > 2 else "unknown"

#MAIN WINDOW
root = tk.Tk()
root.title("LMS Dashboard")
root.state("zoomed")
root.resizable(False, False)

base_path = os.path.join(os.path.dirname(__file__), '..', 'images')
images_folder = os.path.normpath(base_path)

# LOAD IMAGES
logo_ucc = Image.open(os.path.join(images_folder, "UCC.png")).resize((60, 60))
logo_coe = Image.open(os.path.join(images_folder, "COE.png")).resize((60, 60))
logo_ls = Image.open(os.path.join(images_folder, "LS.png")).resize((110, 70))
background_img_original = Image.open(os.path.join(images_folder, "BLURED LOGO COENGG.png"))

logo_ucc = ImageTk.PhotoImage(logo_ucc)
logo_coe = ImageTk.PhotoImage(logo_coe)
logo_ls = ImageTk.PhotoImage(logo_ls)

# HEADER
header = tk.Frame(root, bg="#0077c2", height=80)
header.pack(fill="x", side="top")
tk.Label(header, image=logo_ucc, bg="#0077c2").pack(side="left", pady=10)
tk.Label(header, image=logo_coe, bg="#0077c2").pack(side="left", pady=10)
tk.Label(header, image=logo_ls, bg="#0077c2").pack(side="left", pady=10)
title = tk.Label(header, text=f"{role.title()} Dashboard", font=("Orbitron", 24, "bold"), bg="#0077c2", fg="black")
title.pack(side="left", padx=20)
tk.Button(header, text="Logout", command=lambda: confirm_logout(), bg="red", fg="white", font=("Orbitron", 10, "bold")).pack(side="right", padx=20)

# MAIN BODY
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

sidebar = tk.Frame(main_frame, bg="#00bcd4", width=200)
sidebar.pack(side="left", fill="y")

content_frame = tk.Frame(main_frame)
content_frame.pack(side="left", fill="both", expand=True)

bg_label = tk.Label(content_frame)
bg_label.place(relx=0.5, rely=0.5, anchor="center")

def resize_bg(event):
    width = event.width
    height = event.height
    resized = background_img_original.resize((width, height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized)
    bg_label.configure(image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

content_frame.bind("<Configure>", resize_bg)

frames = {}

def create_frame(name):
    f = tk.Frame(content_frame, bg="#9edcff")
    frames[name] = f
    return f

def show_frame(name):
    for f in frames.values():
        f.place_forget()
    frames[name].place(relx=0.5, rely=0.5, anchor="center")

def confirm_logout():
    if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
        root.destroy()

# STUDENT VIEWS
def build_student_dashboard():
    home = create_frame("home")
    courses = create_frame("courses")
    assignments = create_frame("assignments")
    quizzes = create_frame("quizzes")

    tk.Label(home, text=f"Welcome, {user_id}!", font=("Orbitron", 18), bg="#9edcff").pack(pady=40)

    # Course List
    tk.Label(courses, text="Available Courses", font=("Orbitron", 18), bg="#9edcff").pack(pady=10)
    for c in backend.get_courses():
        row = tk.Frame(courses, bg="#9edcff")  # row background fixed
        row.pack(pady=5, fill="x")  # make row fill horizontally to avoid blank sides
        tk.Label(row, text=f"{c['name']} ({c['course_id']})", font=("Orbitron", 14), bg="#9edcff").pack(side="left",
                                                                                                        padx=10)

        # Frame for button to control its background
        button_frame = tk.Frame(row, bg="#9edcff")
        button_frame.pack(side="left", padx=5)

        tk.Button(button_frame, text="Apply", bg="#4CAF50", activebackground="#45a049", fg="white",
                  command=lambda cid=c['course_id']: enroll(cid),
                  bd=0, relief="flat", highlightthickness=0).pack()

    # Assignments
    tk.Label(assignments, text="Your Assignments", font=("Orbitron", 18), bg="#9edcff").pack(pady=10)
    student_assignments = backend.get_assignments_for_student(user_id)
    if not student_assignments:
        tk.Label(assignments, text="No assignments yet.", font=("Arial", 12), bg="#9edcff").pack(pady=10)
    else:
        for cid, tasks in student_assignments.items():
            tk.Label(assignments, text=f"{cid} Assignments", font=("Orbitron", 14, "bold"), bg="#9edcff").pack()
            for task in tasks:
                tk.Label(assignments, text=f"- {task['title']}: {task['description']}", wraplength=800,
                         bg="#9edcff").pack()

    # Quizzes
    tk.Label(quizzes, text="Your Quizzes", font=("Orbitron", 18), bg="#9edcff").pack(pady=10)
    student_quizzes = backend.get_quizzes_for_student(user_id)
    if not student_quizzes:
        tk.Label(quizzes, text="No quizzes yet.", font=("Arial", 12), bg="#9edcff").pack(pady=10)
    else:
        for cid, qzs in student_quizzes.items():
            tk.Label(quizzes, text=f"{cid} Quizzes", font=("Orbitron", 14, "bold"), bg="#9edcff").pack()
            for q in qzs:
                tk.Label(quizzes, text=f"- {q['title']}: {q['description']}", wraplength=800, bg="#9edcff").pack()

    tk.Button(sidebar, text="Home", command=lambda: show_frame("home"), **btn_style).pack(pady=10)
    tk.Button(sidebar, text="Courses", command=lambda: show_frame("courses"), **btn_style).pack(pady=10)
    tk.Button(sidebar, text="Assignments", command=lambda: show_frame("assignments"), **btn_style).pack(pady=10)
    tk.Button(sidebar, text="Quizzes", command=lambda: show_frame("quizzes"), **btn_style).pack(pady=10)
    show_frame("home")

def enroll(course_id):
    if backend.enroll_student(user_id, course_id):
        messagebox.showinfo("Success", f"You have enrolled in {course_id}.")
    else:
        messagebox.showinfo("Info", f"You are already enrolled in {course_id}.")

# INSTRUCTOR VIEWS
def build_instructor_dashboard():
    assign = create_frame("assign")
    quiz = create_frame("quiz")

    tk.Label(assign, text="Post Assignment", font=("Orbitron", 18), bg="#9edcff").pack(pady=10)
    tk.Label(assign, text="Course ID", bg="#9edcff").pack()
    cid_entry = tk.Entry(assign)
    cid_entry.pack()
    tk.Label(assign, text="Title", bg="#9edcff").pack()
    title_entry = tk.Entry(assign)
    title_entry.pack()
    tk.Label(assign, text="Description", bg="#9edcff").pack()
    desc_entry = tk.Entry(assign)
    desc_entry.pack()
    tk.Button(assign, text="Post", command=lambda: post_assignment(cid_entry.get(), title_entry.get(), desc_entry.get())).pack(pady=5)

    tk.Label(quiz, text="Post Quiz", font=("Orbitron", 18), bg="#9edcff").pack(pady=10)
    tk.Label(quiz, text="Course ID", bg="#9edcff").pack()
    cidq_entry = tk.Entry(quiz)
    cidq_entry.pack()
    tk.Label(quiz, text="Title", bg="#9edcff").pack()
    titleq_entry = tk.Entry(quiz)
    titleq_entry.pack()
    tk.Label(quiz, text="Description", bg="#9edcff").pack()
    descq_entry = tk.Entry(quiz)
    descq_entry.pack()
    tk.Button(quiz, text="Post", command=lambda: post_quiz(cidq_entry.get(), titleq_entry.get(), descq_entry.get())).pack(pady=5)

    tk.Button(sidebar, text="Post Assignment", command=lambda: show_frame("assign"), **btn_style).pack(pady=10)
    tk.Button(sidebar, text="Post Quiz", command=lambda: show_frame("quiz"), **btn_style).pack(pady=10)
    show_frame("assign")

def post_assignment(course_id, title, desc):
    if backend.post_assignment(user_id, course_id, title, desc):
        messagebox.showinfo("Success", "Assignment posted successfully.")
    else:
        messagebox.showerror("Error", "Failed to post assignment.")

def post_quiz(course_id, title, desc):
    if backend.post_quiz(user_id, course_id, title, desc):
        messagebox.showinfo("Success", "Quiz posted successfully.")
    else:
        messagebox.showerror("Error", "Failed to post quiz.")

# STYLING
btn_style = {
    "font": ("Orbitron", 14),
    "width": 15,
    "height": 2,
    "bd": 0,
    "relief": "flat",
    "bg": "#00bcd4",
    "fg": "black"
}

# LOAD DASHBOARD
if role.lower() == "student":
    build_student_dashboard()
else:
    build_instructor_dashboard()

root.mainloop()
