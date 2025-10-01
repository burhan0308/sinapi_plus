import streamlit as st
from utils import calcular_custo_total,montar_relatorio_final
import pandas as pd

st.subheader("Resultados da Simulação")

_, __, coluna = st.columns([3,1,1])
custo_total = calcular_custo_total()
with coluna:   
    st.metric(
        'Total Simulado(R$)',
        custo_total,
              )



df_final = montar_relatorio_final()
with st.container():
    st.dataframe(df_final)