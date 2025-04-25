import pandas as pd

def load_event_attendance_data():
    df = pd.read_csv("Cleaned_Event_Attendance.csv")
    df['event_date'] = pd.to_datetime(df['event_date'])
    df['day_of_week'] = df['event_date'].dt.day_name()
    df['month'] = df['event_date'].dt.month

    return df

def load_company_data():
    df = pd.read_csv("Cleaned_Company_Visits.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["company"] = df["company"].str.strip().str.lower()
    return df
