import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from oneroster_api import Classes, Enrollment, User, set_credentials

from clever_sync import build_teacher_data, create_sections_sheet


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

    teachers_dict = build_teacher_data(users)
    sections_dict = create_sections_sheet(
        classes=classes, enrollments=enrollments, teachers=teachers_dict
    )

    teachers = pd.DataFrame(teachers_dict)
    sections = pd.DataFrame(sections_dict)

    teachers.to_csv("data/clever/teachers.csv", index=False)
    sections.to_csv("data/clever/sections.csv", index=False)
    print(sections)


if __name__ == "__main__":
    main()
