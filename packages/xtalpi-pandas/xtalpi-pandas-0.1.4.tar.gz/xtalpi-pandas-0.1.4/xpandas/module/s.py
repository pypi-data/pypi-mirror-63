def split_func(arr, n):
    for i in range(0, len(arr), n):
        yield arr[i:i + n]


def split_csv(df, csv):
    row = df.shape[0]
    while True:
        print('\ncsv共有%s行' % row)
        n = int(input('每几行分割为一个csv? :'))
        if 0 < n <= row:
            break
        else:
            print('\n输入错误，请输入1至%s之间的数！' % row)

    for idx, i in enumerate(split_func([i for i in range(df.shape[0])], n)):
        df.loc[i].to_csv(csv.replace('.csv', '_' + str(idx) + '.csv'), index=False)
