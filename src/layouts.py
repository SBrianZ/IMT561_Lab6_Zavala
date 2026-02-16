import pandas as pd
import streamlit as st

from src.charts import plot_response_hist, plot_borough_bar, plot_borough_count


def header_metrics(df: pd.DataFrame) -> None:
    """Rendering header metrics. Placeholder values are intentional."""
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    # TODO (IN-CLASS): Replace these placeholders with real metrics from df

    ## ^ I am not following what you want for this step, so I just filled out the BLANKS and added your % request.
    # for devices

    # Suggestions:
    # - Total complaints (len(df))
    # - Median response time
    # - % from Web vs Phone vs App (pick one)

    with c1:
        st.metric("Total complaints", len(df['complaint_type']))
    with c2:
        st.metric("Median response (days)", df['response_time_days'].median().round(2))
    with c3:
        st.metric("Most common complaint", df['complaint_type'].value_counts().index[0])
    with c4:
        st.metric("Web Users", str(round((df['channel']=="Web").sum()/len(df['channel'])*100,2))+'%')
    with c5:
        st.metric("Phone Users", str(round((df['channel']=="Phone").sum()/len(df['channel'])*100,2))+'%')
    with c6:
        st.metric("App Users", str(round((df['channel']=="App").sum()/len(df['channel'])*100,2))+'%')



def body_layout_tabs(df: pd.DataFrame) -> None:
    """Tabs layout with 3 default tabs."""
    t1, t2, t3 = st.tabs(["Distribution", "By Borough", "Table"])

    with t1:
        st.subheader("Response Time Distribution")
        plot_response_hist(df)

        # TODO (IN-CLASS): Add a short interpretation sentence under the chart
        st.info(f"INTERPRETATION: On average, it takes around {df['response_time_days'].mean().round(2)} days for a response."
                f"\nDays are reported as a float, so after rounding the value, the most common number of days reported is around"
                f" {df['response_time_days'].round(0).value_counts().index[0]}.")
        # Since the barchart is visualizing floats and using bins, the median is going to look inaccurate. This is because
        # the bins are capturing values from a .01 to .99 range, which doesn't make sense when rounding since values
        # in the middle of that will round to the closest "ones" place value. I personally would've first rounded the
        # barchart to integers since I would interpret days as whole numbers. However, I am not going to change your viz
        # and instead just show how I would tell someone what the most common whole number day is based on this floating viz.

    with t2:
        st.subheader("Median Response Time by Borough")
        plot_borough_bar(df)

        # TODO (IN-CLASS): Add a second view here (e.g., count by borough)
        st.subheader("Count by Borough")
        plot_borough_count(df)
        # ^ I made this barchart in the charts.py

    with t3:
        st.subheader("Filtered Rows")
        st.dataframe(df, use_container_width=True, height=480)

        # TODO (OPTIONAL): Add st.download_button to export filtered rows
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="sample.csv",
            mime="text/csv",
            icon=":material/download:",
        )
        ## Source: https://docs.streamlit.io/develop/api-reference/widgets/st.download_button
        ## Source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html