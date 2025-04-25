import streamlit as st
from recommendation_engine import recommend_schedule, recommend_companies, find_popular_companies, find_company_name
from load_data import load_company_data, load_event_attendance_data
from month_hour import generate_month_hour_attendance_heatmap
from month_DOW import generate_month_DOW_attendance_heatmap
from DOW_hour import generate_DOW_hour_attendance_heatmap

st.set_page_config(page_title="VMSC Event Dashboard", layout="wide")
st.title("VMSC Event Recommendation")

df_events = load_event_attendance_data()
df_companies = load_company_data()


st.subheader("Event Attendance Data")
st.dataframe(df_events)

st.subheader("Company Visit Data")
st.dataframe(df_companies)

st.header("Recommended Event Strategy:")
recommendations = recommend_schedule(df_events)
st.markdown(f"Best Day of the Week: {recommendations['best_day']}")
st.markdown(f"Best Month: {recommendations['best_month']}")
st.markdown(f"Most Successful Event Type: {recommendations['best_type']}")

st.subheader("Ranked Days by Average Attendance (Excluding Field of Flags and Military Appreciation Tailgate)")
st.dataframe(recommendations["ranked_days"])


st.header("Company & Sector Analysis")

analysis = find_popular_companies(df_events, df_companies)

st.subheader("Company Attendance Ranking")
st.dataframe(analysis["company_rank"])

st.subheader("Average Attendance by Business Sector")
st.dataframe(analysis["sector_avg"])

st.subheader("Underrepresented Sectors")
if analysis["underrepresented_sectors"]:
    for sector in analysis["underrepresented_sectors"]:
        st.markdown(f"- {sector}")
else:
    st.markdown("No underrepresented sectors found.")


company_names = df_companies['company'].dropna().unique().tolist()
selected_company = st.selectbox("Select a company you've visited", company_names)


if selected_company:
    st.subheader(f"Companies similar to **{selected_company}** based on business sectors")
    recommendations_df = recommend_companies(selected_company, df_companies, df_events)

    if not recommendations_df.empty:
        st.dataframe(recommendations_df.reset_index(drop=True), use_container_width=True)
    else:
        st.info("No similar companies found based on previous visit data.")


st.header("Month and Hour Heatmap")
generate_month_hour_attendance_heatmap('CLEANED_attendances_by_month_and_hour.csv')
st.image('heatmap_month_hour.png', caption='Attendance by Month and Start Hour')

st.header("Month and DOW Heatmap")
generate_month_DOW_attendance_heatmap('CLEANED_attendances_by_month_and_DOW.csv')
st.image('heatmap_month_DOW.png', caption='Attendance by Month and Day of Week')

st.header("DOW and Hour Heatmap")
generate_DOW_hour_attendance_heatmap('CLEANED_attendances_by_DOW_and_hour.csv')
st.image('heatmap_DOW_hour.png', caption='Attendance by Day of Week and Start Hour')
