import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Global Inequality", layout="wide")

# ===============================
# DARK MODE TOGGLE
# ===============================
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    body {background-color: #0e1117; color: white;}
    .card {background-color: #1c1f26; color: white;}
    </style>
    """, unsafe_allow_html=True)

# ===============================
# TITLE
# ===============================
st.markdown("<h1 style='text-align:center;'>🌍 Global Income Inequality Dashboard</h1>", unsafe_allow_html=True)

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    return pd.read_excel("WIID_19Dec2018.xlsx")

df = load_data()

df = df[['country','year','gini_reported','region_wb',
         'incomegroup','gdp_ppp_pc_usd2011','population']]

df = df.dropna(subset=['gini_reported'])

# ===============================
# DOWNLOAD BUTTON
# ===============================
st.download_button("📥 Download Data", df.to_csv(index=False), "data.csv")

# ===============================
# FILTERS
# ===============================
country = st.sidebar.selectbox("Country", ["All"] + list(df.country.unique()))
year = st.sidebar.selectbox("Year", ["All"] + sorted(df.year.dropna().unique()))

if country != "All":
    df = df[df.country == country]

if year != "All":
    df = df[df.year == year]

# ===============================
# KPI CARDS
# ===============================
col1, col2, col3 = st.columns(3)

col1.metric("Avg Inequality", round(df.gini_reported.mean(),2))
col2.metric("Max Inequality", round(df.gini_reported.max(),2))
col3.metric("Min Inequality", round(df.gini_reported.min(),2))

# ===============================
# NAVIGATION
# ===============================
option = st.sidebar.radio("Analysis", [
    "Overview","Global","Regional","GDP","Income Group","Trend","Population","World Map"
])

# ===============================
# OVERVIEW
# ===============================
if option == "Overview":
    st.dataframe(df.head())
    st.info("Dataset shows global income inequality patterns.")

# ===============================
# GLOBAL
# ===============================
elif option == "Global":
    top = df.groupby('country')['gini_reported'].mean().nlargest(10)

    fig, ax = plt.subplots()
    top.plot(kind='bar', ax=ax)

    st.pyplot(fig)
    st.success("Top countries show high inequality gaps.")

# ===============================
# REGIONAL
# ===============================
elif option == "Regional":
    region = df.groupby('region_wb')['gini_reported'].mean()

    fig, ax = plt.subplots()
    sns.barplot(x=region.index, y=region.values, ax=ax)
    plt.xticks(rotation=45)

    st.pyplot(fig)

# ===============================
# GDP
# ===============================
elif option == "GDP":
    fig = px.scatter(df, x='gdp_ppp_pc_usd2011', y='gini_reported',
                     color='region_wb',
                     title="GDP vs Inequality")
    st.plotly_chart(fig)

# ===============================
# INCOME GROUP
# ===============================
elif option == "Income Group":
    inc = df.groupby('incomegroup')['gini_reported'].mean()

    fig, ax = plt.subplots()
    sns.barplot(x=inc.index, y=inc.values, ax=ax)
    plt.xticks(rotation=45)

    st.pyplot(fig)

# ===============================
# TREND (ANIMATED)
# ===============================
elif option == "Trend":
    trend = df.groupby(['year'])['gini_reported'].mean().reset_index()

    fig = px.line(trend, x='year', y='gini_reported',
                  title="Global Inequality Trend Over Time")

    st.plotly_chart(fig)

# ===============================
# POPULATION
# ===============================
elif option == "Population":
    fig = px.scatter(df, x='population', y='gini_reported',
                     size='population', color='region_wb')

    st.plotly_chart(fig)

# ===============================
# WORLD MAP 🌍
# ===============================
elif option == "World Map":
    map_df = df.groupby('country')['gini_reported'].mean().reset_index()

    fig = px.choropleth(
        map_df,
        locations="country",
        locationmode="country names",
        color="gini_reported",
        title="Global Inequality Map",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig)
