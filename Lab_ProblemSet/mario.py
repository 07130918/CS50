def main():
    height = 10
    while height > 8 and type(height) is not str:
        print('height: ', end='')
        height = int(input())
    return draw(height)


def draw(height):
    # basecase
    if(height == 0):
        return

    draw(height - 1)
    for _ in range(height):
        print("■", end='')
    print()


if __name__ == '__main__':
    main()
