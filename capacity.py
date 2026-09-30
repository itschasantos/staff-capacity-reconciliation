"""Staff capacity calculations extracted from original scheduling work."""
import pandas as pd

def build_staff_mapping(staff_mapping_list) -> pd.DataFrame:
    m = pd.DataFrame(staff_mapping_list).copy()
    m['StaffName'] = m['FirstName'].astype(str).str.strip() + ' ' + m['LastName'].astype(str).str.strip()
    return m[['ContactId', 'StaffName']]

def build_availability_table(emp_avail: pd.DataFrame, day_avail: pd.DataFrame, staff_map: pd.DataFrame) -> pd.DataFrame:
    day_avail = day_avail.copy()
    day_avail['Id'] = day_avail['Dayavailabilityguid'].astype(str).str.split('-').str[0]
    emp_avail = emp_avail.copy()
    emp_avail['Id'] = emp_avail['Id'].astype(str)
    merged = emp_avail.merge(day_avail[['Id', 'Dayname']], on='Id', how='left')
    merged = merged.merge(staff_map, left_on='Contactid', right_on='ContactId', how='left')
    merged['Startts'] = pd.to_datetime(merged['Startts'], errors='coerce')
    merged['Endts'] = pd.to_datetime(merged['Endts'], errors='coerce')
    merged['AvailableHours'] = (merged['Endts'] - merged['Startts']).dt.total_seconds() / 3600
    availability_table = merged.groupby(['StaffName', 'Dayname'], dropna=False)['AvailableHours'].sum().reset_index().rename(columns={'Dayname': 'DayOfWeek'})
    return availability_table

def build_scheduled_table(appt: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end) + pd.Timedelta(days=1)
    appt_in_range = appt[(appt['StartDateTime'] >= start_dt) & (appt['StartDateTime'] < end_dt)].copy()
    appt_in_range['ISOYear'] = appt_in_range['StartDateTime'].dt.isocalendar().year
    appt_in_range['ISOWeek'] = appt_in_range['StartDateTime'].dt.isocalendar().week
    weeks = appt_in_range[['ISOYear', 'ISOWeek']].drop_duplicates().shape[0]
    weeks = max(weeks, 1)
    scheduled = appt_in_range.groupby(['Principal1Name', 'DayOfWeek'], dropna=False)['SegmentHours'].sum().reset_index().rename(columns={'Principal1Name': 'StaffName', 'SegmentHours': 'ScheduledHours_Total'})
    scheduled['ScheduledHours_WeeklyAvg'] = scheduled['ScheduledHours_Total'] / weeks
    scheduled['WeeksCounted'] = weeks
    return scheduled

def reconcile(availability_table: pd.DataFrame, scheduled_table: pd.DataFrame) -> pd.DataFrame:
    rec = availability_table.merge(scheduled_table[['StaffName', 'DayOfWeek', 'ScheduledHours_WeeklyAvg']], on=['StaffName', 'DayOfWeek'], how='left')
    rec['ScheduledHours_WeeklyAvg'] = rec['ScheduledHours_WeeklyAvg'].fillna(0)
    rec['CapacityGap'] = rec['AvailableHours'] - rec['ScheduledHours_WeeklyAvg']
    return rec.sort_values(['StaffName', 'DayOfWeek'])
