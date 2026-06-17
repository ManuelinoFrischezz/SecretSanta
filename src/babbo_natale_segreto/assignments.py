import os

from babbo_natale_segreto.crypto import (
    encrypt_name,
)
from babbo_natale_segreto.storage import (
    ASSIGNMENTS_DIR,
)


def get_assignment(
    person_name: str,
):

    filename = f"{person_name.replace(' ', '_')}.txt"

    filepath = os.path.join(
        ASSIGNMENTS_DIR,
        filename,
    )

    if not os.path.exists(filepath):
        return None, None

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

        if len(lines) >= 2:
            encrypted_name = lines[0].strip()

            encryption_key = lines[1].strip()

            return (
                encrypted_name,
                encryption_key,
            )

    return None, None


def save_assignments(
    assignments: dict[str, str],
    cipher,
    encryption_key: bytes,
):

    os.makedirs(
        ASSIGNMENTS_DIR,
        exist_ok=True,
    )

    for giver, receiver in assignments.items():
        encrypted_receiver = encrypt_name(
            cipher,
            receiver,
        )

        filename = f"{giver.replace(' ', '_')}.txt"

        filepath = os.path.join(
            ASSIGNMENTS_DIR,
            filename,
        )

        with open(
            filepath,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(f"{encrypted_receiver}\n")

            f.write(f"{encryption_key.decode()}\n")
