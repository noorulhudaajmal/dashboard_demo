import pandas as pd

def load_data(path="data/report_table.csv", parse_dates=["date"]):
    df = pd.read_csv(path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df

def latest_snapshot(df):
    return df.sort_values("date").iloc[-1]

def compute_high_level_kpis(df):
    # returns a dict of a few high-level KPIs from the latest row
    latest = latest_snapshot(df)
    kpis = {
        "Total Units": int(latest.get("total_units", 0)),
        "Occupied Units": int(latest.get("occupied_units", 0)),
        "Percentage Occupied": float(latest.get("percentage_occupied", 0)),
        "Pre-leased Units": int(latest.get("pre_leased_units", 0)),
        "Rent Billed": format_kpi_value(latest.get("rent_billed", 0)),
        "Rent Collected": format_kpi_value(latest.get("rent_collections", 0)),
        "Pct Rent Collected": float(latest.get("percentage_rent_collected", 0)),
    }
    return kpis

def compute_operations_kpis(df):
    latest = latest_snapshot(df)
    kpis = {
        "Open Work Orders": int(latest.get("open_work_orders", 0)),
        "Completed Work Orders (last snap)": int(latest.get("completed_work_orders", 0)),
        "New Leads": int(latest.get("new_leads", 0)),
        "Applications Started": int(latest.get("applications_started", 0)),
        "Approved Applications": int(latest.get("approved_applications", 0)),
    }
    return kpis


def format_kpi_value(kpi_value):
    if kpi_value >= 1e6:
        return f"${kpi_value / 1e6:.2f} M"
    elif kpi_value >= 1e3:
        return f"${kpi_value / 1e3:.2f} K"
    else:
        return f"${kpi_value:.2f}"
