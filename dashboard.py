import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from backend.recommendation_engine import recommend_schedule, recommend_companies, find_popular_companies, find_company_name
from backend.load_data import load_company_data, load_event_attendance_data
from backend.DOW_hour import generate_DOW_hour_attendance_heatmap
from backend.month_DOW import generate_month_DOW_attendance_heatmap
from backend.month_hour import generate_month_hour_attendance_heatmap
import calendar

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Dashboard")

def clean_data (df):
    df = df.drop_duplicates()
    
    # remove all empty entries
    df = df.dropna()
    
    # Reset indexes
    df = df.reset_index(drop=True)

    return df

def load_data (default_path: str, file_type: str = "csv", key: str = "data_file_uploader",
               uploader_text = "Upload a new file to override"):
    uploaded_file = st.sidebar.file_uploader(
        uploader_text,
        type=["csv", "xlsx"],
        key=key
    )
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.sidebar.success("Uploaded file loaded successfully.")
            return df
        except Exception as e:
            st.sidebar.error(f"Failed to load uploaded file: {e}")
    try:
        if file_type == "csv":
            df = pd.read_csv(default_path)
        else:
            df = pd.read_excel(default_path)
        st.sidebar.info("Using default dataset from repository.")
        return df
    except Exception as e:
        st.sidebar.error(f"Failed to load default file: {e}")
        return pd.DataFrame()

tabs = st.tabs(["📊 Event Insights", "🔐 Login Trends", "🏢 Company Visits", "🧠 Recommendation Engine"])

cleaned_event_attendance = load_data("backend/Cleaned_Event_Attendance.csv",
                                     key = "Event_Attendance_Uploader",
                                     uploader_text = "Upload Event Attendance File Here")
cleaned_event_attendance = clean_data(cleaned_event_attendance)

cleaned_company_visits = load_data("backend/Cleaned_Company_Visits.csv",
                                   key = "Company_Visits_Uploader",
                                   uploader_text = "Upload Company Sectors File Here")

cleaned_company_visits = clean_data(cleaned_company_visits)

cleaned_event_attendance.columns = cleaned_event_attendance.columns.str.strip().str.lower().str.replace(" ", "_")
cleaned_event_attendance['event_date'] = pd.to_datetime(df['event_date'])
cleaned_event_attendance['day_of_week'] = cleaned_event_attendance['event_date'].dt.day_name()
cleaned_event_attendance['month'] = cleaned_event_attendance['event_date'].dt.month

cleaned_company_visits.columns = cleaned_company_visits.columns.str.strip().str.lower().str.replace(" ", "_")
cleaned_company_visits["company"] = cleaned_company_visits["company"].str.strip().str.lower()

with tabs[0]:
    st.header("Event Insights")

    df_date = cleaned_event_attendance.groupby("event_date")["attendance"].sum().reset_index()
    df_date.columns = ["Event Date", "Attendance"]
    df_date["Month"] = df_date["Event Date"].dt.month

    # Dropdown: Aggregation Option
    agg_option = st.selectbox("Aggregate Attendance By:", ["Quarter", "Month"])

    if agg_option == "Quarter":
        def get_sector(month):
            if month in [1, 2, 3]:
                return 'Q1 (Jan-Mar)'
            elif month in [4, 5, 6]:
                return 'Q2 (Apr-Jun)'
            elif month in [7, 8, 9]:
                return 'Q3 (Jul-Sep)'
            else:
                return 'Q4 (Oct-Dec)'

        df_date['Sector'] = df_date['Month'].apply(get_sector)

        grouped = df_date.groupby('Sector')['Attendance'].mean().reindex(
            ['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (Jul-Sep)', 'Q4 (Oct-Dec)']
        )

        x_labels = grouped.index

    else:  # Month
        grouped = df_date.groupby('Month')['Attendance'].mean()
        x_labels = [calendar.month_name[m] for m in grouped.index]

    # 📊 Bar Plot Only
    st.subheader(f"📊 Average Attendance by {agg_option}")

    fig, ax = plt.subplots(figsize=(8, 5))

    x_pos = range(len(x_labels))

    ax.bar(x_pos, grouped.values, color='skyblue', edgecolor='black')

    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_labels, rotation=30)
    ax.set_ylabel('Average Attendance')
    ax.set_title('Average Attendance During Calendar Year (2022 - 2025)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)

    # 📈 Top Event Types by Attendance
    st.subheader("🏆 Top Event Types by Total Attendance")

    event_totals = cleaned_event_attendance.groupby('event_type')['attendance'].sum()
    top_events = event_totals.sort_values(ascending=False).head(10)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.barh(top_events.index, top_events.values, color='deepskyblue')
    ax2.set_xscale('log')

    tick_vals = [100, 300, 1000, 3000, 10000, 30000, 100000]
    ax2.set_xticks(tick_vals)
    ax2.set_xticklabels([f'{int(t):,}' for t in tick_vals])

    ax2.set_xlabel('Total Attendance')
    ax2.set_ylabel('Event Type')
    ax2.set_title('Top Event Types by Attendance')
    ax2.invert_yaxis()
    ax2.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig2)

