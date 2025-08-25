import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from oneroster_api import Classes, Demographics, Enrollments, Users, set_credentials

import clever_sync as cs


def setup() -> None:
    load_dotenv(".env")
    set_credentials(
        base_url=os.getenv("ONEROSTER_BASEURL"),
        client_id=os.getenv("ONEROSTER_ID"),
        client_secret=os.getenv("ONEROSTER_SECRET"),
        credential_path=Path("data/secure/oneroster.json"),
    )


def main() -> None:
    setup()
    classes = Classes.retrieve_all()
    users = Users.retrieve_all()
    enrollments = Enrollments.retrieve_all()
    demographics = Demographics.retrieve_all()

    teachers_data = cs.build_teacher_data(users)
    sections_data = cs.create_sections_sheet(
        classes=classes, enrollments=enrollments, teachers=teachers_data
    )
    enrollments_data = cs.build_enrollment_data(
        enrollments_list=enrollments, sections_data=sections_data
    )
    students_data = cs.build_student_data(
        user_list=users, enrollment_data=enrollments_data, demographic_data=demographics
    )

    teachers_sheet = pd.DataFrame(teachers_data)
    sections_sheet = pd.DataFrame(sections_data)
    enrollments_sheet = pd.DataFrame(enrollments_data)
    students_sheet = pd.DataFrame(students_data)

    teachers_sheet.to_csv("data/clever/teachers.csv", index=False)
    sections_sheet.to_csv("data/clever/sections.csv", index=False)
    enrollments_sheet.to_csv("data/clever/enrollments.csv", index=False)
    students_sheet.to_csv("data/clever/students.csv", index=False)
    print(enrollments_sheet)


if __name__ == "__main__":
    main()
