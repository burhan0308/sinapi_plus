import streamlit as st
import pandas as pd

@st.cache_data(ttl='600',show_spinner=False)
def carregar_arquivos():
    with st.spinner(
        "Os arquivos estão sendo carregados, pode levar alguns instantes. Por favor, aguarde..."
    ):
        st.session_state["arquivos_base"] = {}
        progress_placeholder = st.empty()
        progress = 0
        arquivos_base = [
            "precos_composicoes_insumos",
            "base_composicoes"
        ]

        for arquivo in arquivos_base:
            st.session_state["arquivos_base"][arquivo] = pd.read_excel(f'excel_files/{arquivo}.xlsx')
            progress += 50
            progress_placeholder.progress(progress)
        
        progress_placeholder.empty()
    st.session_state["loaded_data"] = True