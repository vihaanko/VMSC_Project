import pandas as pd
import calendar

def recommend_schedule(df):
    # Remove outliers (Field of Flags and Military Appreciation Tailgate)
    df = df[~df['event_name'].str.lower().isin(['field of flags', 'military appreciation tailgate'])]
    # Ranks weekdays by average attendance
    weekday_avg = df.groupby('day_of_week')['attendance'].mean().sort_values(ascending=False)

    # Finds the best day and month
    best_day = weekday_avg.idxmax()
    best_month = df.groupby('month')['attendance'].mean().idxmax()
    best_type = df.groupby('event_type')['attendance'].mean().idxmax()

    return {
        "best_day": best_day,
        "best_month": calendar.month_name[best_month],
        "best_type": best_type,
        "ranked_days": weekday_avg.reset_index().rename(columns={"attendance": "average_attendance"})
    }

def recommend_companies(selected_company, df_companies, df_events):
    # Filters to the rows with Office Visits as teh event type
    office_visits = df_events[df_events['event_type'] == 'Office Visits'].copy()

    # Gets company name from event name by checking if its mentioned
    office_visits['company'] = office_visits['event_name'].apply(
        lambda name: next((comp for comp in df_companies['company'] if comp.lower() in name.lower()), None)
    )

    office_visits = office_visits.dropna(subset=['company'])

    # Merges office visit data with company info using the name as the key
    merged_df = office_visits.merge(df_companies, on='company', how='left')

    # Returns empty if selected company isn't in dataset
    if selected_company not in merged_df['company'].values:
        return pd.DataFrame(columns=merged_df.columns)

    # Get the business sectors for company
    sectors = merged_df[merged_df['company'] == selected_company][['business_sector_1', 'business_sector_2']].iloc[0]

    # Recommends other companies that share atleast one of the two business sectors (For Comparisons)
    recommendations = merged_df[
        ((merged_df['business_sector_1'] == sectors['business_sector_1']) |
         (merged_df['business_sector_2'] == sectors['business_sector_1']) |
         (merged_df['business_sector_1'] == sectors['business_sector_2']) |
         (merged_df['business_sector_2'] == sectors['business_sector_2']))
        & (merged_df['company'] != selected_company)
    ]

    return recommendations[['company', 'business_sector_1', 'business_sector_2']].drop_duplicates()

def find_popular_companies(df_events, df_companies):
    office_visits = df_events[df_events['event_type'] == 'Office Visits'].copy()

    # Remove outliers (Field of Flags and Military Appreciation Tailgate)
    office_visits = office_visits[~office_visits['event_name'].str.lower().isin(['field of flags', 'military appreciation tailgate'])]

    # Matches company names from events
    office_visits['company_matched'] = office_visits['event_name'].apply(lambda x: find_company_name(x.lower()))
    df_companies['company_lower'] = df_companies['company'].str.lower()

    # Merges event attendance data with company data 
    merged = pd.merge(
        office_visits,
        df_companies,
        left_on='company_matched',
        right_on='company_lower',
        how='left'
    )

    # Creates ranking of companies based on total attendance
    company_rank = merged.groupby('company')['attendance'].sum().sort_values(ascending=False).reset_index()

    # Average attendance per sector_1
    sector_avg = merged.groupby('business_sector_1')['attendance'].mean().sort_values(ascending=False).reset_index()

    # Counts how many times each sector appears and identifies underrepresented sectors
    sector_attendance_counts = merged['business_sector_1'].value_counts()
    underrepresented_sectors = sector_attendance_counts[sector_attendance_counts < 2].index.tolist()

    return {
        "company_rank": company_rank,
        "sector_avg": sector_avg,
        "underrepresented_sectors": underrepresented_sectors
    }

def find_company_name(event_name):
    company_names = [
        'wabash', 'lockheed martin', 'scientific research corporation', 'linear logistics', 'ups',
        'indiana packers', 'caterpillar', 'parallax', 'owens corning', 'cascade', 'warrant tech'
    ]

    # Searches for the first company name that appears in the event name
    for name in company_names:
        if name in event_name:
            return name
    return ""
