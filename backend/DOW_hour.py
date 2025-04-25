import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_DOW_hour_attendance_heatmap(csv, save_path='heatmap_DOW_hour.png'):
    df = pd.read_csv(csv)
    df = df.drop(columns=df.columns[0]) 

    df.set_index('Start Hour', inplace=True)

    plt.figure(figsize=(10, 6))
    sns.heatmap(df.T, annot=True, fmt='d', cmap='Reds')  # Transpose to put DOW as y-axis
    plt.title('Attendance Heatmap by Day of Week and Start Hour')
    plt.xlabel('Start Hour')
    plt.ylabel('Day of Week')
    plt.tight_layout()

    plt.savefig(save_path)
