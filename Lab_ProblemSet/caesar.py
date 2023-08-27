# Caesar Cipher
import sys


def main(key: int) -> None:
    key %= 26
    word = input("plaintext: ").strip()
    alphabet = [chr(i) for i in range(97, 123)]  # 'a' to 'z'
    ciphertext = ""

    for char in word:
        if not char.isalpha():
            ciphertext += char
            continue

        for i, alpha in enumerate(alphabet):
            if alpha == char:
                ciphertext += alphabet[(i + key) % 26]
            elif alpha.upper() == char:
                ciphertext += alphabet[(i + key) % 26].upper()

    print(f"ciphertext: {ciphertext}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    if int(sys.argv[1]) < 1:
        sys.exit(1)

    main(int(sys.argv[1]))
