def main():
    word1 = input("Player 1: ").strip()
    word2 = input("Player 2: ").strip()
    score1 = compute_score(word1)
    score2 = compute_score(word2)

    if score1 > score2:
        print("Player 1 wins!")
    elif score1 < score2:
        print("Player 2 wins!")
    else:
        print("Tie!")

def compute_score(word: str) -> int:
    POINTS = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 0]
    alphabet = [chr(i) for i in range(97, 123)]  # 'a' to 'z'
    word = word.lower()
    score = 0

    for char in word:
        if not char.isalpha():
            continue
        alphabet_index = alphabet.index(char)
        score += POINTS[alphabet_index]

    return score

if __name__ == "__main__":
    main()
