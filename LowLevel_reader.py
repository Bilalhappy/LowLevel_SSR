import pandas as pd
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
import matplotlib.dates as md
from matplotlib.lines import Line2D

df = pd.read_csv("lowlevel",sep="\s+",header = None)
df[2] = pd.to_timedelta(df[2],"D" )
df[3] = pd.to_timedelta(df[3],"S" )
df[2] = dt.strptime("1950-01-01","%Y-%m-%d")+df[3] +df[2] 

df2 = df.sort_values(by=[1,2],ignore_index=True)

df2 = df2.drop(list(df2)[41:], axis=1)
df2 = df2.drop(list(df2)[3:31], axis=1)
df2 = df2[~df2[1].str.startswith('R')]
df2['t_f'] = (df2[31] == df2[32]) & (df2[33] == df2[34]) & (df2[35] == df2[36]) & (df2[37] == df2[38]) & (df2[39] == df2[40])
del df2[0]

E_df = df2[df2[1].str.startswith('E')]
G_df = df2[df2[1].str.startswith('G')]

industries = E_df.groupby(1)

fig = plt.figure()
cmap = clrs.ListedColormap(['green', 'red'])
ax = fig.add_subplot(111)
plt.rcParams["figure.autolayout"] = True
i = 0
labels = []

for k in industries.groups:
    industry = industries.get_group(k)
    epok = industry[2].tolist()
    new_index = pd.date_range(start=dt.strftime(epok[0],"%Y-%m-%d %H:%M:%S"), end=dt.strftime(epok[-1],"%Y-%m-%d %H:%M:%S"), freq='5s')
    industry = industry.set_index([1, 2])
    industry = industry.reindex(new_index, level=2, fill_value= True)
    labels.append(industry.index.levels[0].tolist()[0])
    print(industry.index.levels[0].tolist()[0],":",("Available : %"+str(round(industry['t_f'].value_counts(normalize=True).mul(100).get(0),1))),("Not-Available : %"+str(industry['t_f'].value_counts(normalize=True).mul(100).get(1))))
    industry = industry.reset_index(level=[1])
    ax.scatter(x = industry.index, y= [i for l in range(len(industry.t_f))], c=(industry.t_f != True).astype(float), marker='d',s=2, cmap=cmap)#plt.cm.get_cmap('RdBu'))
    i += 1

industries = G_df.groupby(1)
for k in industries.groups:
    industry = industries.get_group(k)
    epok = industry[2].tolist()
    new_index = pd.date_range(start=dt.strftime(epok[0],"%Y-%m-%d %H:%M:%S"), end=dt.strftime(epok[-1],"%Y-%m-%d %H:%M:%S"), freq='5s')
    industry = industry.set_index([1, 2])
    industry = industry.reindex(new_index, level=2, fill_value= True)
    labels.append(industry.index.levels[0].tolist()[0])
    print(industry.index.levels[0].tolist()[0],":",("Available : %"+str(round(industry['t_f'].value_counts(normalize=True).mul(100).get(0),1))),("Not-Available : %"+str(industry['t_f'].value_counts(normalize=True).mul(100).get(1))))
    industry = industry.reset_index(level=[1])
    ax.scatter(x = industry.index, y= [i for l in range(len(industry.t_f))], c=(industry.t_f != True).astype(float), marker='d',s=2, cmap=cmap)#plt.cm.get_cmap('RdBu'))
    i += 1

ax.set_yticks(np.arange(len(labels)))
ax.set_yticklabels(labels)

ax.xaxis.set_major_locator(md.HourLocator(interval = 3))
ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
#plt.xlim(dt.strptime("2023-08-05 00:00:00","%Y-%m-%d %H:%M:%S"), dt.strptime("2023-08-06 00:00:00","%Y-%m-%d %H:%M:%S"))

handles, labels = plt.gca().get_legend_handles_labels()
point = Line2D([0], [0], label='Available', marker='o', markersize=5, 
         markeredgecolor='g', markerfacecolor='g', linestyle='')
point2 = Line2D([0], [0], label='Not-Available', marker='o', markersize=5, 
         markeredgecolor='g', markerfacecolor='r', linestyle='')
handles = [point,point2]

ax.set_ylabel('Satellite Number',fontsize = 10)
ax.set_xlabel('Time (UTC)',fontsize = 10)

ax.tick_params(axis='y', labelsize=6)
plt.title("SSR Products Availability",fontsize = 14)
plt.legend(loc='upper right',handles=handles,ncol = 2,fontsize = 7)
plt.savefig("availability.png", bbox_inches = 'tight', dpi=300, pad_inches = 0.02)
plt.close()
