import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Global Income Inequality", layout="wide")

st.title("🌍 Global Income Inequality Analysis")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel("WIID_19Dec2018.xlsx")
    return df

df = load_data()

# Select important columns
df = df[['country','year','gini_reported','region_wb',
         'incomegroup','gdp_ppp_pc_usd2011',
         'top5','bottom5','population']]

df = df.dropna(subset=['gini_reported'])

# Sidebar
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Select Analysis",
    ["Overview",
     "Global Inequality",
     "Regional Analysis",
     "GDP vs Inequality",
     "Income Group",
     "Trend Analysis",
     "Population Analysis"]
)

# ===============================
# Overview
# ===============================
if option == "Overview":
    st.subheader("Dataset Overview")
    st.write(df.head())
    st.write("Shape:", df.shape)

# ===============================
# Task 1: Global Inequality
# ===============================
elif option == "Global Inequality":
    st.subheader("Global Inequality Distribution")

    country_gini = df.groupby('country')['gini_reported'].mean().nlargest(10)

    fig, ax = plt.subplots()
    country_gini.plot(kind='bar', ax=ax)
    ax.set_title("Top 10 Countries with Highest Inequality")

    st.pyplot(fig)

# ===============================
# Task 2: Regional Analysis
# ===============================
elif option == "Regional Analysis":
    st.subheader("Regional Inequality")

    region = df.groupby('region_wb')['gini_reported'].mean()

    fig, ax = plt.subplots()
    sns.barplot(x=region.index, y=region.values, ax=ax)
    plt.xticks(rotation=45)

    st.pyplot(fig)

# ===============================
# Task 3: GDP vs Inequality
# ===============================
elif option == "GDP vs Inequality":
    st.subheader("GDP vs Inequality")

    fig, ax = plt.subplots()
    sns.scatterplot(
        x='gdp_ppp_pc_usd2011',
        y='gini_reported',
        data=df,
        ax=ax
    )

    st.pyplot(fig)

# ===============================
# Task 4: Income Group
# ===============================
elif option == "Income Group":
    st.subheader("Income Group Comparison")

    inc = df.groupby('incomegroup')['gini_reported'].mean()

    fig, ax = plt.subplots()
    sns.barplot(x=inc.index, y=inc.values, ax=ax)
    plt.xticks(rotation=45)

    st.pyplot(fig)

# ===============================
# Task 5: Trend Analysis
# ===============================
elif option == "Trend Analysis":
    st.subheader("Inequality Trend Over Time")

    trend = df.groupby('year')['gini_reported'].mean()

    fig, ax = plt.subplots()
    trend.plot(ax=ax)

    st.pyplot(fig)

# ===============================
# Task 6: Population Analysis
# ===============================
elif option == "Population Analysis":
    st.subheader("Population vs Inequality")

    fig, ax = plt.subplots()
    sns.scatterplot(
        x='population',
        y='gini_reported',
        data=df,
        ax=ax
    )

    st.pyplot(fig)
