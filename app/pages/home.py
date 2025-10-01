import streamlit as st

st.title("SINAPI+")

st.markdown("### O que é o SINAPI+?")
st.markdown(
    "É uma ferramenta para estimativa de custos de construção, baseada nos insumos e referências do SINAPI."
)


st.selectbox(
    label="Selecione um Estado:",
    options=[
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
    ],
    key='input_estado',
)
