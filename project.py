import streamlit as st
import pandas as pd




#creating my page

st.set_page_config("Redbus",page_icon="",layout="wide")
st.subheader("Redbus")
st.image(r"C:\Users\rakes\OneDrive\Pictures\Screenshots\Screenshot (176).png", width=100)
#getting data from database
#calling function
from conection import *


result= view_ll_data() 
df=pd.DataFrame(result,columns=["ID","busname","bustype","departing_time","reaching_time","duration","Price","Seats_Available","star_ratings","Route_name","Route_link"])



#side bar
st.sidebar.header("Filter Route_name")
routename=st.sidebar.multiselect(
    label="Filter Route_name",
    options=df["Route_name"].unique(),
    default=df["Route_name"].unique()
)

st.sidebar.header("Filter bustype")
Bustype=st.sidebar.multiselect(
    label="Filter bustype",
    options=df["bustype"].unique(),
    default=df["bustype"].unique()
)

st.sidebar.header("Filter by Price Range")
price_filter = st.sidebar.radio(
    "Select Price Range:",
    ("Minimum (100-500)", "Moderate (500-1000)", "Maximum (1000 and above)")
)

# Apply Price filter
if price_filter == "Minimum (100-500)":
    df = df[(df['Price'] >= 100) & (df['Price'] <= 500)]
elif price_filter == "Moderate (500-1000)":
    df = df[(df['Price'] > 500) & (df['Price'] <= 1000)]
else:
    df = df[df['Price'] > 1000]

df_selection=df.query("Route_name==@routename & bustype==@Bustype")


def metrics():
    from streamlit_extras.metric_cards import style_metric_cards
    col1,col2=st.columns(2)
    col1.metric("Total number of buses",df.ID.count(),delta="All buses")
    col2.metric("Price",value=f"{df.Price.max():,.0f}",delta="Maximum Price")
    style_metric_cards(background_color="#071021",border_color="#1f66bd")
metrics()

def table():
    with st.expander("My buses"):
        seedata=st.multiselect("Filter Data",df_selection.columns,default=["ID","busname","bustype","departing_time","reaching_time","duration","Price","Seats_Available","star_ratings","Route_name","Route_link"])
        st.dataframe(df_selection[seedata],use_container_width=True)
table()        




