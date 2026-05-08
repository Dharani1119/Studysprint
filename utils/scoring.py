import numpy as np

def calculate_balance_score(plan, daily_hours):
    if not plan:
        return 50
    avg_hours = np.mean([p['total_hours'] for p in plan])
    balance = 100 - abs(avg_hours - daily_hours) * 8
    return max(45, min(100, int(balance)))