# Tab 2: Login Trends
with tabs[1]:
    st.header("Login Trends")
    st.header("Month and Hour Heatmap")
    generate_month_hour_attendance_heatmap('backend/CLEANED_attendances_by_month_and_hour.csv')
    st.image('heatmap_month_hour.png', caption='Attendance by Month and Start Hour')

    st.header("Month and Day of Week Heatmap")
    generate_month_DOW_attendance_heatmap('backend/CLEANED_attendances_by_month_and_DOW.csv')
    st.image('heatmap_month_DOW.png', caption='Attendance by Month and Day of Week')

    st.header("Day of Week and Hour Heatmap")
    generate_DOW_hour_attendance_heatmap('backend/CLEANED_attendances_by_DOW_and_hour.csv')
    st.image('heatmap_DOW_hour.png', caption='Attendance by Day of Week and Start Hour')

# Tab 3: Company Visits
with tabs[2]:
    st.header("Company Visits")

    # Load and process data for company visits

    # Combine both business_sector_1 and business_sector_2
    sectors = pd.concat([
        cleaned_company_visits['business_sector_1'],
        cleaned_company_visits['business_sector_2'].dropna()
    ])

    sector_counts = sectors.value_counts()
    top_sectors = sector_counts.head(10)

    # Pie chart of top company sectors
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.pie(top_sectors, labels=top_sectors.index, autopct='%1.1f%%', startangle=140)
    ax3.set_title('Most Popular Company Sectors')
    ax3.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
    plt.tight_layout()

    st.pyplot(fig3)

    st.header("Company & Sector Analysis")

    analysis = find_popular_companies(cleaned_event_attendance, cleaned_company_visits)

    st.subheader("Company Attendance Ranking")
    st.dataframe(analysis["company_rank"])

    st.subheader("Average Attendance by Business Sector")
    st.dataframe(analysis["sector_avg"])

# Tab 4: Recommendation Engine
with tabs[3]:

    # Recommended Event Strategy Section
    st.header("Recommendation Engine")
    st.subheader("Recommended Event Strategy:")
    newDF = recommend_schedule(cleaned_event_attendance)
    st.markdown(f"Best Day of the Week: {newDF['best_day']}")
    st.markdown(f"Best Month: {newDF['best_month']}")
    st.markdown(f"Most Successful Event Type: {newDF['best_type']}")
    st.dataframe(newDF["ranked_days"])

    # Combine both business_sector_1 and business_sector_2
    sectors = pd.concat([
        cleaned_company_visits['business_sector_1'],
        cleaned_company_visits['business_sector_2'].dropna()
    ])
    
    #Underepresented Sectors Section
    st.subheader("Underrepresented Sectors")
    if analysis["underrepresented_sectors"]:
        for sector in analysis["underrepresented_sectors"]:
            st.markdown(f"- {sector}")
    else:
        st.markdown("No underrepresented sectors found.")


    company_names = cleaned_company_visits['company'].dropna().unique().tolist()
    selected_company = st.selectbox("Select a company you've visited", company_names)


    if selected_company:
        st.subheader(f"Companies similar to **{selected_company}** based on business sectors")
        recommendations_df = recommend_companies(selected_company, cleaned_company_visits, cleaned_event_attendance)

        if not recommendations_df.empty:
            st.dataframe(recommendations_df.reset_index(drop=True), use_container_width=True)
        else:
            st.info("No similar companies found based on previous visit data.")
