#!/bin/bash

cd /Users/federicobernardini/Desktop/BabboNataleSegreto

# Controlla se è stato passato un nome come argomento
if [ -z "$1" ]; then
    echo "❌ Errore: Devi specificare il nome del giver!"
    echo "Uso: ./scripts/estrazione.sh \\Nome_Cognome\\"
    echo ""
    echo "Esempio: ./scripts/estrazione.sh \\Chiara_Di_Stefano\\"
    exit 1
fi

# Nome del giver passato come argomento
GIVER_NAME="$1"

# Converte il nome in formato filename (sostituisce spazi con underscore)
FILENAME="${GIVER_NAME// /_}.txt"
FILEPATH="config/assignments/$FILENAME"

# Controlla se il file esiste
if [ ! -f "$FILEPATH" ]; then
    echo "❌ Errore: File non trovato: $FILEPATH"
    echo ""
    echo "File disponibili:"
    ls -1 config/assignments/*.txt 2>/dev/null | sed 's/configg/assignments\//  - /' | sed 's/\.txt$//' | sed 's/_/ /g'
    exit 1
fi

echo "🎅 Estrazione per: $GIVER_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Leggi il nome criptato (prima riga) e la chiave (seconda riga)
ENCRYPTED_NAME=$(sed -n '1p' "$FILEPATH")
ENCRYPTION_KEY=$(sed -n '2p' "$FILEPATH")

# echo "📄 File trovato: $FILENAME"
# echo ""
# echo "🔐 Nome criptato:"
# echo "$ENCRYPTED_NAME"
# echo ""
# echo "🔑 Chiave di decrittazione:"
# echo "$ENCRYPTION_KEY"
# echo ""
# echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
# echo "Per decrittare il nome, usa:"
# echo "  venv_babbo/bin/python src/babbonatale_segreto/decrypt_names.py"
# echo ""
# echo "Oppure esegui automaticamente la decrittazione..."

# Esegui la decrittazione automatica usando Python
venv_babbo/bin/python -c "
from cryptography.fernet import Fernet

encrypted = '$ENCRYPTED_NAME'
key = '$ENCRYPTION_KEY'

cipher = Fernet(key.encode())
decrypted = cipher.decrypt(encrypted.encode()).decode()

print('🎁 Il tuo Babbo Natale Segreto è:\n')
print(f'   ✨ {decrypted} ✨')
"

sleep 3
clear
