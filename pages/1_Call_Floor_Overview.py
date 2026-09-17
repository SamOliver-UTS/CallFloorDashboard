import streamlit as st
import pandas as pd
import plotly.express as px
from database.connection import load_callfloor

st.title("Call Floor Overview")
df=load_callfloor()

with st.sidebar:

    st.header("Filters")

    if "CampaignName" in df.columns:
        campaigns = st.multiselect(
            "Campaign",
            sorted(df["CampaignName"].dropna().unique())
        )

        if campaigns:
            df = df[df["CampaignName"].isin(campaigns)]

    if "BatchName" in df.columns:
        batches = st.multiselect(
            "Batch",
            sorted(df["BatchName"].dropna().unique())
        )

        if batches:
            df = df[df["BatchName"].isin(batches)]

    if "DialerTypeName" in df.columns:
        dialers = st.multiselect(
            "Dialer Type",
            sorted(df["DialerTypeName"].dropna().unique())
        )

        if dialers:
            df = df[df["DialerTypeName"].isin(dialers)]

unique_leads=int(df['UniqueLeadCount'].sum()) if 'UniqueLeadCount' in df.columns else 0
phones=int(df['PhoneCount'].sum()) if 'PhoneCount' in df.columns else 0
calls=int(df['CallAttemptCount'].sum()) if 'CallAttemptCount' in df.columns else 0
contacts=int(df['ContactAttemptCount'].sum()) if 'ContactAttemptCount' in df.columns else 0
success=int(df['SuccessAttemptCount'].sum()) if 'SuccessAttemptCount' in df.columns else 0
sales=int(df['SalesCount'].sum()) if 'SalesCount' in df.columns else 0

cols=st.columns(6)
for c,v,t in zip(cols,[unique_leads,phones,calls,contacts,success,sales],["Unique Leads","Phone Count","Call Attempts","Contacts","Success","Sales"]):
    c.metric(t,f'{v:,}')

contact_rate = (contacts / calls * 100) if calls else 0
success_rate = (success / contacts * 100) if contacts else 0
sales_conversion = (sales / success * 100) if success else 0

row2 = st.columns(3)

row2[0].metric(
    "Contact Rate",
    f"{contact_rate:.2f}%"
)

row2[1].metric(
    "Success Rate",
    f"{success_rate:.2f}%"
)

row2[2].metric(
    "Sales Conversion",
    f"{sales_conversion:.2f}%"
)

if 'CampaignName' in df.columns and 'CallAttemptCount' in df.columns:
    agg = (
    df.groupby("CampaignName", as_index=False)
      ["CallAttemptCount"]
      .sum()
      .sort_values(
        "CallAttemptCount",
        ascending=False
      )
)
    st.plotly_chart(px.bar(agg,x='CampaignName',y='CallAttemptCount',title='Calls by Campaign'),use_container_width=True)

if 'WrapupCategoryName' in df.columns and 'CallAttemptCount' in df.columns:
    w=df.groupby('WrapupCategoryName',as_index=False)['CallAttemptCount'].sum()
    st.plotly_chart(px.bar(w,x='CallAttemptCount',y='WrapupCategoryName',orientation='h',title='Disposition Analysis'),use_container_width=True)

if (
    "DialerTypeName" in df.columns
    and "ContactAttemptCount" in df.columns
):

    dialer = (
        df.groupby(
            "DialerTypeName",
            as_index=False
        )
        [
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

    st.plotly_chart(
        px.pie(
            analysis,
            names="CallAnalysisName",
            values="CallAttemptCount",
            title="Call Analysis Distribution"
        ),
        use_container_width=True
    )

st.dataframe(df.head(100),use_container_width=True)


