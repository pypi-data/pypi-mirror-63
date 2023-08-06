import math


def chunk_func(arr, n):
    m = int(math.ceil(len(arr) / float(n)))
    for i in range(0, len(arr), m):
        yield arr[i:i + m]


def chunk_csv(df, csv):
    row = df.shape[0]
    print('\ncsv共有%s行' % row)
    n = int(input('将csv按行平均分为几份? :'))
    for idx, i in enumerate(chunk_func([i for i in range(df.shape[0])], n)):
        df.loc[i].to_csv(csv.replace('.csv', '_' + str(idx) + '.csv'), index=False)
