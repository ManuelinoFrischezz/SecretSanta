import random


def prepare_participants(
    people: list[dict],
):

    participants = []

    for person in people:
        if person["participation"] != "True":
            continue

        if person["name"] not in person["cant_take"]:
            person["cant_take"].append(person["name"])

        participants.append(person)

    return participants


def create_assignments(
    participants: list[dict],
    max_attempts: int = 1000,
):

    for _ in range(max_attempts):
        shuffled = participants.copy()

        random.shuffle(shuffled)

        assignments = {}

        available = [p["name"] for p in participants]

        success = True

        for giver_obj in shuffled:
            giver = giver_obj["name"]

            cant_take = giver_obj["cant_take"]

            possible_receivers = [name for name in available if name not in cant_take]

            if not possible_receivers:
                success = False

                break

            receiver = random.choice(possible_receivers)

            assignments[giver] = receiver

            available.remove(receiver)

        if success:
            return assignments

    raise ValueError("Unable to generate valid assignments.")
