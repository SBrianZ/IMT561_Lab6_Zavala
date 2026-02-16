import pandas as pd
import streamlit as st


def render_filters(df: pd.DataFrame) -> dict:
    """Rendering filter widgets and returning the chosen values."""
    st.sidebar.header("Filters")

    boroughs = ["All"] + sorted(df["borough"].unique().tolist())
    channels = ["All"] + sorted(df["channel"].unique().tolist())
    complaint_types = ["All"] + sorted(df['complaint_type'].unique().tolist())

    borough = st.sidebar.selectbox("Borough", boroughs, index=0)
    channel = st.sidebar.selectbox("Channel", channels, index=0)

    # TODO (DEMO): Convert this selectbox to a multiselect (and update filtering logic)
    # complaint = st.sidebar.selectbox("Complaint Type", complaint_types, index=0)
    complaint = st.sidebar.multiselect("Complaint Type", complaint_types, default=complaint_types)
    # ^This line of code given in class actually doesn't work by itself, scroll down to apply_filters for reason.

    # Response time slider
    min_rt, max_rt = float(df["response_time_days"].min()), float(df["response_time_days"].max())
    rt_range = st.sidebar.slider(
        "Response time (days)",
        min_value=0.0,
        max_value=float(max_rt),
        value=(0.0, float(min(30.0, max_rt))),
        step=0.5,
    )

    # TODO (IN-CLASS): Add a checkbox toggle to cap outliers (e.g., at 99th percentile)
    cap_outliers = st.sidebar.checkbox("Cap extreme response times", value=False)
    # this was already here when I opened the lab ^

    return {
        "borough": borough,
        "channel": channel,
        "complaint": complaint,
        "rt_range": rt_range,
        "cap_outliers": cap_outliers,
    }


def apply_filters(df: pd.DataFrame, selections: dict) -> pd.DataFrame:
    """Applying filter selections to the dataframe."""
    out = df.copy()

    if selections["borough"] != "All":
        out = out[out["borough"] == selections["borough"]]

    if selections["channel"] != "All":
        out = out[out["channel"] == selections["channel"]]

    if selections["complaint"] == ["All"] or selections["complaint"] == []:
        out = out
    else:
       out = out[out["complaint_type"].isin(selections["complaint"])]

    ## Source: .isin() https://www.w3schools.com/python/pandas/ref_df_isin.asp checks if a value is in an array or df
    # Note: The apply filter causes errors with multiselect bcuz it doesn't know what to do with [].
    # So we have to assign [] to be something; I just made it operate similar to ['All'].

    lo, hi = selections["rt_range"]
    out = out[(out["response_time_days"] >= lo) & (out["response_time_days"] <= hi)]

    # TODO (IN-CLASS): Implement outlier capping when cap_outliers is checked
    # HINT: use out["response_time_days"].quantile(0.99)
    if selections["cap_outliers"]:
        bound = out["response_time_days"].quantile(0.99)
        out["response_time_days"] = out["response_time_days"].clip(upper=bound)

    ## Source: .clip() https://www.geeksforgeeks.org/python/numpy-clip-in-python/ - limits/clips values out of array
    return out.reset_index(drop=True)
