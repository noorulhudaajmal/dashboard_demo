import streamlit as st
from streamlit_option_menu import option_menu
import utils
import plots
from css.st_ui import st_ui_css


st.set_page_config(page_title="Property Analytics", layout="wide")
st.markdown(st_ui_css, unsafe_allow_html=True)

DF_PATH = "data/report_table.csv"

@st.cache_data
def load():
    return utils.load_data(DF_PATH)

df = load()

# st.write("### Property Management Dashboard")

selected = option_menu(
    menu_title=None,
    options=["Overview", "Operations"],
    icons=["speedometer", "wrench"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)


if selected == "Overview":
    kpis = utils.compute_high_level_kpis(df)

    # show metrics in 3 columns + 2nd row
    cols = st.columns(7)
    labels = list(kpis.items())
    for i, (label, val) in enumerate(labels):
        with cols[i % 7]:
            # for percentages show the % sign
            if "Percentage" in label or "Pct" in label:
                st.metric(label, f"{val} %")
            elif "Rent" in label:
                st.metric(label, f"{val}")
            else:
                st.metric(label, val)

    # two plots below
    col1, col2 = st.columns([2,1.2])
    with col1:
        st.plotly_chart(plots.line_rent_collection(df), use_container_width=True)
    with col2:
        st.plotly_chart(plots.bar_occupancy_trend(df), use_container_width=True)

elif selected == "Operations":
    ops = utils.compute_operations_kpis(df)
    c1,c2,c3,c4,c5 = st.columns(5)
    items = list(ops.items())
    for idx, (label, val) in enumerate(items):
        col = [c1,c2,c3,c4,c5][idx]
        with col:
            st.metric(label, val)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plots.leads_funnel(df), use_container_width=True)
    with col2:
        # reuse occupancy trend for a quick maintenance view
        st.plotly_chart(plots.bar_occupancy_trend(df), use_container_width=True)

# footer: small data table preview
st.markdown("---")
st.subheader("Recent data snapshot")
st.dataframe(df.sort_values("date", ascending=False).head(10))
