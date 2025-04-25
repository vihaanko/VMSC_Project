import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_month_DOW_attendance_heatmap(csv, save_path='heatmap_month_DOW.png'):
    df = pd.read_csv(csv, index_col=0)

    plt.figure(figsize=(10, 6))
    sns.heatmap(df, annot=True, fmt='d', cmap='Reds')
    plt.title('Attendance Heatmap by Month and Day of Week')
    plt.ylabel('Day of Week')
    plt.xlabel('Month')
    plt.tight_layout()

    plt.savefig(save_path)
