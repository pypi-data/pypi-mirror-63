import pandas as pd
from tabulate import tabulate


def stats_output(data):
    if isinstance(data, pd.Series):
        df = pd.DataFrame(data)
        print(tabulate(df, tablefmt='psql'))
        print(f'共{df.shape[0]}项数据')
        print("----------Your data is a pandas series, i.e. use series['罚球'] to select data----------")
    elif isinstance(data, pd.DataFrame):
        print(tabulate(data, headers='keys', tablefmt='psql'))
        print(f'数据共{data.shape[0]}行，{data.shape[1]}列.')
        print("----------Your data is a pandas dataframe----------")
    else:
        print(tabulate(data, tablefmt='psql'))
        print(
            '----------You data is not a series or dataframe. Output may not reflect the true data structure----------')


class GameStats(object):
    """
    GameStats can be initialized by a dataframe or use 'from_csv' method to initialize from a csv file.
    """
    def __init__(self, df):
        df.loc[df['球员'] == '10', '球员'] = '田宇恒'
        self.__raw_stats = df

    def __repr__(self):
        return 'Please use "all_games_stats" property to check all raw stats.'

    def __str__(self):
        return str(self.__raw_stats)

    @classmethod
    def from_csv(cls, path):
        games_stats = pd.read_csv(path, encoding='UTF-8',
                                  dtype={'Game_ID': object, '号码': object})
        # as of 2020-01-01, 10 is 田宇恒
        games_stats.loc[games_stats['球员'] == '10', '球员'] = '田宇恒'
        return GameStats(games_stats)

    @property
    def all_games_stats(self):
        return self.__raw_stats

    def head(self):
        return self.__raw_stats.head()
