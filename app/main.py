import streamlit as st
from data_loading import carregar_arquivos


st.set_page_config(
    page_title="SINAPI+",
    layout="wide",
    initial_sidebar_state="expanded",
)

session = st.session_state
if "loaded_data" not in session:
    session["loaded_data"] = False
    carregar_arquivos()

home = st.Page(page="pages/home.py", title="🏡 Home", default=True)
agua_potavel = st.Page(
    page="pages/sinapi_agua_potavel.py",
    title="🚰 Água Potável",
)
pages = [home, agua_potavel]

selected_page = st.navigation(pages)

selected_page.run()
