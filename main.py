import os
from pathlib import Path

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


def import_oneroster_data() -> dict:
    return {
        "users": Users.retrieve_all(),
        "enrollments": Enrollments.retrieve_all(),
        "demographics": Demographics.retrieve_all(),
        "classes": Classes.retrieve_all(),
    }


def main() -> None:
    setup()
    oneroster_data = import_oneroster_data()
    clever_data = cs.build_clever_sheets(oneroster_data)
    cs.export_clever_sheets(clever_data, Path("data/clever"))


if __name__ == "__main__":
    main()
