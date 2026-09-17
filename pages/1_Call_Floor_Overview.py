import streamlit as st
import pandas as pd
import plotly.express as px
from database.connection import load_callfloor

st.title("Call Floor Overview")
df=load_callfloor()

with st.sidebar:
    if 'CampaignName' in df.columns:
        camp=st.multiselect('Campaign',sorted(df['CampaignName'].dropna().unique()))
        if camp: df=df[df['CampaignName'].isin(camp)]

unique_leads=int(df['UniqueLeadCount'].sum()) if 'UniqueLeadCount' in df.columns else 0
phones=int(df['PhoneCount'].sum()) if 'PhoneCount' in df.columns else 0
calls=int(df['CallAttemptCount'].sum()) if 'CallAttemptCount' in df.columns else 0
contacts=int(df['ContactAttemptCount'].sum()) if 'ContactAttemptCount' in df.columns else 0
success=int(df['SuccessAttemptCount'].sum()) if 'SuccessAttemptCount' in df.columns else 0
sales=int(df['SalesCount'].sum()) if 'SalesCount' in df.columns else 0

cols=st.columns(6)
for c,v,t in zip(cols,[unique_leads,phones,calls,contacts,success,sales],["Unique Leads","Phone Count","Call Attempts","Contacts","Success","Sales"]):
    c.metric(t,f'{v:,}')

if calls:
    st.metric('Contact Rate',f'{contacts/calls*100:.2f}%')

if 'CampaignName' in df.columns and 'CallAttemptCount' in df.columns:
    agg=df.groupby('CampaignName',as_index=False)['CallAttemptCount'].sum()
    st.plotly_chart(px.bar(agg,x='CampaignName',y='CallAttemptCount',title='Calls by Campaign'),use_container_width=True)

if 'WrapupCategoryName' in df.columns and 'CallAttemptCount' in df.columns:
    w=df.groupby('WrapupCategoryName',as_index=False)['CallAttemptCount'].sum()
    st.plotly_chart(px.bar(w,x='CallAttemptCount',y='WrapupCategoryName',orientation='h',title='Disposition Analysis'),use_container_width=True)

st.dataframe(df.head(100),use_container_width=True)
