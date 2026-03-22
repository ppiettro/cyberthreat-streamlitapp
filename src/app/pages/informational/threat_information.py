from main import base_df, initialize_data
from backend.scripts.threats_info import ThreatInfo
from backend.scripts.webscrape import threat_type_general_info_webscraper
import streamlit as st


data = initialize_data(base_df)

threats_df = data["Threats df"]
threats_count = data["Threats count"]


st.title(":material/warning: Threats' information")

tab_names = [threat for threat in threats_count.index]
tabs = st.tabs(tab_names)

for i, (threat_type, count) in enumerate(threats_count.items()):
    with tabs[i]:
        st.badge(f"{count} (Number of '{threat_type}' that were in the LAST WEEK TOP 10) ",
                icon="⚠️", 
                color="red"
                )
        
        cols = st.columns(2)
        with cols[0].container(border=True):
            threats = ThreatInfo(threat_type)
            threat_description = threats.get_data()   

            if threat_description == "No data":
                threat_description = threat_type_general_info_webscraper(threat_type)
                threats.publish_data(threat_description)

            info_url = f"https://threats.kaspersky.com/en/class/{threat_type}/"
            
            if len(threat_description.split()) > 0:
                st.markdown("Collected from :green[Kaspersky Threats - Ameaças] :material/warning:")
                st.markdown(threat_description)

                st.markdown(f"**:green[Read more about {threat_type} on]** [Kaspersky Threats - Ameaças](%s)" % info_url)

            else:
                st.markdown("We couldn't collect the description of this threat from :red[Kaspersky Threats - Ameaças] :material/warning:")
                st.markdown(f"**:green[Read more about {threat_type} on:]** [Kaspersky Threats - Ameaças](%s)" % info_url)
                
        with cols[1].container(border=False):

            threat_df = threats_df.loc[threats_df["Threat Type"] == threat_type]

            st.dataframe(
                data=threat_df, 
                hide_index=True,
                column_config={
                    "Threat Type": None,
                    "Threat Link": None,
                    "Country Stats Detection Type": None,
                },
            )
