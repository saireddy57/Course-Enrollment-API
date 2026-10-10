from fastapi import FastAPI, HTTPException
import json

from .schemas import Course, Enrollment

app = FastAPI()


def load_data():
    with open("data.json", "r") as file:
        return json.load(file)


def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


@app.post("/courses")
def create_course(course: Course):
    data = load_data()

    new_course = {
        "id": len(data["courses"]) + 1,
        "name": course.name
    }

    data["courses"].append(new_course)
    save_data(data)

    return new_course


@app.get("/courses")
def get_courses():
    data = load_data()
    return data["courses"]


@app.post("/enroll")
def enroll(enrollment: Enrollment):
    data = load_data()

    if not any(s["id"] == enrollment.student_id for s in data["students"]):
        raise HTTPException(status_code=404, detail="Student not found")

    if not any(c["id"] == enrollment.course_id for c in data["courses"]):
        raise HTTPException(status_code=404, detail="Course not found")

    for e in data["enrollments"]:
        if (
            e["student_id"] == enrollment.student_id
            and e["course_id"] == enrollment.course_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Student already enrolled in this course"
            )

    new_enrollment = {
        "id": len(data["enrollments"]) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }

    data["enrollments"].append(new_enrollment)
    save_data(data)

    return new_enrollment


@app.get("/students/{student_id}/courses")
def get_student_courses(student_id: int):
    data = load_data()

    if not any(s["id"] == student_id for s in data["students"]):
        raise HTTPException(status_code=404, detail="Student not found")

    course_ids = [
        e["course_id"]
        for e in data["enrollments"]
        if e["student_id"] == student_id
    ]

    return [
        course
        for course in data["courses"]
        if course["id"] in course_ids
    ]


@app.delete("/enroll/{enrollment_id}")
def delete_enrollment(enrollment_id: int):
    data = load_data()

    for enrollment in data["enrollments"]:
        if enrollment["id"] == enrollment_id:
            data["enrollments"].remove(enrollment)
            save_data(data)
            return {"message": "Enrollment deleted"}

    raise HTTPException(status_code=404, detail="Enrollment not found")
