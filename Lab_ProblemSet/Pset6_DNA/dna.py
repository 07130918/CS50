# DNA塩基配列から個人を特定するプログラム
# https://cs50.jp/x/2021/week6/problem-set/dna/
import csv
import sys


def main(dna_database, text_file):
    sequence = get_sequence(text_file)
    short_tandem_repeats = get_short_tandem_repeats(dna_database)
    dna_pattern = create_dna_pattern_dict(short_tandem_repeats, sequence)

    print(search_person(dna_database, dna_pattern))


def get_sequence(file):
    with open(file, "r") as f:
        return f.read().replace('\n', '')


def get_short_tandem_repeats(dna_database):
    with open(dna_database, "r") as file:
        short_tandem_repeats_list = file.readlines()[0].replace('\n', '').split(',')
        short_tandem_repeats_list.pop(0)
    return short_tandem_repeats_list


def create_dna_pattern_dict(short_tandem_repeats, sequence):
    dna_pattern_dict = {}
    for i in short_tandem_repeats:
        dna_pattern_dict[i] = str(get_repeat_count(i, sequence.count(i), sequence))
    return dna_pattern_dict


def get_repeat_count(i, repeat_count, sequence):
    """DNA配列(i)がsequence文字列に連続で出現する最大回数を求める再帰関数"""
    if i * repeat_count in sequence:
        return repeat_count

    return get_repeat_count(i, repeat_count - 1, sequence)


def search_person(dna_database, dna_pattern):
    with open(dna_database, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row.pop('name')
            if row == dna_pattern:
                return name
    return 'No match'


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
