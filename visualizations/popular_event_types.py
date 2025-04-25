import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Cleaned_Event_Attendance.csv')

event_totals = df.groupby('event_type')['attendance'].sum()

top_events = event_totals.sort_values(ascending = False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_events.index, top_events.values, color='deepskyblue')
plt.xscale('log')

tick_vals = [100, 300, 1000, 3000, 10000, 30000, 100000]
plt.xticks(tick_vals, [f'{int(t):,}' for t in tick_vals])

plt.xlabel('Total Attendance')
plt.ylabel('Event Type')
plt.title('Top Event Types by Attendance')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
