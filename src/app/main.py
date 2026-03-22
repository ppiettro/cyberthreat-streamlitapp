from backend.scripts.webscrape import webscrape_week_threats
from backend.scripts.threats_info import CyberThreatsData
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Brazil CyberThreats",
    page_icon=":material/shield_lock:",
    layout="wide"
)

@st.cache_data
def load_threat_data():
    """Cached function to load the threat data from the csv file.
    This prevents re-loading the data repeatedly within a session.

    :return dataframe: A pandas dataframe which contains all the collected data
    """
        
    cyberthreatstats = CyberThreatsData()
    base_df = pd.read_csv("src/data/cyberthreats_data.csv")

    last_collection_date = base_df["Date of Collection"][0]
    last_collection_date = pd.to_datetime(last_collection_date).date()
    current_date = pd.to_datetime("today").date()

    if (current_date - last_collection_date).days >= 7:
        data_list = webscrape_week_threats()

        if len(data_list) == 0:
            return base_df
        
        else:
            new_base_df = pd.DataFrame(data_list)
            cyberthreatstats.update_data(new_base_df.to_csv(index=False))

            return new_base_df
        
    else:
        return base_df

@st.cache_data
def initialize_data(base_data):
    threats_df = base_data.loc[base_data["Country Stats Detection Type"] != "Kaspersky Anti-Spam"].drop(columns=["Date of Collection"]).reset_index(drop=True)
    threats_count = pd.Series(threats_df["Threat Type"]).value_counts()
    latest_collection_date = base_data["Date of Collection"][0]

    html_datatable = threats_df.to_html(index=False).replace('border="1"','border="0"').replace('style="text-align: right;"', 'class="header-tr"')

    return {"Threats df": threats_df, 
            "Threats count": threats_count, 
            "Latest Collection Date": latest_collection_date, 
            "HTML Data Table": html_datatable
            }


base_df = load_threat_data()

pages = [
    st.Page("./pages/home/home.py", title="Home", icon=":material/other_houses:"),
    st.Page("./pages/dashboard/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    st.Page("./pages/informational/threat_information.py", title="Information about threats", icon=":material/dictionary:"),
    st.Page("./pages/search/search_threat.py", title="Search threat", icon=":material/search:")
    ]

navigation_bar = st.navigation(pages=pages, position="top")

navigation_bar.run()