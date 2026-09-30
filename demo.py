import pandas as pd
from capacity import build_scheduled_table, reconcile

# Entirely fabricated staff labels and hours.
available = pd.DataFrame([
    {"StaffName": "DEMO-STAFF-01", "DayOfWeek": "Monday", "AvailableHours": 8.0},
    {"StaffName": "DEMO-STAFF-02", "DayOfWeek": "Monday", "AvailableHours": 4.0},
    {"StaffName": "DEMO-STAFF-03", "DayOfWeek": "Monday", "AvailableHours": 6.0},
])
appointments = pd.DataFrame([
    {"Principal1Name": "DEMO-STAFF-01", "StartDateTime": pd.Timestamp("2026-01-05 09:00"), "SegmentHours": 6.0},
    {"Principal1Name": "DEMO-STAFF-02", "StartDateTime": pd.Timestamp("2026-01-05 09:00"), "SegmentHours": 5.0},
])
appointments["DayOfWeek"] = appointments["StartDateTime"].dt.day_name()
scheduled = build_scheduled_table(appointments, "2026-01-05", "2026-01-11")
result = reconcile(available, scheduled)
assert result["CapacityGap"].tolist() == [2.0, -1.0, 6.0]
print(result.to_string(index=False))
