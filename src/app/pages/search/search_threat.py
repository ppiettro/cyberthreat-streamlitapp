from main import base_df, initialize_data
from backend.scripts.webscrape import threat_info_webscraper
import streamlit as st



@st.cache_data
def get_threat_details(url):
    """
    Cached function to scrape threat details.
    This prevents re-scraping the same URL repeatedly within a session.
    """

    return threat_info_webscraper(url=url)


data = initialize_data(base_df)

threats_df = data["Threats df"]
threats_count = data["Threats count"]

st.title(":material/search: Search Threat")

with st.container(border=False):
    option = st.selectbox(
        label="Search a threat to read about it",
        options=threats_df["Threat Name"].unique(),
        index=None,
        placeholder="Select a threat...",
    )

    if option:
            with st.container(border=True):
                threat_url = f'{threats_df.loc[threats_df["Threat Name"] == option]["Threat Link"].values[0]}/'

                parent_class_name, parent_class_description, class_name, platform_type, platform_description = get_threat_details(url=threat_url)

                if class_name != "Not found":
                    class_url = f"https://threats.kaspersky.com/en/class/{class_name}/"
                    
                    st.subheader(f":green[Class:] [{class_name}](%s)" % class_url)
                    st.markdown("You can see the description of this class on the 'Information about threats' tab.")

                if parent_class_name != "Not found":
                    parent_class_url = f"https://threats.kaspersky.com/en/class/{parent_class_name}/"

                    st.subheader(f":green[Parent Class:] [{parent_class_name}](%s)" % parent_class_url)
                    st.markdown(parent_class_description)
                
                if platform_type != "Not found":
                    platform_url = f"https://threats.kaspersky.com/en/platform/{platform_type}/"

                    st.subheader(f":green[Platform:] [{platform_type}](%s)" % platform_url)
                    st.markdown(platform_description)

                if class_name == "Not found" and parent_class_name == "Not found" and platform_type == "Not found":
                    st.markdown("Sorry, but it seems we couldn't get any kind of data about this threat. Please, click on the text below and see if there is some data about it.")

                st.markdown(f"[Read more about the threat](%s)" % threat_url)

