
import streamlit as st

st.set_page_config(page_title="Shooting Tracker", layout="centered")
st.title("🏀 Guy's 3PT Shooting Tracker")

st.write("הכנס כמה זריקות לקחת וכמה קלעת בכל אזור שלשה:")

# הזנת נתונים לפי אזור
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

st.markdown("---")
st.subheader("📊 סטטיסטיקה כללית")
if total_shots > 0:
    total_pct = total_makes / total_shots * 100
    st.write(f"**סך כל הזריקות:** {total_shots}")
    st.write(f"**סך כל הקליעות:** {total_makes}")
    st.write(f"**אחוז כללי:** {total_pct:.1f}%")
else:
    st.write("אין נתונים עדיין. התחל להזין זריקות.")
