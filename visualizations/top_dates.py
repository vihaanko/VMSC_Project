import pandas as pd

df = pd.read_csv('Cleaned_Event_Attendance.csv')

df['event_date'] = pd.to_datetime(df['event_date'])

top_dates = df.groupby('event_date')['attendance'].sum().sort_values(ascending=False)

print("Top 10 event dates by total attendance:")
print(top_dates.head(10))
