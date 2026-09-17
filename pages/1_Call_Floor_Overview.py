import streamlit as st
import pandas as pd
import plotly.express as px
from database.connection import load_callfloor

st.set_page_config(
    page_title="Call Floor Overview",
    page_icon="📞",
    layout="wide"
)

st.title("📞 Call Floor Overview")

# -----------------------------
# Load Data
# -----------------------------
try:
    df = load_callfloor()

    if df.empty:
        st.warning("No records returned from dws.vw_CallFloorOverview")
        st.stop()

except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# -----------------------------
# Sidebar Filters
# -----------------------------
with st.sidebar:

    st.header("Filters")

    if "CampaignCode" in df.columns:
        campaigns = st.multiselect(
            "Campaign",
            sorted(df["CampaignCode"].dropna().unique())
        )

        if campaigns:
            df = df[df["CampaignCode"].isin(campaigns)]

    if "BatchCode" in df.columns:
        batches = st.multiselect(
            "Batch",
            sorted(df["BatchCode"].dropna().unique())
        )

        if batches:
            df = df[df["BatchCode"].isin(batches)]

    if "DialerTypeName" in df.columns:
        dialers = st.multiselect(
            "Dialer Type",
            sorted(df["DialerTypeName"].dropna().unique())
        )

        if dialers:
            df = df[df["DialerTypeName"].isin(dialers)]

# -----------------------------
# KPI Calculations
# -----------------------------
unique_leads = (
    int(df["UniqueLeadCount"].sum())
    if "UniqueLeadCount" in df.columns else 0
)

phones = (
    int(df["PhoneCount"].sum())
    if "PhoneCount" in df.columns else 0
)

calls = (
    int(df["CallAttemptCount"].sum())
    if "CallAttemptCount" in df.columns else 0
)

contacts = (
    int(df["ContactAttemptCount"].sum())
    if "ContactAttemptCount" in df.columns else 0
)

success = (
    int(df["SuccessAttemptCount"].sum())
    if "SuccessAttemptCount" in df.columns else 0
)

sales = (
    int(df["SalesCount"].sum())
    if "SalesCount" in df.columns else 0
)

# -----------------------------
# KPI Row 1
# -----------------------------
kpi1 = st.columns(6)

kpi1[0].metric("Unique Leads", f"{unique_leads:,}")
kpi1[1].metric("Phone Count", f"{phones:,}")
kpi1[2].metric("Call Attempts", f"{calls:,}")
kpi1[3].metric("Contacts", f"{contacts:,}")
kpi1[4].metric("Success", f"{success:,}")
kpi1[5].metric("Sales", f"{sales:,}")

# -----------------------------
# KPI Row 2
# -----------------------------
contact_rate = (
    (contacts / calls) * 100
    if calls else 0
)

success_rate = (
    (success / contacts) * 100
    if contacts else 0
)

sales_conversion = (
    (sales / success) * 100
    if success else 0
)

kpi2 = st.columns(3)

kpi2[0].metric(
    "Contact Rate",
    f"{contact_rate:.2f}%"
)

kpi2[1].metric(
    "Success Rate",
    f"{success_rate:.2f}%"
)

kpi2[2].metric(
    "Sales Conversion",
    f"{sales_conversion:.2f}%"
)

# -----------------------------
# Calls By Campaign
# -----------------------------
if (
    "CampaignName" in df.columns
    and "CallAttemptCount" in df.columns
):

    campaign_calls = (
        df.groupby(
            "CampaignName",
            as_index=False
        )["CallAttemptCount"]
        .sum()
        .sort_values(
            "CallAttemptCount",
            ascending=False
        )
    )

    st.subheader("Calls by Campaign")

    fig_campaign = px.bar(
        campaign_calls,
        x="CampaignName",
        y="CallAttemptCount",
        title="Call Attempts by Campaign"
    )

    st.plotly_chart(
        fig_campaign,
        use_container_width=True
    )

# -----------------------------
# Disposition Analysis
# -----------------------------
if (
    "WrapupCategoryName" in df.columns
    and "CallAttemptCount" in df.columns
):

    disposition = (
        df.groupby(
            "WrapupCategoryName",
            as_index=False
        )["CallAttemptCount"]
        .sum()
        .sort_values(
            "CallAttemptCount",
            ascending=False
        )
    )

    st.subheader("Disposition Analysis")

    fig_disp = px.bar(
        disposition,
        x="CallAttemptCount",
        y="WrapupCategoryName",
        orientation="h"
    )

    st.plotly_chart(
        fig_disp,
        use_container_width=True
    )

# -----------------------------
# Dialer Analysis
# -----------------------------
if {
    "DialerTypeName",
    "CallAttemptCount",
    "ContactAttemptCount",
    "SuccessAttemptCount",
    "SalesCount"
}.issubset(df.columns):

    dialer = (
        df.groupby(
            "DialerTypeName",
            as_index=False
        )[
            [
                "CallAttemptCount",
                "ContactAttemptCount",
                "SuccessAttemptCount",
                "SalesCount"
            ]
        ]
        .sum()
    )

    st.subheader("Dialer Performance")

    st.dataframe(
        dialer,
        use_container_width=True
    )

# -----------------------------
# Call Analysis
# -----------------------------
if (
    "CallAnalysisName" in df.columns
    and "CallAttemptCount" in df.columns
):

    analysis = (
        df.groupby(
            "CallAnalysisName",
            as_index=False
        )["CallAttemptCount"]
        .sum()
    )

    st.subheader("Call Analysis Distribution")

    fig_analysis = px.pie(
        analysis,
        names="CallAnalysisName",
        values="CallAttemptCount"
    )

    st.plotly_chart(
        fig_analysis,
        use_container_width=True
    )

# -----------------------------
# Raw Data
# -----------------------------
with st.expander("View Data"):

    st.dataframe(
        df,
        use_container_width=True
    )
