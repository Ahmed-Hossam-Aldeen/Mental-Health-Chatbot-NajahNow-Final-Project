from nltk import ngrams
import pandas as pd
import collections


def create_grams(file_path):
    dep = pd.read_excel(file_path)
    s = ''
    dep.dropna(inplace=True, axis=0)
    count = 0
    for i in dep.post:
        if type(i) != str:
            continue
        s = s + ' ' + i
        count += 1
        if count % 1000 == 0:
            print(f'Processed {count}')
    for i in range(1, 21):
        print(f'Creating {i}-grams')
        grams = ngrams(s.split(), i)
        gramsFrqq = collections.Counter(grams).most_common(100)
        print('Write to file')
        f = open(f'{i}-grams.txt', 'a')
        for gram in gramsFrqq:
            for g in gram[0]:
                f.write(g)
                f.write(' ')
            f.write(str(gram[1]))
            f.write('\n')
        f.close()
    print('Ended')


if __name__ == '__main__':
    files = []
