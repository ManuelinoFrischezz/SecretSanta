"""
Secret Santa decryption utility.
"""

from babbo_natale_segreto.crypto import (
    decrypt_name,
)


def main():

    print("🔓 SECRET SANTA DECRYPTOR\n")

    encryption_key = input("Encryption key: ").strip()

    encrypted_name = input("Encrypted name: ").strip()

    try:
        decrypted = decrypt_name(
            encrypted_name,
            encryption_key,
        )

        print(f"\n✅ Decrypted name: {decrypted}")

    except Exception as e:
        print(f"\n❌ Decryption error: {e}")


if __name__ == "__main__":
    main()
