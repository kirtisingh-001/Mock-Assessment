from fastapi import FastAPI

app = FastAPI()

students = []

# function for testing
def add(a: int, b: int) -> int:
    return a + b

# CREATE
@app.post("/students")
def create_student(student: dict):
    student["id"] = len(students) + 1
    students.append(student)
    return student

# GET
@app.get("/students")
def get_students():
    return students