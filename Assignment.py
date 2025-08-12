import json

# ======== Class Definitions ========

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")


class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def enroll_course(self, course_name):
        if course_name not in self.courses:
            self.courses.append(course_name)

    def display_student_info(self):
        print("Student Information:")
        print(f"Name: {self.name}")
        print(f"ID: {self.student_id}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")
        print(f"Enrolled Courses: {', '.join(self.courses) if self.courses else 'None'}")
        print(f"Grades: {self.grades if self.grades else 'None'}")


class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []  # list of student IDs

    def add_student(self, student_id):
        if student_id not in self.students:
            self.students.append(student_id)

    def display_course_info(self):
        print("Course Information:")
        print(f"Course Name: {self.course_name}")
        print(f"Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        print(f"Enrolled Students: {', '.join(self.students) if self.students else 'None'}")


# ======== Data Storage ========

students = {}
courses = {}
DATA_FILE = "student_management.json"

# ======== Functions ========

def add_new_student():
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    address = input("Enter Address: ")
    student_id = input("Enter Student ID: ")
    if student_id in students:
        print("Error: Student ID already exists.")
        return
    students[student_id] = Student(name, age, address, student_id)
    print(f"Student {name} (ID: {student_id}) added successfully.")

def add_new_course():
    course_name = input("Enter Course Name: ")
    course_code = input("Enter Course Code: ")
    instructor = input("Enter Instructor: ")
    if course_code in courses:
        print("Error: Course code already exists.")
        return
    courses[course_code] = Course(course_name, course_code, instructor)
    print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")

def enroll_student_in_course():
    student_id = input("Enter Student ID: ")
    course_code = input("Enter Course Code: ")
    if student_id not in students:
        print("Error: Student not found.")
        return
    if course_code not in courses:
        print("Error: Course not found.")
        return
    students[student_id].enroll_course(courses[course_code].course_name)
    courses[course_code].add_student(students[student_id].name)
    print(f"Student {students[student_id].name} (ID: {student_id}) enrolled in {courses[course_code].course_name} (Code: {course_code}).")

def add_grade_for_student():
    student_id = input("Enter Student ID: ")
    course_code = input("Enter Course Code: ")
    grade = input("Enter Grade: ")
    if student_id not in students:
        print("Error: Student not found.")
        return
    if course_code not in courses:
        print("Error: Course not found.")
        return
    course_name = courses[course_code].course_name
    if course_name not in students[student_id].courses:
        print("Error: Student not enrolled in this course.")
        return
    students[student_id].add_grade(course_name, grade)
    print(f"Grade {grade} added for {students[student_id].name} in {course_name}.")

def display_student_details():
    student_id = input("Enter Student ID: ")
    if student_id not in students:
        print("Error: Student not found.")
        return
    students[student_id].display_student_info()

def display_course_details():
    course_code = input("Enter Course Code: ")
    if course_code not in courses:
        print("Error: Course not found.")
        return
    courses[course_code].display_course_info()

def save_data():
    data = {
        "students": {
            sid: {
                "name": s.name,
                "age": s.age,
                "address": s.address,
                "student_id": s.student_id,
                "grades": s.grades,
                "courses": s.courses
            }
            for sid, s in students.items()
        },
        "courses": {
            cid: {
                "course_name": c.course_name,
                "course_code": c.course_code,
                "instructor": c.instructor,
                "students": c.students
            }
            for cid, c in courses.items()
        }
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("All student and course data saved successfully.")

def load_data():
    global students, courses
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        students = {
            sid: Student(
                s["name"], s["age"], s["address"], s["student_id"]
            )
            for sid, s in data["students"].items()
        }
        for sid, s in data["students"].items():
            students[sid].grades = s["grades"]
            students[sid].courses = s["courses"]

        courses = {
            cid: Course(
                c["course_name"], c["course_code"], c["instructor"]
            )
            for cid, c in data["courses"].items()
        }
        for cid, c in data["courses"].items():
            courses[cid].students = c["students"]

        print("Data loaded successfully.")
    except FileNotFoundError:
        print("No saved data found.")

# ======== Main Menu ========

def main():
    while True:
        print("\n==== Student Management System ====")
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")

        choice = input("Select Option: ")

        if choice == "1":
            add_new_student()
        elif choice == "2":
            add_new_course()
        elif choice == "3":
            enroll_student_in_course()
        elif choice == "4":
            add_grade_for_student()
        elif choice == "5":
            display_student_details()
        elif choice == "6":
            display_course_details()
        elif choice == "7":
            save_data()
        elif choice == "8":
            load_data()
        elif choice == "0":
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
