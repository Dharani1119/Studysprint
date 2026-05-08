from datetime import datetime, timedelta

def calculate_days_remaining(exam_date):
    today = datetime.now().date()
    exam = datetime.strptime(exam_date, "%Y-%m-%d").date()
    return max(0, (exam - today).days)

def generate_study_plan(subjects, difficulties, exam_date, daily_hours):
    days_left = calculate_days_remaining(exam_date)
    if days_left == 0:
        return None, "Exam date has passed or is today."
    
    diff_weight = {"Easy": 1.0, "Medium": 1.5, "Hard": 2.0}
    weights = [diff_weight.get(d, 1.5) for d in difficulties]
    total_weight = sum(weights)
    
    total_study_hours = days_left * daily_hours
    subject_hours = [round((w / total_weight) * total_study_hours, 1) for w in weights]
    
    plan = []
    subject_list = list(zip(subjects, subject_hours, difficulties))
    
    for day in range(days_left):
        date = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")
        daily_tasks = []
        
        for subj, hours, diff in subject_list:
            session_hours = round(hours / days_left, 1)
            if session_hours > 0:
                daily_tasks.append({
                    "subject": subj,
                    "hours": session_hours,
                    "type": "Focus Study" if diff == "Hard" else "Regular Study"
                })
        
        if day % 4 == 3 and day < days_left - 1:
            daily_tasks.append({"subject": "All Subjects", "hours": 1.0, "type": "Revision"})
        
        plan.append({
            "day": day + 1,
            "date": date,
            "tasks": daily_tasks,
            "total_hours": round(sum(t["hours"] for t in daily_tasks), 1)
        })
    
    return plan, f"✅ Plan generated for {days_left} days"
