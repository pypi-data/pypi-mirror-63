import math


def chunk_func(arr, n):
    m = int(math.ceil(len(arr) / float(n)))
    for i in range(0, len(arr), m):
        yield arr[i:i + m]


def chunk_csv(df, csv):
    row = df.shape[0]
    while True:
        print('\ncsv共有%s行' % row)
        n = int(input('将csv按行平均分为几份? :'))
        if 0 < n <= row:
            break
        else:
            print('\n输入错误，请输入1至%s之间的数！' % row)

    for idx, i in enumerate(chunk_func([i for i in range(df.shape[0])], n)):
        df.loc[i].to_csv(csv.replace('.csv', '_' + str(idx) + '.csv'), index=False)
