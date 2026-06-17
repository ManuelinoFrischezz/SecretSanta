#!/bin/bash

# Start Secret Santa Streamlit application
echo "🎅 Starting Secret Santa..."
echo ""

# Load environment variables
set -a
source ".env"
set +a

set -euo pipefail

# Get current assignment filenames
assignment_names=$(
    find config/assignments \
        -type f \
        -name "*.txt" \
        -exec basename {} .txt \; \
    | sort
)

# Get active participants
participant_names=$(
    venv_babbo/bin/python - <<'PY'
import json

with open("config/participants.json", encoding="utf-8") as f:
    participants = json.load(f)

for name in sorted(
    person["name"].replace(" ", "_")
    for person in participants
    if person.get("participation") == "True"
):
    print(name)
PY
)

# Run extraction only if needed
if diff \
    <(echo "$assignment_names") \
    <(echo "$participant_names") \
    >/dev/null
then

    echo "Assignments are up to date."

else

    echo "Assignments mismatch. Running extraction..."

    rm -f config/assignments/*.txt

    PYTHONPATH=src \
    venv_babbo/bin/python \
        src/babbo_natale_segreto/extraction.py
fi

# Start Streamlit
PYTHONPATH=src \
venv_babbo/bin/streamlit run \
    src/streamlit_app/app_streamlit.py &

# Expose the service through ngrok
ngrok http "$PORT_NUMBER" \
    --basic-auth "$ACCESS_KEY"
