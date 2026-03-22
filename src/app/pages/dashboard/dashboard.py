import streamlit as st
from main import base_df, initialize_data

data = initialize_data(base_df)

threats_df = data["Threats df"]
threats_count = data["Threats count"]

st.title(":material/bar_chart_4_bars: Gráficos")

cols = st.columns([2, 0.75])

with cols[0].container(border=True):
    st.subheader("Threat Types Distribution")

    option = st.selectbox(
        label="Selecione quais tipos de ameaças deseja ver",
        options=threats_count.index.unique(),
        index=None,
        placeholder="Selecione um tipo de ameaça",
    )

    if option:
        data = threats_df.loc[threats_df["Threat Type"] == option].drop(columns=["Country Stats Detection Type", "Threat Type", "Threat Link"])

        col_name = "Threat Name"
        if col_name in data.columns:
            data = data.set_index(col_name)
            data.index.name = None
            data["Threat Value (%)"] = data["Threat Value (%)"].str.rstrip('%').astype(float)
            data = data.sort_values(by="Threat Value (%)", ascending=True)

        st.bar_chart(
            data=data,
            width=1500,
            height=650,
            stack="center",
        )

with cols[1].container(border=True):
    st.subheader("Threat X frequency")

    st.bar_chart(
        threats_count,
        width=500,
        height=300,
        stack="layered",
        )

with cols[1].container(border=True):
    st.subheader("Threat distribution")

    data = threats_df.drop(columns=["Country Stats Detection Type", "Threat Type", "Threat Link"])
    data["Threat Value (%)"] = data["Threat Value (%)"].str.rstrip('%').astype(float).round(2)
    data = data.sort_values(by="Threat Value (%)", ascending=True)

    st.scatter_chart(
        data=data,
        x= "Threat Value (%)",
        y="Threat Name",
        width=500,
        height=350,
        size="Threat Value (%)",
    )
