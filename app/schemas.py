from pydantic import BaseModel


class Course(BaseModel):
    name: str


class Enrollment(BaseModel):
    student_id: int
    course_id: int
