def main():
    height = int(input("height: ").strip())
    draw(height)

def draw(h: int):
    # Never forget the base case in recursion
    if h == 0:
        return

    draw(h - 1)
    print("■" * h)

if __name__ == "__main__":
    main()
