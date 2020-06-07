#!/usr/bin/python3
'''
https://medium.com/dunder-data
https://medium.com/dunder-data/create-a-bar-chart-race-animation-in-python-with-matplotlib-477ed1590096

COVID-19 deaths data

For this bar chart race, we’ll use a small dataset produced by John Hopkins University containing the total deaths by infodate for six countries during the currently ongoing coronavirus pandemic. Let’s read it in now.

'''

import pandas as pd
df = pd.read_csv('data/covid19.csv', index_col='infodate',
                  parse_dates=['infodate'])
df.tail()
s = df.loc['2020-03-29']
'''
China     3304.0
USA       2566.0
Italy    10779.0
UK        1231.0
Iran      2640.0
Spain     6803.0
Name: 2020-03-29 00:00:00, dtype: float64
'''

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4, 2.5), dpi=144)
colors = plt.cm.Dark2(range(6))
y = s.index
width = s.values
ax.barh(y=y, width=width, color=colors);

def nice_axes(ax):
  ax.set_facecolor('.8')
  ax.tick_params(labelsize=8, length=0)
  ax.grid(True, axis='x', color='white')
  ax.set_axisbelow(True)
  [spine.set_visible(False) for spine in ax.spines.values()]


nice_axes(ax)
fig

fig, ax_array = plt.subplots(nrows=1, ncols=3, figsize=(7, 2.5), dpi=144, tight_layout=True)
dates = ['2020-03-29', '2020-03-30', '2020-03-31']
for ax, date in zip(ax_array, dates):
  s = df.loc[date].sort_values()
  ax.barh(y=s.index, width=s.values, color=colors)
  ax.set_title(date, fontsize='smaller')
  nice_axes(ax)

df.loc['2020-03-29'].rank(method='first')

'''
China    4.0
USA      2.0
Italy    6.0
UK       1.0
Iran     3.0
Spain    5.0
Name: 2020-03-29 00:00:00, dtype: float64
'''
fig, ax_array = plt.subplots(nrows=1, ncols=6, figsize=(12, 2),
                             dpi=144, tight_layout=True)
df2 = df.loc['2020-03-29':'2020-03-31']
df2 = df2.reset_index()

df2.index = df2.index * 5

last_idx = df2.index[-1] + 1
df_expanded = df2.reindex(range(last_idx))

df_expanded['infodate'] = df_expanded['infodate'].fillna(method='ffill')
df_expanded = df_expanded.set_index('infodate')

df_rank_expanded = df_expanded.rank(axis=1, method='first')

df_expanded = df_expanded.interpolate()

df_rank_expanded = df_rank_expanded.interpolate()

labels = df_expanded.columns
for i, ax in enumerate(ax_array.flatten()):
    y = df_rank_expanded.iloc[i]
    width = df_expanded.iloc[i]
    ax.barh(y=y, width=width, color=colors, tick_label=labels)
    nice_axes(ax)
ax_array[0].set_title('2020-03-29')
ax_array[-1].set_title('2020-03-30');

fig, ax_array = plt.subplots(nrows=1, ncols=6, figsize=(12, 2),
                             dpi=144, tight_layout=True)
labels = df_expanded.columns
for i, ax in enumerate(ax_array.flatten(), start=5):
    y = df_rank_expanded.iloc[i]
    width = df_expanded.iloc[i]
    ax.barh(y=y, width=width, color=colors, tick_label=labels)
    nice_axes(ax)
ax_array[0].set_title('2020-03-30')
ax_array[-1].set_title('2020-03-31');


def process():
  pass

if __name__ == '__main__':
  process()