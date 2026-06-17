import os

from babbo_natale_segreto.storage import (
    ASSIGNMENTS_DIR,
    PARTICIPANTS_FILE,
    load_json,
    save_json,
)


def load_participants_full_info():

    return load_json(PARTICIPANTS_FILE)


def load_active_participants():

    participants = load_participants_full_info()

    return sorted([p["name"] for p in participants if p["participation"] == "True"])


def save_participants(
    participants: list[dict],
) -> None:

    save_json(
        PARTICIPANTS_FILE,
        participants,
    )


def add_new_member(
    participants: list[dict],
    name: str,
    surname: str,
    cant_take_list: list[str],
):

    new_participant_name = f"{name.title()} {surname.title()}"

    participants.append(
        {
            "name": new_participant_name,
            "participation": "True",
            "cant_take": cant_take_list,
        }
    )

    save_participants(participants)


def toggle_participant(
    participants: list[dict],
    name: str,
):

    for person in participants:
        if person["name"] == name:
            current = person["participation"]

            person["participation"] = "False" if current == "True" else "True"

            break

    save_participants(participants)


def delete_participant(
    participants: list[dict],
    name: str,
):

    updated_participants = [person for person in participants if person["name"] != name]

    assignment_file = os.path.join(
        ASSIGNMENTS_DIR,
        f"{name.replace(' ', '_')}.txt",
    )

    if os.path.exists(assignment_file):
        os.remove(assignment_file)

    save_participants(updated_participants)

    return updated_participants
