"""
🎅 Babbo Natale Segreto - Interfaccia Web
App Streamlit per visualizzare le assegnazioni del Babbo Natale Segreto
"""

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass

import streamlit as st
from cryptography.fernet import Fernet


@dataclass
class NewMember:
    """New member data class

    args:
        name[str]: name of the new partecipant
        surname[str]: surname of the new partecipant
        cant_take_list[list[str]]: list of people that can't be taken by the new partecipant
    """

    name: str
    surname: str
    cant_take_list: list[str]


# Configurazione pagina
st.set_page_config(
    page_title="🎅 Babbo Natale Segreto", page_icon="🎄", layout="centered"
)

# Directory base
BASEDIR = os.path.dirname(os.path.abspath(__file__))
ASSIGNMENTS_DIR = "config/assignments"


def load_participants():
    """Carica la lista dei partecipanti dal file JSON"""
    try:
        with open("config/participants.json", "r", encoding="utf-8") as f:
            people = json.load(f)
        # Filtra solo i partecipanti attivi
        participants = [p["name"] for p in people if p["participation"] == "True"]

        if not participants:
            st.warning(
                "Nessun partecipante trovato! Registra almeno 3 persone per usare il servizio."
            )

        st.session_state["participants_full_info"] = people

        return sorted(participants)
    except FileNotFoundError:
        st.error("❌ File config/participants.json non trovato!")
        return []


if "participants" not in st.session_state:
    st.session_state["participants"] = load_participants()


def get_assignment(person_name):
    """Recupera l'assegnazione per una persona specifica"""
    # Converti il nome in formato file
    filename = f"{person_name.replace(' ', '_')}.txt"
    filepath = os.path.join(ASSIGNMENTS_DIR, filename)

    if not os.path.exists(filepath):
        return None, None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                encrypted_name = lines[0].strip()
                encryption_key = lines[1].strip()
                return encrypted_name, encryption_key
    except Exception as e:
        st.error(f"❌ Errore nella lettura del file: {e}")

    return None, None


def decrypt_assignment(encrypted_name, encryption_key):
    """Decripta il nome dell'assegnazione"""
    try:
        cipher = Fernet(encryption_key.encode())
        decrypted = cipher.decrypt(encrypted_name.encode()).decode()
        return decrypted
    except Exception as e:
        st.error(f"❌ Errore nella decrittazione: {e}")
        return None


def run_sorteggio():
    """Esegue lo script extraction.py per generare un nuovo sorteggio"""
    script_path = "src/babbo_natale_segreto/extraction.py"

    try:
        # Esegui lo script Python
        result = subprocess.run(
            [sys.executable, script_path], capture_output=True, text=True
        )

        if result.returncode == 0:
            return True, "✅ Sorteggio completato con successo!"
        else:
            return False, f"❌ Errore durante il sorteggio:\n{result.stderr}"
    except Exception as e:
        return False, f"❌ Errore nell'esecuzione: {str(e)}"


def cleanup_assignments() -> None:

    valid_names = {
        p["name"].replace(" ", "_")
        for p in st.session_state["participants_full_info"]
        if p["participation"] == "True"
    }

    for filename in os.listdir("config/assignments"):
        if not filename.endswith(".txt"):
            continue

        assignment_name = filename.removesuffix(".txt")

        if assignment_name not in valid_names:
            os.remove(
                os.path.join(
                    "config/assignments",
                    filename,
                )
            )


def add_new_member(new_member: NewMember) -> None:

    new_participant_name = f"{new_member.name.title()} {new_member.surname.title()}"

    new_participant = {
        "name": new_participant_name,
        "participation": "True",
        "cant_take": new_member.cant_take_list,
    }

    st.session_state["participants_full_info"].append(new_participant)

    save_participants()

    success, message = run_sorteggio()

    if not success:
        raise RuntimeError(message)


