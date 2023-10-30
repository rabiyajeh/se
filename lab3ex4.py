# (1) Import the required libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import os  # for file handling
import warnings  # in case there are warnings, we want to ignore them
warnings.filterwarnings('ignore')

# (2) Page Configuration and Dashboard Title

# set the title of the page
st.set_page_config(page_title="Dashboard!!!", page_icon=":bar_chart:", layout="wide")

# set the title of the Dashboard
st.title("EDA of Superstore Data :bar_chart:")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# (3) Setting File uploader option on dashboard
fl = st.file_uploader(":file_folder: Upload a File", type=["csv", "txt", "xlsx", "xls"])
if fl is not None:
    fileName = fl.name
    st.write(fileName)
    df = pd.read_csv(fl, encoding="ISO-8859-1")
else:
    # Assuming "Superstore.csv" is in the same folder as your script
    df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")

# (4) Now select the dates for which you want to show the Sales, as in the dataset there is a column for order date

col1, col2 = st.columns(2)
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))
    df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

# (5) Now set the filters option on the sidebar for which you want to draw a bar chart and pie plot for sale

st.sidebar.header("Choose your filter:")

# Create for Region
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# Create for State
state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# Create for City
city = st.sidebar.multiselect("Pick the City", df3["City"].unique())

# Filter the data based on Region, State, and City

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df3["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df3["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()

st.subheader("Category wise Sales")
fig = px.bar(
    category_df, x="Category", y="Sales",
    text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
    template="seaborn"
)
st.plotly_chart(fig, use_container_width=True, height=200)

st.subheader("Region wise Sales")
fig = px.pie(
    filtered_df, values="Sales", names="Region", hole=0.5
)
fig.update_traces(text=filtered_df["Region"], textposition="outside")
st.plotly_chart(fig, use_container_width=True)
