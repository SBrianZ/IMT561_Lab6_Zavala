import streamlit as st
import pandas as pd

from src.data import load_data
from src.filters import render_filters, apply_filters
from src.charts import plot_response_hist, plot_borough_bar
from src.layouts import header_metrics, body_layout_tabs


# -----------------------------
# IMT 561 Streamlit Lab Starter
# -----------------------------
#
# This repo is intentionally incomplete.
# During the lab, the instructor fills in TODO blocks live.
# Students then extend the same app for the in-class activity + assignment.
#


def main() -> None:
    st.set_page_config(
        page_title="S Brian's NYC 311 Mini Dashboard (Lab)",
        layout="wide",
    )

    st.title("NYC 311 Mini Dashboard")
    st.caption("Starter app for IMT 561 lab: layouts + filters + coordinated views.")

    # ✅ Data loading (cached)
    df = load_data("data/sample.csv")

    # -------------------------
    # TODO (DEMO): Add a quick 'data sanity' check
    # ^ Went ahead and just added this to the dashboard. It doesn't really make sense to keep in there but I want
    # to prove to y'all that I know how to do this task.
    # - show first 5 rows (optional)
    st.subheader("Sanity Check", divider=True)
    st.subheader("First 5 Rows")
    st.write(df.head(5))
    st.write(f"Total # of rows of the dataset: {df.shape[0]}.")
    st.subheader("KPIs", divider=True)
    # - show row count

    # -------------------------
    # HINT: st.write / st.dataframe
    # st.write(...)
    # st.dataframe(...)

    # -------------------------
    # Filters (sidebar by default)
    # -------------------------
    # render_filters returns a dictionary of user selections
    selections = render_filters(df)

    # apply_filters returns a filtered dataframe based on selections
    df_f = apply_filters(df, selections)

    # -------------------------
    # TODO (DEMO): Explain Streamlit re-runs
    # Brian's explanation: Reruns basically just updates your dashboard to match what you have programmed.
    # If you have Always Rerun enabled, then it will refresh every so often to stay updated with your code.
    # - changing a widget reruns the script top-to-bottom
    # - df_f changes because selections changes
    # -------------------------

    # -------------------------
    # Header metrics
    # -------------------------
    # TODO (IN-CLASS): Replace placeholder metrics with real calculations
    header_metrics(df_f)
    #^ I believe this is redundant with a KPI TODO in filters.py.
    # The headers metrics already have functional placeholder metrics, with real calculations, once fixed in that TODO.

    st.divider()

    # -------------------------
    # Main body
    # -------------------------
    # Tabs layout by default (3 tabs)
    tab_choice = st.radio(
        "Choose a layout for the body (lab demo uses tabs; assignment can remix):",
        ["Tabs (3)", "Two Columns"],
        horizontal=True,
    )

    if tab_choice == "Tabs (3)":
        body_layout_tabs(df_f)
    else:
        # -------------------------
        # TODO (DEMO): Implement a 2-column layout
        # ^this is functional and came with the assignment.
        # - left column: a chart
        # - right column: a table
        # -------------------------
        # HINT: st.columns(2)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Response Time Distribution")
            plot_response_hist(df_f)

        with col2:
            st.subheader("Filtered Rows")
            st.dataframe(df_f, use_container_width=True, height=420)


    # -------------------------
    # TODO (IN-CLASS): Add a footer with a short 'design note'
    st.subheader("Design Note", divider=True)
    st.caption("The NYC 311 Mini Dashboard is a live visualization that highlights common listing complaints across "
               "NYC boroughs. Analysts, students, and other city stakeholders interested in studying rental management "
               "can use this dashboard to understand the most prevalent issues affecting different neighborhoods, across"
               " the five boroughs. Some questions that people can answer from this dashboard include the most common complaint"
               " type per borough, the most common channel people report their complaints, and the overall median time"
               " it takes for specific boroughs to respond to a specific listing complaint types.")
    # - 2–3 sentences: who is the audience + what questions can they answer?
    ## Source: https://docs.streamlit.io/develop/api-reference/text/st.caption
    # I didn't know what you meant by footer, so I just looked up another way to do text and found caption.
    # -------------------------

if __name__ == "__main__":
    main()
