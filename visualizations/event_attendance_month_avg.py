import pandas as pd
import matplotlib.pyplot as plt

# goal -> create a plot showing how attendance changes over time

df = pd.read_csv('event_date+attendance.csv') # read the file
df = df.rename(columns={"Event Date" : "Date"}) # rename the event date to date

df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, errors='coerce') # use datetime to format the dates

df = df.dropna(subset = ['Date', 'Attendance']) # drop any missing values
df = df.sort_values('Date') # sort the dates from earliest to latest

df['Month'] = df['Date'].dt.month

df['Month'] = df['Date'].dt.month_name()
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
               'November', 'December']

monthly_avg = df.groupby('Month')['Attendance'].mean().reindex(month_order)

#plot
plt.figure(figsize=(10, 5))
plt.plot(monthly_avg.index, monthly_avg.values, marker='o', linestyle='-')
plt.title('Average Attendance per Month')
plt.ylabel('Average Attendance')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
