from faker import Faker
import random
from .models import *
from django.db.models import Sum

fake = Faker()


def subject_marks(n):
    try:
        students_obj = Student.objects.all()
        for students in students_obj:
            subjects = Subject.objects.all()
            for subject in subjects:
                StudentSubjectMarks.objects.create(
                    subject=subject,
                    student=students,
                    marks=random.randint(0, 100)
                )
    except Exception as e:
        print(e)


def seed_db(n=10) -> None:
    try:
        for i in range(0, n):
            department_obj = Department.objects.all()
            random_idx = random.randint(0, len(department_obj) - 1)
            department = department_obj[random_idx]
            student_id = f'STU-0{random.randint(100, 999)}'
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(18, 24)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)
            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address
            )
    except Exception as e:
        print(e)


def generate_reportCard():
    currentRank = -1
    ranks = Student.objects.annotate(marks=Sum("studentmarks__marks")).order_by("-marks", "-student_age")
    i = 1
    for rank in ranks:
        StudentReportCard.objects.create(
            student=rank,
            student_rank=i
        )
        i = i + 1
