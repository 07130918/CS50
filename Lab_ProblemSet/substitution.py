import sys

def main(key: str) -> int:
    word = input("plaintext: ").strip()
    alphabet = [chr(i) for i in range(97, 123)]  # 'a' to 'z'
    ciphertext = ""

    for char in word:
        try:
            alphabet_index = alphabet.index(char.lower())
        except ValueError:
            continue  # Skip characters not in the alphabet

        if char.islower():
            ciphertext += key[alphabet_index].lower()
        else:
            ciphertext += key[alphabet_index]

    print(f"ciphertext: {ciphertext}")
    return 0

if __name__ == "__main__":
    if len(sys.argv[1]) != 26:
        sys.exit(1)
    main(sys.argv[1])