@st.dialog("Add New Member")
def show_registration():
    """Registration pop up for adding a new partecipant"""
    st.write("Please enter your details to register a new member.")
    new_member = NewMember(
        name=st.text_input("Nome"),
        surname=st.text_input("Cognome"),
        cant_take_list=st.multiselect("can't take", st.session_state["participants"]),
    )

    if st.button("Submit New Member"):
        # Create a file for each member being registered
        try:
            add_new_member(new_member)
            # Also add the functionality of removing a member
            st.success("New member added!")
            st.rerun()
        except Exception as e:
            raise ValueError("Error: %s", e)


def save_participants() -> None:
    """Persist participants and refresh session state."""

    participants = st.session_state["participants_full_info"]

    with open("config/participants.json", "w", encoding="utf-8") as f:
        json.dump(
            participants,
            f,
            indent=4,
            ensure_ascii=False,
        )

    st.session_state["participants"] = [
        p["name"] for p in participants if p["participation"] == "True"
    ]


def delete_participant(name: str) -> None:
    """Delete participant permanently."""

    st.session_state["participants_full_info"] = [
        person
        for person in st.session_state["participants_full_info"]
        if person["name"] != name
    ]

    save_participants()

    cleanup_assignments()

    success, message = run_sorteggio()

    if not success:
        raise RuntimeError(message)


def remove_from_extraction(name: str) -> None:
    """Toggle participant participation."""

    for person in st.session_state["participants_full_info"]:
        if person["name"] == name:
            person["participation"] = (
                "False" if person["participation"] == "True" else "True"
            )
            break

    save_participants()

    cleanup_assignments()

    success, message = run_sorteggio()

    if not success:
        raise RuntimeError(message)


# ===== SIDEBAR - AMMINISTRAZIONE =====
with st.sidebar:
    st.header("⚙️ Impostazioni")
    st.markdown("---")

    st.subheader("🔄 Nuovo Sorteggio")
    st.warning("⚠️ **ATTENZIONE**: Questo cancellerà tutte le assegnazioni esistenti!")

    # Checkbox di conferma
    confirm = st.checkbox("Confermo di voler eseguire un nuovo sorteggio")

    if st.button(
        "🎲 Riesegui Sorteggio",
        type="secondary",
        disabled=not confirm,
        use_container_width=True,
    ):
        with st.spinner("Esecuzione sorteggio in corso..."):
            success, message = run_sorteggio()

            if success:
                st.success(message)
                # Reset dello stato
                if "reveal" in st.session_state:
                    del st.session_state.reveal
                st.rerun()
            else:
                st.error(message)

    st.markdown("---")
    st.caption(
        "💡 Il nuovo sorteggio genererà nuove assegnazioni casuali rispettando i vincoli definiti."
    )

# ===== INTERFACCIA PRINCIPALE =====


