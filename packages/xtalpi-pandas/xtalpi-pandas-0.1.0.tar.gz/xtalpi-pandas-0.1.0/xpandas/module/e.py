from xpandas.module.utils import show_col_names


def handle_col(df):
    col_names = show_col_names(df)
    while True:
        col_name = input('想要按照哪一列进行选取? :')
        if col_name in col_names:
            break
        else:
            print('列名错误，请重新输入')

    while True:
        print('数值型：[1.<][2.<=][3.=][4.>][5.>=]')
        print('字符串型：[6.包含][7.不包含]')
        cmd = input('请从1-7中选择一个操作：')

        if cmd == '1':
            threshold = input('请输入阈值：')
            df_new = df.loc[df[col_name] < float(threshold)]
            break
        elif cmd == '2':
            threshold = input('请输入阈值：')
            df_new = df.loc[df[col_name] <= float(threshold)]
            break
        elif cmd == '3':
            threshold = input('请输入阈值：')
            df_new = df.loc[df[col_name] == float(threshold)]
            break
        elif cmd == '4':
            threshold = input('请输入阈值：')
            df_new = df.loc[df[col_name] > float(threshold)]
            break
        elif cmd == '5':
            threshold = input('请输入阈值：')
            df_new = df.loc[df[col_name] >= float(threshold)]
            break
        elif cmd == '6':
            threshold = input('请输入字符：')
            df_new = df.loc[df[col_name].str.contains(threshold)]
            break
        elif cmd == '7':
            threshold = input('请输入字符：')
            df_new = df.loc[df[col_name].str.contains(threshold) == False]
            break
        else:
            print('输入错误！请从1至7中选择一个操作！')
    return df_new


def extract_csv(df, csv):
    while True:
        df = handle_col(df)
        row = df.shape()[0]
        print('按照条件获取了%s条数据' % row)
        go_on = input('\n是否继续提取？[1.是][2.否]：')
        if go_on != '1':
            df.to_csv(csv.replace('.csv', '_extract' + '.csv'), index=False)
            break
