
def cal_mean(df, col):
    return df[col].mean()


def cal_median(df, col):
    return df[col].median()


def cal_mode(df, col):
    return df[col].mode()[0]


def cal_min(df, col):
    return df[col].min()


def cal_max(df, col):
    return df[col].max()


def cal_quantile(df, col, q):
    return df[col].quantile(q)
