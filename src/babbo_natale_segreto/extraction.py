import json
import os
import random

from cryptography.fernet import Fernet

BASEDIR = os.path.dirname(os.path.abspath(__file__))

# Carica i dati dal file YAML
with open("config/participants.json", "r", encoding="utf-8") as f:
    people = json.load(f)

# Importa librerie per crittografia

# Genera una chiave di crittografia (salvala in modo sicuro!)
# Per questo esempio uso una chiave fissa, ma in produzione dovresti generarla una volta e salvarla
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)


def encrypt_name(name):
    """Cripta il nome del receiver"""
    return cipher.encrypt(name.encode()).decode()


def decrypt_name(encrypted_name):
    """Decripta il nome del receiver (per debug)"""
    return cipher.decrypt(encrypted_name.encode()).decode()


partecipants = []
for person in people:
    if person["participation"] == "True":
        # Aggiungi automaticamente il giver alla sua lista cant_take
        if person["name"] not in person["cant_take"]:
            person["cant_take"].append(person["name"])
        partecipants.append(person)


def create_assignments(partecipants, max_attempts=1000):
    """Crea gli abbinamenti rispettando i vincoli cant_take"""
    for attempt in range(max_attempts):
        # Mescola i partecipanti
        shuffled = partecipants.copy()
        random.shuffle(shuffled)

        assignments = {}
        available = [p["name"] for p in partecipants]

        # Prova a creare gli abbinamenti
        success = True
        for giver_obj in shuffled:
            giver = giver_obj["name"]
            cant_take = giver_obj["cant_take"]

            # Trova i receiver possibili (esclusi quelli in cant_take e già assegnati)
            possible_receivers = [name for name in available if name not in cant_take]

            if not possible_receivers:
                success = False
                break

            # Assegna un receiver casuale tra quelli possibili
            receiver = random.choice(possible_receivers)
            assignments[giver] = receiver
            available.remove(receiver)

        if success:
            return assignments

    raise Exception(
        f"Impossibile creare abbinamenti validi dopo {max_attempts} tentativi.\n Rimuovi i vincoli sulle possibili."
    )


assignments = create_assignments(partecipants)

# Crea la cartella per i file
output_dir = "config/assignments"
os.makedirs(output_dir, exist_ok=True)

print("Secret Santa Assignments (con nomi criptati):")
for giver, receiver in assignments.items():
    encrypted_receiver = encrypt_name(receiver)
    # print(f"{giver}: {encrypted_receiver}")

    # Crea un file per ogni persona
    # Nome file: usa il nome della persona (sostituendo spazi con underscore)
    filename = f"{giver.replace(' ', '_')}.txt"
    filepath = os.path.join(output_dir, filename)

    # Scrivi il file con il nome criptato sulla prima riga e la chiave sulla seconda
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{encrypted_receiver}\n")
        f.write(f"{encryption_key.decode()}\n")

    # print(f"  → File salvato: {filepath}")

print("\n✅ Chiave di crittografia (salvala in modo sicuro!):")
print(encryption_key.decode())
