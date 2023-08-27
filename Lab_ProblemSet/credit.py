# クレジットカード番号から会社の特定(Luhnのアルゴリズム)
# https://cs50.jp/x/2021/week6/problem-set/credit/
# American Expressは15桁、MasterCardは16桁、Visaは13桁あるは16桁

def main():
    print('Number: ', end='')
    credit_card_number = input()
    reverse_num = credit_card_number[::-1]
    valid_card = card_confirm(reverse_num)
    if not valid_card:
        print('INVALID')
        return

    print(find_company(credit_card_number))


def card_confirm(credit_card_number):
    sum = 0
    odd_index_sum = 0
    for i in range(len(credit_card_number)):
        if i % 2 == 1:
            # 6 * 2で12になった時(2桁になった場合), 1 + 2に分ける
            if int(credit_card_number[i]) * 2 >= 10:
                sum += 1
                sum += int(credit_card_number[i]) * 2 - 10
            else:
                sum += int(credit_card_number[i]) * 2
        else:
            odd_index_sum += int(credit_card_number[i])

    if (sum + odd_index_sum) % 10 == 0:
        return True
    else:
        return False


def find_company(credit_card_number):
    if int(credit_card_number[0]) == 3 and int(credit_card_number[1]) == (4 or 7):
        return 'AMEX'
    elif int(credit_card_number[0]) == 5 and int(credit_card_number[1]) in range(1, 6):
        return 'Master'
    elif int(credit_card_number[0]) == 4:
        return 'Visa'


if __name__ == '__main__':
    main()
