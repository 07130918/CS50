# ユーザにお釣りを渡すために必要なコインの最小数を計算するプログラム
# コインは25セント，10セント，5セント，1セント
from retry import retry


def main():
    coin = 0
    owed_cent = check_input_val()
    print(calculate(coin, owed_cent))


@retry()
def check_input_val():
    print('Change owed:', end='')
    owed_cent = float(input()) * 100
    if owed_cent < 0:
        raise Exception
    return owed_cent


def calculate(coin, owed_cent):
    # basecase
    if owed_cent == 0:
        return coin

    if owed_cent >= 25:
        coin += 1
        owed_cent -= 25
        return calculate(coin, owed_cent)
    elif owed_cent >= 10:
        coin += 1
        owed_cent -= 10
        return calculate(coin, owed_cent)
    elif owed_cent >= 5:
        coin += 1
        owed_cent -= 5
        return calculate(coin, owed_cent)
    elif owed_cent >= 1:
        coin += 1
        owed_cent -= 1
        return calculate(coin, owed_cent)


if __name__ == '__main__':
    main()
