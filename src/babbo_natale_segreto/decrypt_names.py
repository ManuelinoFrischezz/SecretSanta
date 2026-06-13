"""
Script per decrittare i nomi del Babbo Natale Segreto
"""
from cryptography.fernet import Fernet

def decrypt_name(encrypted_name, key):
    """Decripta un nome usando la chiave fornita"""
    cipher = Fernet(key.encode())
    return cipher.decrypt(encrypted_name.encode()).decode()

# ISTRUZIONI:
# 1. Copia la chiave generata dallo script principale
# 2. Copia il nome criptato che vuoi decrittare
# 3. Esegui questo script

if __name__ == "__main__":
    print("🔓 DECRITTATORE BABBO NATALE SEGRETO\n")
    
    # Inserisci qui la chiave
    encryption_key = input("Inserisci la chiave di crittografia: ").strip()
    
    # Inserisci il nome criptato
    encrypted_name = input("Inserisci il nome criptato: ").strip()
    
    try:
        decrypted = decrypt_name(encrypted_name, encryption_key)
        print(f"\n✅ Nome decrittato: {decrypted}")
    except Exception as e:
        print(f"\n❌ Errore nella decrittazione: {e}")
        print("Controlla che chiave e nome criptato siano corretti!")
