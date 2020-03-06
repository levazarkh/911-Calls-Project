import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('911.csv')

#cheking info of a new DataFrame
# print(df.info())

#cheking head of DataFrame (first 5 rows)
# print(df.head(5))

#finding out the most common reason for a 911 call
df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
# print(df['Reason'].value_counts())
# sns.countplot(x='Reason',data=df,palette='viridis')
# plt.show()

print(type(df['timeStamp'].iloc[0]))
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)

dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)

#using seaborn plotting reasons for calls on different day of week
sns.countplot(x='Day of Week',data=df,hue='Reason',palette='viridis')
#getting legend in the top right corner so it doesn't interfere with a plot
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

#using seaborn plotting reasons for calls for month
sns.countplot(x='Month',data=df,hue='Reason',palette='viridis')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

#because month 9-11 are missing we use groupby to have an extimate of missing month
byMonth = df.groupby('Month').count()
# print(byMonth.head())
byMonth['twp'].plot()
plt.show()

sns.lmplot(x='Month',y='twp',data=byMonth.reset_index())
plt.show()

df['Date']=df['timeStamp'].apply(lambda t: t.date())
df.groupby('Date').count()['twp'].plot()
plt.tight_layout()
plt.show()

#different plots for every reason for a call
df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()
plt.show()

df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()
plt.show()

df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()
plt.show()

dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
# print(dayHour.head())

#creating heatmap
plt.figure(figsize=(12,6))
sns.heatmap(dayHour,cmap='viridis')
plt.show()

#creating clustermap
sns.clustermap(dayHour,cmap='viridis')
plt.show()

#same for month
dayMonth = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
# print(dayMonth.head())
plt.figure(figsize=(12,6))
sns.heatmap(dayMonth,cmap='viridis')
plt.show()
sns.clustermap(dayMonth,cmap='viridis')
plt.show()


