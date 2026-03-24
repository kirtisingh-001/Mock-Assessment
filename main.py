<<<<<<< HEAD
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
=======
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# READ ALL + FILTER
@app.get("/students", response_model=list[schemas.StudentResponse])
def get_students(course: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Student)

    if course:
        query = query.filter(models.Student.course == course)

    return query.all()

# SEARCH (BONUS 🔥)
@app.get("/students/search", response_model=list[schemas.StudentResponse])
def search_students(name: str, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.name.contains(name)).all()

# UPDATE
@app.put("/students/{id}")
def update_student(id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()

    if not db_student:
        return {"error": "Student not found"}

    db_student.name = student.name
    db_student.age = student.age
    db_student.course = student.course

    db.commit()
    db.refresh(db_student)
    return db_student

# DELETE
@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()

    if not db_student:
        return {"error": "Student not found"}

    db.delete(db_student)
    db.commit()
    return {"message": "Deleted successfully"}
>>>>>>> ecfbe46a0c75bf69d758450db49e8cd1cf6fc6f5
