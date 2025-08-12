import plotly.express as px

def line_rent_collection(df):
    df2 = df.sort_values("date")
    fig = px.line(df2, x="date", y=["rent_billed", "rent_collections"],
                  labels={"value": "Amount", "date": "Date"},
                  title="Rent billed vs collected over time")
    fig.update_layout(legend_title_text="")
    return fig

def bar_occupancy_trend(df):
    df2 = df.sort_values("date")
    if "percentage_occupied" in df2.columns:
        fig = px.bar(df2, x="date", y="percentage_occupied",
                     labels={"percentage_occupied": "Pct Occupied", "date": "Date"},
                     title="Occupancy % over time")
    else:
        fig = px.bar(df2, x="date", y="occupied_units",
                     labels={"occupied_units": "Occupied Units", "date": "Date"},
                     title="Occupied units over time")
    return fig

def leads_funnel(df):
    df2 = df.sort_values("date").tail(12)
    fig = px.bar(df2, x="date", y=["new_leads", "applications_started", "approved_applications"],
                 title="Leads -> Applications -> Approvals (latest snapshots)")
    return fig
