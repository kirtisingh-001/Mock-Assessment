from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Fake database (list)
students = []

# Model for validation
class Student(BaseModel):
    name: str
    age: int
    course: str

# Home route (optional)
@app.get("/")
def home():
    return {"message": "Student API chal rahi hai 🚀"}

# GET all students (with query filter)
@app.get("/students")
def get_students(course: Optional[str] = None):
    if course:
        return [s for s in students if s["course"].lower() == course.lower()]
    return students

# POST - Add new student
@app.post("/students", status_code=201)
def add_student(student: Student):
    student_dict = student.dict()
    student_dict["id"] = len(students) + 1
    students.append(student_dict)
    return student_dict

# GET student by ID
@app.get("/students/{id}")
def get_student(id: int):
    for s in students:
        if s["id"] == id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")

# PUT - Update student
@app.put("/students/{id}")
def update_student(id: int, student: Student):
    for i in range(len(students)):
        if students[i]["id"] == id:
            students[i].update(student.dict())
            return students[i]
    raise HTTPException(status_code=404, detail="Student not found")

# DELETE - Remove student
@app.delete("/students/{id}")
def delete_student(id: int):
    for i in range(len(students)):
        if students[i]["id"] == id:
            return {
                "message": "Student deleted successfully",
                "data": students.pop(i)
            }
    raise HTTPException(status_code=404, detail="Student not found")