def __main__():

    if "selected_name" not in st.session_state:
        st.session_state["selected_name"] = ""

    if "reveal" not in st.session_state:
        st.session_state["reveal"] = False

    # Titolo
    st.markdown(
        """
        <div style="
            text-align: center;
        ">
            <h2>🎅 Babbo Natale Segreto</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "➕ Register Participant",
            use_container_width=True,
        ):
            show_registration()

    with col2:
        if st.button(
            "👥 Manage Participants",
            use_container_width=True,
        ):
            st.session_state["show_manage_participants"] = not st.session_state.get(
                "show_manage_participants",
                False,
            )

    # Selezione del nome
    st.subheader("🎄 Seleziona il tuo nome")

    # Usa session_state per controllare la selezione
    participants_options = [""] + st.session_state["participants"]

    selected_name = st.session_state.get(
        "selected_name",
        "",
    )

    if selected_name not in participants_options:
        selected_name = ""
        st.session_state.selected_name = ""

    selected_index = participants_options.index(selected_name)

    selected_name = st.selectbox(
        "Chi sei?",
        options=participants_options,
        format_func=lambda x: "Scegli il tuo nome..." if x == "" else x,
        key="name_selector",
        index=selected_index,
    )

    # Aggiorna lo stato
    if selected_name != st.session_state["selected_name"]:
        st.session_state["selected_name"] = selected_name
        st.session_state["reveal"] = False

    if selected_name:
        st.markdown("---")

        # Recupera l'assegnazione
        encrypted_name, encryption_key = get_assignment(selected_name)

        if encrypted_name and encryption_key:
            # Mostra un pulsante per rivelare il nome
            left_spacer, button_col, right_spacer = st.columns([3, 2, 3])

            with button_col:
                if st.button(
                    "🎁 Scopri chi hai sorteggiato!",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state["reveal"] = True

            # Se il pulsante è stato premuto, mostra il nome
            if st.session_state.get("reveal", False):
                decrypted_name = decrypt_assignment(encrypted_name, encryption_key)

                if decrypted_name:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #1e4625;
                            padding: 1rem;
                            border-radius: 0.8rem;
                            text-align: center;
                            color: white;
                            margin-top: 0.8rem;
                            margin-bottom: 0.8rem;
                        ">
                            <h3>🎉 Hai sorteggiato:</h3>
                            <h2>{decrypted_name}</h2>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        """
                        <div style="
                            background-color: rgba(255, 193, 7, 0.15);
                            border: 1px solid rgba(255, 193, 7, 0.35);
                            padding: 0.8rem;
                            border-radius: 0.5rem;
                            text-align: center;
                            color: rgb(255, 193, 7);
                            margin-top: 0.8rem;
                            margin-bottom: 0.8rem;
                            font-size: 0.9rem;
                            font-weight: 500;
                        ">
                            💡 Ricorda: È un segreto! Non fare l'infame e tienilo per te. 🤫
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Timer per nascondere dopo 3 secondi
                    time.sleep(5)

                    # Reset dello stato e della selezione
                    st.session_state.reveal = False
                    st.rerun()
        else:
            st.error(f"❌ Nessuna assegnazione trovata per {selected_name}")
            st.info("💡 Assicurati che il sorteggio sia stato eseguito correttamente.")

    if st.session_state.get("show_manage_participants", False):
        st.markdown("---")
        st.subheader("👥 Manage Participants")

        st.write("Enable, disable or permanently remove participants.")

        header1, header2, header3 = st.columns([5, 2, 2])

        with header1:
            st.markdown(
                "**ATTENTION**: EXCLUDING OR DELETEING A MEMEBER WILL START A NEW DRAW!"
            )

        st.divider()

        for participant in st.session_state["participants_full_info"]:
            name = participant["name"]
            active = participant["participation"] == "True"

            col1, col2, col3 = st.columns([5, 2, 2])

            with col1:
                st.write(name)

            with col2:
                st.write("🟢 Active" if active else "🔴 Inactive")

            with col3:
                action_col1, action_col2 = st.columns(2)

                with action_col1:
                    if st.button(
                        "Exclude" if active else "Include",
                        key=f"toggle_{name}",
                        use_container_width=True,
                    ):
                        remove_from_extraction(name)
                        st.rerun()

                with action_col2:
                    if st.button(
                        "Delete",
                        key=f"delete_{name}",
                        type="primary",
                        use_container_width=True,
                    ):
                        st.session_state["pending_delete"] = name
                        st.rerun()

            if st.session_state.get("pending_delete") == name:
                st.warning(f"⚠️ Delete {name} permanently?")

                confirm_col, cancel_col = st.columns(2)

                with confirm_col:
                    if st.button(
                        "DELETE",
                        key=f"confirm_delete_{name}",
                        type="primary",
                        use_container_width=True,
                    ):
                        delete_participant(name)

                        del st.session_state["pending_delete"]

                        st.rerun()

                with cancel_col:
                    if st.button(
                        "Cancel",
                        key=f"cancel_delete_{name}",
                        use_container_width=True,
                    ):
                        del st.session_state["pending_delete"]

                        st.rerun()

                st.divider()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888; font-size: 0.8em;'>
        🔥 Tradizione Crazy ZC 🔥<br>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    __main__()
