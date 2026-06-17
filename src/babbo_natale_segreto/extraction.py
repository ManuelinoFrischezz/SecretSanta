from babbo_natale_segreto.assignment_engine import (
    create_assignments,
    prepare_participants,
)

from babbo_natale_segreto.assignments import (
    save_assignments,
)
from babbo_natale_segreto.crypto import (
    generate_cipher,
)
from babbo_natale_segreto.participants import (
    load_participants_full_info,
)


def main():

    people = load_participants_full_info()

    participants = prepare_participants(people)

    assignments = create_assignments(participants)

    cipher, encryption_key = generate_cipher()

    save_assignments(
        assignments,
        cipher,
        encryption_key,
    )

    print("✅ Secret Santa assignments generated.")


if __name__ == "__main__":
    main()
