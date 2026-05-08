import plotly.express as px
import pandas as pd

def subject_allocation_chart(subjects, allocated_hours):
    df = pd.DataFrame({"Subject": subjects, "Allocated Hours": allocated_hours})
    fig = px.pie(df, names="Subject", values="Allocated Hours",
                 title="Study Time Allocation",
                 color_discrete_sequence=px.colors.sequential.Blues_r)
    fig.update_traces(textinfo='percent+label', textfont_size=14)
    return fig

def weekly_distribution_chart(plan):
    df = pd.DataFrame(plan[:14])
    fig = px.bar(df, x="date", y="total_hours",
                 title="Daily Study Hours",
                 labels={"total_hours": "Hours"})
    fig.update_layout(template="plotly_white", height=400)
    return fig
