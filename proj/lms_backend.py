import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "lms_data"

def load_json(filename):
    with open(DATA_DIR / filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, indent=4)

def get_courses():
    return load_json("courses.json")

def enroll_student(student_id, course_id):
    enrollments = load_json("enrollments.json")
    if student_id not in enrollments:
        enrollments[student_id] = []
    if course_id not in enrollments[student_id]:
        enrollments[student_id].append(course_id)
        save_json("enrollments.json", enrollments)
        return True
    return False

def get_enrolled_courses(student_id):
    enrollments = load_json("enrollments.json")
    return enrollments.get(student_id, [])

def get_assignments_for_student(username):
    assignments_path = os.path.join(DATA_DIR, 'assignments.json')
    enrollments_path = os.path.join(DATA_DIR, 'enrollments.json')

    with open(assignments_path, 'r') as a_file:
        assignments = json.load(a_file)

    with open(enrollments_path, 'r') as e_file:
        enrollments = json.load(e_file)

    student_courses = enrollments.get(username, [])
    student_assignments = {}

    for course_id in student_courses:
        student_assignments[course_id] = assignments.get(course_id, [])

    return student_assignments

def get_quizzes_for_student(username):
    quizzes_path = os.path.join(DATA_DIR, 'quizzes.json')
    enrollments_path = os.path.join(DATA_DIR, 'enrollments.json')

    if not os.path.exists(quizzes_path):
        return {}

    with open(quizzes_path, 'r') as q_file:
        quizzes = json.load(q_file)

    with open(enrollments_path, 'r') as e_file:
        enrollments = json.load(e_file)

    student_courses = enrollments.get(username, [])
    student_quizzes = {}

    for course_id in student_courses:
        student_quizzes[course_id] = quizzes.get(course_id, [])

    return student_quizzes

def post_assignment(instructor_id, course_id, title, description):
    assignments_path = os.path.join(DATA_DIR, 'assignments.json')

    try:
        # Load current assignments
        if os.path.exists(assignments_path):
            with open(assignments_path, 'r') as f:
                assignments = json.load(f)
        else:
            assignments = {}

        # Add the assignment
        if course_id not in assignments:
            assignments[course_id] = []

        assignments[course_id].append({
            "title": title,
            "description": description,
            "posted_by": instructor_id
        })

        # Save back
        with open(assignments_path, 'w') as f:
            json.dump(assignments, f, indent=4)

        return True
    except Exception as e:
        print(f"Error posting assignment: {e}")
        return False


def post_quiz(instructor_id, course_id, title, description):
    quizzes_path = os.path.join(DATA_DIR, 'quizzes.json')

    try:
        # Load existing quizzes
        if os.path.exists(quizzes_path):
            with open(quizzes_path, 'r') as f:
                quizzes = json.load(f)
        else:
            quizzes = {}

        if course_id not in quizzes:
            quizzes[course_id] = []

        quizzes[course_id].append({
            "title": title,
            "description": description,
            "posted_by": instructor_id
        })

        with open(quizzes_path, 'w') as f:
            json.dump(quizzes, f, indent=4)

        return True
    except Exception as e:
        print(f"Error posting quiz: {e}")
        return False
