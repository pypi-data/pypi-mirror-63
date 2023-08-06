from xpandas.module.utils import show_col_names


def top_csv(df, csv):
    col_names = show_col_names(df)

    while True:
        col_name = input('\n想要按照哪一列进行TOP? :')
        if col_name in col_names:
            break
        else:
            print('列名错误，请重新输入')
    while True:
        print('\n[1.升序(值越小越好)]或[2.降序(值越大越好)]')
        assending_num = input('请输入1或2选择排列方式：')
        if assending_num == '1':
            assending = True
            break
        elif assending_num == '2':
            assending = False
            break
        else:
            print('请从1或2中选择一个')

    row = df.shape[0]
    while True:
        print('\ncsv共有%s行' % row)
        top_num = int(input('想要Top前多少行？：'))
        if 0 < top_num <= row:
            break
        else:
            print('\n输入错误，请输入1至%s之间的数！' % row)
    top_df = df.sort_values(col_name, ascending=assending)[:top_num]
    top_df.to_csv(csv.replace('.csv', '_top'+str(top_num)+'.csv'), index=False)
