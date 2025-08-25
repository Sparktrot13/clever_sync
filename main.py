import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from oneroster_api import Classes, Enrollment, User, set_credentials

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
    enrollments = Enrollment.retrieve_all()
    users = User.retrieve_all()
    enrollments = Enrollment.retrieve_all()

    teachers_dict = cs.build_teacher_data(users)
    sections_dict = cs.create_sections_sheet(
        classes=classes, enrollments=enrollments, teachers=teachers_dict
    )
    enrollments_dict = cs.build_enrollment_data(
        enrollments_list=enrollments, sections_data=sections_dict
    )

    teachers = pd.DataFrame(teachers_dict)
    sections = pd.DataFrame(sections_dict)
    enrollments = pd.DataFrame(enrollments_dict)

    teachers.to_csv("data/clever/teachers.csv", index=False)
    sections.to_csv("data/clever/sections.csv", index=False)
    enrollments.to_csv("data/clever/enrollments.csv", index=False)
    print(enrollments)


if __name__ == "__main__":
    main()
