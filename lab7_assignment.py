import streamlit as st
import pandas as pd
import plotly.express as px

# Load Dataset
DATA_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(DATA_URL)


# Page Config + Theme
st.set_page_config(
    page_title="Titanic Data",
    layout="wide",
)

st.title("🚢 Titanic Data Visualization App")
st.write("Explore the Titanic dataset interactively using filters and charts.")

# Sidebar Controls
st.sidebar.title("Filters Options")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df["Sex"].unique(),
    default=df["Sex"].unique()
)

class_filter = st.sidebar.multiselect(
    "Select Passenger Class",
    options=df["Pclass"].unique(),
    default=df["Pclass"].unique()
)

age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=0, max_value=80, value=(0, 80)
)

# Apply filters
filtered_df = df[
    (df["Sex"].isin(gender_filter)) &
    (df["Pclass"].isin(class_filter)) &
    (df["Age"].between(age_range[0], age_range[1]))
]

# Summary Section
st.subheader("Summary Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Passengers", len(filtered_df))
col2.metric("Survived", filtered_df["Survived"].sum())
survival_rate = round((filtered_df["Survived"].mean() * 100), 2)
col3.metric("Survival Rate (%)", f"{survival_rate}%")

# Visualization 1 – Bar Chart (Survival by Class)
st.subheader("Survival Count by Passenger Class")

fig1 = px.bar(
    filtered_df,
    x="Pclass",
    y="Survived",
    color="Pclass",
    barmode="group",
    title="Survival Count by Class",
)
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2 – Histogram (Age Distribution)
st.subheader("Age Distribution of Passengers")

fig2 = px.histogram(
    filtered_df,
    x="Age",
    nbins=30,
    title="Age Distribution",
    color="Sex"
)
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3 – Scatter Plot (Optional Extra)
st.subheader("Fare vs Age (Colored by Survival)")

fig3 = px.scatter(
    filtered_df,
    x="Age",
    y="Fare",
    color="Survived",
    size="Fare",
    hover_data=["Name", "Sex", "Pclass"],
    title="Fare vs Age (Survived vs Not Survived)"
)
st.plotly_chart(fig3, use_container_width=True)

# Raw Data Toggle
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
