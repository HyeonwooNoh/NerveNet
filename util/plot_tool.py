import pandas as pd

from matplotlib import pyplot as plt

PALETTE = [
    '#332288',  # indigo
    '#88cc33',  # cyan
    '#44aa99',  # teal
    '#117733',  # green
    '#999933',  # olive
    '#ddcc77',  # sand
    '#cc6677',  # rose
    '#882255',  # wine
    '#aa4499',  # purple
    '#dddddd',  # pale gray
]


def plot(data_list, x_key, y_key, legend_key, separate_keys=[], linewidth=1, avg_window=1):
    df_list = []
    for lid, data in enumerate(data_list):
        df = pd.DataFrame(data)
        df['lid'] = lid
        df_list.append(df)
    df = pd.concat(df_list)

    df = df.set_index(x_key).sort_index()

    line_idx = 0
    ret_legend_names = []
    if len(separate_keys) == 0:
        legend_names = list(set(df[legend_key]))
        for legend_name in legend_names:
            legend_df = df.loc[df[legend_key] == legend_name]
            lids = list(set(legend_df['lid']))
            lid_series = pd.concat([legend_df.loc[legend_df['lid'] == lid][y_key] for lid in lids], axis=1)
            lid_series = lid_series.rolling(window=avg_window).mean()
            line_mean = lid_series.mean(axis=1)
            line_std = lid_series.std(axis=1)
            linecolor = PALETTE[line_idx]
            plt.plot(lid_series.index, line_mean, color=linecolor, linewidth=linewidth)
            plt.fill_between(lid_series.index, line_mean - line_std, line_mean + line_std, alpha=0.2, facecolor=linecolor)
            ret_legend_names.append(legend_name)
            line_idx += 1
    else:
        raise NotImplementedError('TODO')
    return ret_legend_names
