from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import select

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.database import (  # noqa: E402
    SessionLocal,
    create_database_tables,
)
from backend.database_models import User  # noqa: E402


USERS_FILE = PROJECT_ROOT / "data" / "users.csv"

ELECTIVE_COLUMNS = [
    "general_elective_credits",
    "cs_elective_credits",
    "english_elective_credits",
    "science_elective_credits",
    "humanities_elective_credits",
    "social_science_elective_credits",
    "ethics_elective_credits",
]


def safe_integer(value) -> int:
    try:
        if pd.isna(value) or value == "":
            return 0

        return int(float(value))
    except (TypeError, ValueError):
        return 0


def migrate_users() -> None:
    if not USERS_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {USERS_FILE}"
        )

    create_database_tables()

    users = pd.read_csv(USERS_FILE).fillna("")

    migrated = 0
    skipped = 0

    with SessionLocal() as database:
        for _, row in users.iterrows():
            username = str(
                row.get("username", "")
            ).strip().lower()

            if not username:
                continue

            existing_user = database.scalar(
                select(User).where(
                    User.username == username
                )
            )

            if existing_user is not None:
                skipped += 1
                continue

            user_data = {
                "username": username,
                "completed_required_courses": str(
                    row.get(
                        "completed_required_courses",
                        "",
                    )
                ),
                "custom_completed_courses": str(
                    row.get(
                        "custom_completed_courses",
                        "",
                    )
                ),
                "planned_courses": str(
                    row.get("planned_courses", "")
                ),
            }

            for column in ELECTIVE_COLUMNS:
                user_data[column] = safe_integer(
                    row.get(column, 0)
                )

            database.add(User(**user_data))
            migrated += 1

        database.commit()

    print(
        f"Migration complete: "
        f"{migrated} migrated, "
        f"{skipped} skipped."
    )


if __name__ == "__main__":
    migrate_users()