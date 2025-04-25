import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_month_hour_attendance_heatmap(csv, save_path='heatmap_month_hour.png'):
    df = pd.read_csv(csv)

    # Drops the month column (since rows are empty)
    df = df.drop(columns=[df.columns[0]])

    df.set_index('Start Hour', inplace=True)

    plt.figure(figsize=(10, 6))
    sns.heatmap(df, annot=True, fmt='d', cmap='Reds')  
    plt.title('Attendance Heatmap by Month and Start Hour')
    plt.ylabel('Start Hour')
    plt.xlabel('Month')
    plt.tight_layout()

    plt.savefig(save_path)
