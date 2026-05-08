import streamlit as st
import pandas as pd
from utils.planner import generate_study_plan, calculate_days_remaining
from utils.scoring import calculate_balance_score
from utils.charts import subject_allocation_chart, weekly_distribution_chart

st.set_page_config(page_title="StudySprint", page_icon="📚", layout="centered")

# Calming UI
st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 10px;
        height: 52px;
        font-size: 18px;
    }
    h1 {color: #1e2937;}
    .card {background-color: white; padding: 24px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);}
</style>
""", unsafe_allow_html=True)

st.title("📚 StudySprint")
st.markdown("**Create a stress-free study plan in seconds.**")

# Inputs
st.subheader("📌 Your Subjects")
subjects_input = st.text_area(
    "Enter one subject per line",
    "Mathematics\nBiology\nPhysics\nChemistry",
    height=140
)
subjects = [s.strip() for s in subjects_input.split("\n") if s.strip()]

col1, col2 = st.columns(2)
with col1:
    exam_date = st.date_input("Exam Date", value=None)
with col2:
    daily_hours = st.slider("Daily Available Study Hours", 1, 12, 4)

st.subheader("Difficulty Level")
difficulties = []
for subj in subjects:
    diff = st.selectbox(f"**{subj}**", ["Easy", "Medium", "Hard"], key=f"diff_{subj}")
    difficulties.append(diff)

# Generate Button
if st.button("Generate Study Plan", type="primary", use_container_width=True):
    if len(subjects) == 0 or not exam_date:
        st.error("Please add at least one subject and select exam date.")
    else:
        exam_str = exam_date.strftime("%Y-%m-%d")
        plan, message = generate_study_plan(subjects, difficulties, exam_str, daily_hours)
        
        if plan:
            st.success(message)
            
            # Burnout Warning
            days_left = len(plan)
            if daily_hours > 8:
                st.warning("⚠️ Your daily hours are quite high. Consider adding rest to avoid burnout.")
            
            # Score
            score = calculate_balance_score(plan, daily_hours)
            st.metric(label="Study Balance Score", value=f"{score}/100")
            
            st.subheader("📅 Your Personalized Study Roadmap")
            
            # Show plan
            for day in plan[:12]:
                with st.expander(f"Day {day['day']} — {day['date']} ({day['total_hours']} hrs)"):
                    for task in day['tasks']:
                        st.write(f"• **{task['subject']}** — {task['hours']} hours  *({task['type']})*")
            
            if len(plan) > 12:
                st.info(f"Showing first 12 days. Total days: {len(plan)}")
            
            # Charts
            st.subheader("Visual Breakdown")
            col1, col2 = st.columns(2)
            
            with col1:
                total_per_subject = [sum(d['total_hours']*0.3 for d in plan) for _ in subjects]  # rough
                st.plotly_chart(subject_allocation_chart(subjects, total_per_subject), use_container_width=True)
            
            with col2:
                st.plotly_chart(weekly_distribution_chart(plan), use_container_width=True)
            
            # Download
            df = pd.DataFrame(plan)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Plan as CSV",
                data=csv,
                file_name="StudySprint_Plan.csv",
                mime="text/csv"
            )
