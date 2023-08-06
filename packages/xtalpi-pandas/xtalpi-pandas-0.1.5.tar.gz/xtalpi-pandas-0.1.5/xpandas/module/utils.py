def show_col_names(df):
    col_names = list(df.columns)
    if len(col_names) <= 10:
        print('\n列名:', col_names)
    else:
        print('\n列名:', col_names + ['......'])
    return col_names

