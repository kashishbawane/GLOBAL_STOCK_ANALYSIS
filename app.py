import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from streamlit_lottie import st_lottie
import requests
import time

st.set_page_config(page_title="Global Inequality", layout="wide")

# ===============================
# LOGIN
# ===============================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.login = True
        else:
            st.error("Invalid credentials")
    st.stop()

# ===============================
# LOAD LOTTIE
# ===============================
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ===============================
# ANIMATION
# ===============================
lottie = load_lottie("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")
st_lottie(lottie, height=200)

st.markdown("<h1 style='text-align:center;'>🌍 Global Income Inequality Dashboard</h1>", unsafe_allow_html=True)

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    return pd.read_excel("WIID_19Dec2018.xlsx")

with st.spinner("Loading data..."):
    time.sleep(1)
    df = load_data()

df = df[['country','year','gini_reported','region_wb',
         'incomegroup','gdp_ppp_pc_usd2011','population']]

df = df.dropna(subset=['gini_reported'])

# ===============================
# DOWNLOAD
# ===============================
st.download_button("📥 Download Data", df.to_csv(index=False), "data.csv")

# ===============================
# KPI
# ===============================
c1,c2,c3 = st.columns(3)
c1.metric("Avg Inequality", round(df.gini_reported.mean(),2))
c2.metric("Max Inequality", round(df.gini_reported.max(),2))
c3.metric("Min Inequality", round(df.gini_reported.min(),2))

# ===============================
# AI CHATBOT
# ===============================
st.sidebar.markdown("## 🤖 AI Assistant")
question = st.sidebar.text_input("Ask about data")

if question:
    if "average" in question.lower():
        st.sidebar.write("Average inequality:", round(df.gini_reported.mean(),2))
    elif "highest" in question.lower():
        st.sidebar.write(df.loc[df.gini_reported.idxmax()])
    elif "lowest" in question.lower():
        st.sidebar.write(df.loc[df.gini_reported.idxmin()])
    elif "gdp" in question.lower():
        st.sidebar.write("GDP has weak relation with inequality")
    else:
        st.sidebar.write("Ask about average, highest, lowest, GDP")

# ===============================
# NAVIGATION
# ===============================
opt = st.sidebar.radio("Menu",[
    "Overview","Global","Regional","GDP",
    "Income","Trend","Population","Map",
    "ML Prediction","Report"
])

# ===============================
# OVERVIEW
# ===============================
if opt=="Overview":
    st.dataframe(df.head())

# ===============================
# GLOBAL
# ===============================
elif opt=="Global":
    top = df.groupby('country')['gini_reported'].mean().nlargest(10)
    st.bar_chart(top)

# ===============================
# REGIONAL
# ===============================
elif opt=="Regional":
    region = df.groupby('region_wb')['gini_reported'].mean()
    st.bar_chart(region)

# ===============================
# GDP
# ===============================
elif opt=="GDP":
    fig = px.scatter(df,x='gdp_ppp_pc_usd2011',y='gini_reported',
                     color='region_wb',animation_frame='year')
    st.plotly_chart(fig)

# ===============================
# INCOME
# ===============================
elif opt=="Income":
    inc = df.groupby('incomegroup')['gini_reported'].mean()
    st.bar_chart(inc)

# ===============================
# TREND
# ===============================
elif opt=="Trend":
    trend = df.groupby('year')['gini_reported'].mean()
    st.line_chart(trend)

# ===============================
# POPULATION
# ===============================
elif opt=="Population":
    fig = px.scatter(df,x='population',y='gini_reported',
                     size='population',color='region_wb')
    st.plotly_chart(fig)

# ===============================
# MAP
# ===============================
elif opt=="Map":
    map_df = df.groupby('country')['gini_reported'].mean().reset_index()
    fig = px.choropleth(map_df,locations="country",
                        locationmode="country names",
                        color="gini_reported")
    st.plotly_chart(fig)

# ===============================
# ML PREDICTION
# ===============================
elif opt=="ML Prediction":
    st.subheader("Predict Inequality")

    df2 = df.dropna(subset=['gdp_ppp_pc_usd2011'])

    X = df2[['gdp_ppp_pc_usd2011']]
    y = df2['gini_reported']

    model = LinearRegression()
    model.fit(X,y)

    gdp = st.number_input("Enter GDP per capita")

    if st.button("Predict"):
        pred = model.predict([[gdp]])
        st.success(f"Predicted Inequality: {round(pred[0],2)}")

# ===============================
# REPORT + SMART INSIGHTS
# ===============================
elif opt=="Report":
    st.subheader("Smart Insights")

    avg = round(df.gini_reported.mean(),2)
    mx = df.loc[df.gini_reported.idxmax(), 'country']
    mn = df.loc[df.gini_reported.idxmin(), 'country']

    text = f"""
    Average inequality is {avg}.
    Highest inequality country is {mx}.
    Lowest inequality country is {mn}.
    """

    st.write(text)

    if st.button("Download PDF"):
        doc = SimpleDocTemplate("report.pdf")
        styles = getSampleStyleSheet()
        story = [Paragraph(text, styles["Normal"])]
        doc.build(story)

        with open("report.pdf","rb") as f:
            st.download_button("Download", f, "report.pdf")
