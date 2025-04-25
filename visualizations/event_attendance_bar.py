import pandas as pd
import matplotlib.pyplot as plt

# goal -> create a plot showing how attendance changes over time

df = pd.read_csv('event_date+attendance.csv') # read the file
df = df.rename(columns={"Event Date" : "Date"}) # rename the event date to date

df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, errors='coerce') # use datetime to format the dates

df = df.dropna(subset = ['Date', 'Attendance']) # drop any missing values
df = df.sort_values('Date') # sort the dates from earliest to latest

df['Month'] = df['Date'].dt.month

def get_sector(month): # this function is used to separate the months into 4 sectors
    if month in [1, 2, 3]:
        return 'Q1 (Jan-Mar)'
    elif month in [4, 5, 6]:
        return 'Q2 (Apr-Jun)'
    elif month in [7, 8, 9]:
        return 'Q3 (Jul-Sep)'
    else:
        return 'Q4 (Oct-Dec)'

df['Sector'] = df['Month'].apply(get_sector)

sector_avg = df.groupby('Sector')['Attendance'].mean().reindex(['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (Jul-Sep)',
                                                                'Q4 (Oct-Dec)'])
# found the average attendance of each sector

#plot

plt.figure(figsize=(8, 5))
sector_avg.plot(kind='bar', color='skyblue', edgecolor='black')
plt.ylabel('Average Attendance')
plt.title('Average Attendance During Calendar Year (2022 - 2025)')
plt.xticks(rotation=30)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
