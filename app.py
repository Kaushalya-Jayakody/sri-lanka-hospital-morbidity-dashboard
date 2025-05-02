import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Sri Lanka Hospital Morbidity Dashboard", layout="wide")

st.title("🏥 Sri Lanka Hospital Morbidity Dashboard (2006–2013)")
st.markdown("""
Explore hospital discharge data in Sri Lanka by **disease**, **sex**, and **age group**.
Use the sidebar filters to interact with the data.
""")

# Load preprocessed long-format data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_morbidity_data_long.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filters")
selected_disease = st.sidebar.selectbox("Select Disease", sorted(df["Disease"].unique()))
selected_sex = st.sidebar.radio("Select Sex", df["Sex"].unique())
selected_age = st.sidebar.selectbox("Select Age Group", sorted(df["Age_Group"].unique()))

# Filtered subset
filtered = df[(df["Disease"] == selected_disease) & (df["Sex"] == selected_sex)]

# Chart 1 – Line chart
st.subheader(f"📈 Line Chart – {selected_disease} by Age Group ({selected_sex})")
fig1 = px.line(filtered, x="Age_Group", y="Count", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 – Bar chart
st.subheader("📊 Bar Chart – Discharges by Age")
fig2 = px.bar(filtered, x="Age_Group", y="Count", color="Age_Group")
st.plotly_chart(fig2, use_container_width=True)

# Chart 3 – Pie chart by sex
st.subheader(f"🚻 Pie Chart – {selected_disease} Discharges by Sex")
sex_data = df[df["Disease"] == selected_disease].groupby("Sex")["Count"].sum().reset_index()
fig3 = px.pie(sex_data, names="Sex", values="Count")
st.plotly_chart(fig3, use_container_width=True)

# Chart 4 – Top 10 diseases for selected age
st.subheader(f"📌 Top 10 Diseases in Age Group: {selected_age}")
top10 = df[df["Age_Group"] == selected_age].groupby("Disease")["Count"].sum().reset_index()
top10 = top10.sort_values(by="Count", ascending=False).head(10)
fig4 = px.bar(top10, x="Disease", y="Count", title="Top 10 Diseases", color="Disease")
st.plotly_chart(fig4, use_container_width=True)

# raw data table
with st.expander("📄 Show Filtered Data"):
    st.dataframe(filtered)

# footer
st.markdown("---")
st.caption("📘 Developed for 5DATA004W – Data Science Project Lifecycle · University of Westminster | Streamlit Dashboard")