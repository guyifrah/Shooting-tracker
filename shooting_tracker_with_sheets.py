
import streamlit as st
import pandas as pd
import gspread
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials

# כותרת ראשית
st.set_page_config(page_title="Shooting Tracker", layout="centered")
st.title("🏀 Guy's 3PT Shooting Tracker – גרסה מחוברת ל-Google Sheets")

# הגדרות API של Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1-9PCoym7x4oDFcr1tvNikePrTzsMy6vP/edit").sheet1

st.write("מלא את תוצאות האימון היומי:")

# אזורי זריקה
zones = ["Corner Right", "Wing Right", "Top of Key", "Wing Left", "Corner Left"]
shots = {}
makes = {}
percentages = {}

total_shots = 0
total_makes = 0

for zone in zones:
    st.subheader(zone)
    shots[zone] = st.number_input(f"זריקות מ-{zone}", min_value=0, key=f"{zone}_shots")
    makes[zone] = st.number_input(f"קליעות מ-{zone}", min_value=0, max_value=shots[zone], key=f"{zone}_makes")
    percentages[zone] = (makes[zone] / shots[zone] * 100) if shots[zone] > 0 else 0
    st.text(f"אחוזי קליעה: {percentages[zone]:.1f}%")
    total_shots += shots[zone]
    total_makes += makes[zone]

# חישוב אחוז כללי
if total_shots > 0:
    total_pct = total_makes / total_shots * 100
else:
    total_pct = 0.0

# שדה הערות
notes = st.text_input("הערות לאימון:")

# כפתור לשמירת הנתונים
if st.button("📥 שמור תוצאה ל-Google Sheets"):
    today = str(date.today())
    row = [today]
    for zone in zones:
        row += [shots[zone], makes[zone]]
    row += [total_shots, total_makes, f"{total_pct:.1f}%", notes]
    sheet.append_row(row)
    st.success("הנתונים נשמרו בהצלחה!")

# הצגת ההיסטוריה
st.markdown("---")
st.subheader("📊 היסטוריית אימונים (מהגיליון):")
data = sheet.get_all_records()
if data:
    df = pd.DataFrame(data)
    st.dataframe(df)

    # גרף שיפור
    st.subheader("📈 גרף שיפור באחוזי קליעה")
    df["אחוז כללי"] = df["אחוז כללי"].str.replace("%", "").astype(float)
    st.line_chart(df.set_index("תאריך")["אחוז כללי"])
else:
    st.write("עדיין אין נתונים לשמירה.")
