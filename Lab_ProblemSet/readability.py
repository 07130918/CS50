# L は100語あたりの平均字数、Sは100語あたりの平均文数
# Coleman_Liau_index = 0.0588 * L - 0.296 * S - 15.8
import re


def main():
    print('TEXT: ', end='')
    text = input()
    sentences_count, words_count, letters_count = inspect_count(text)
    print(judge_grade(sentences_count, words_count, letters_count))


def inspect_count(text):
    sentences = re.split(r'[?]|[!]|[.]', text)
    sentences_count = len(list(filter(None, sentences)))
    words_count = len(text.split())
    letters_count = 0
    for i in text:
        if re.match(r'[a-zA-Z]', i):
            letters_count += 1
    return sentences_count, words_count, letters_count


def judge_grade(sentences_count, words_count, letters_count):
    L = letters_count / words_count * 100
    S = sentences_count / words_count * 100
    Coleman_Liau_index = round(0.0588 * L - 0.296 * S - 15.8)
    if Coleman_Liau_index >= 16:
        return 'Grede 16+'
    elif Coleman_Liau_index < 1:
        return 'Before Grade 1'
    else:
        return f'Grade {Coleman_Liau_index}'


if __name__ == '__main__':
    main()
