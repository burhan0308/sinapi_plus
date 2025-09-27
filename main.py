import streamlit as st
import pandas as pd
import json
from utils import (
    gerar_df_composicoes_sinapi,
    gerar_df_insumos_sinapi,
    carregar_dados_analise,
    preparar_dataframe_para_grafico,
)
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="SINAPI+",
    layout="wide",
    initial_sidebar_state="expanded",
)

session = st.session_state
carregar_dados_analise()

with st.sidebar:

    st.multiselect("Ano de Publicação", [2025])

    mes_selecionado = st.selectbox(
        "Mês de Publicação",
        session["dados_carregados"]["dados_auxiliares"]["meses"],
        
    )

    estado_selecionado = st.multiselect(
        "Estado", session["dados_carregados"]["dados_auxiliares"]["estados"]
    )

    df_composicoes = session["dados_carregados"]["df_composicoes"]
    lista_grupo_composicoes = df_composicoes["Grupo"].drop_duplicates().to_list()
    grupo_selecionado = st.selectbox("Grupo da Composição", lista_grupo_composicoes)

    lista_de_composicoes = (
        df_composicoes.loc[df_composicoes["Grupo"] == grupo_selecionado, "Descrição"]
        .drop_duplicates()
        .to_list()
    )
    composicao_selecionada = st.selectbox("Selecionar Composição", lista_de_composicoes)

with st.form("view"):
    st.subheader("Variação de preço por mês")
    submitted = st.form_submit_button("Ver Variação de Preços")
    if submitted:
        filtro = session["dados_carregados"]["dados_auxiliares"]["estados"].copy()
        filtro.append("mes")

        dados_analise = df_composicoes.loc[
            df_composicoes["Descrição"] == composicao_selecionada, filtro
        ].reset_index(drop=True)

        # df_long = dados_analise.melt(
        #     id_vars=["mes"], var_name="estado", value_name="preco"
        # )
        # st.write(df_long)
        # df_filtrado = df_long[df_long["estado"].isin(estado_selecionado)].sort_values(
        #     "mes"
        # )

        df_precos_composicoes = preparar_dataframe_para_grafico(
            dados_analise, estado_selecionado
        )

        fig = px.line(
            df_precos_composicoes,
            x="mes",
            y="preco",
            color="estado",
            title="Variação de preço por estado ao longo do tempo",
            labels={"mes": "Mês", "preco": "Preço (R$)", "estado": "Estado"},
            markers=True,
        )

        st.plotly_chart(fig, use_container_width=True)


with st.form("view_mapa"):
    st.subheader("Variação de Preço por Estado")
    submitted = st.form_submit_button("Gerar Visualização")
    if submitted:
        geojson = session["dados_carregados"]["malha_brasil"]

        mes_selecionado_numero = {
            "Janeiro":"1",
            "Fevereiro":"2",
            "Março":"3",
            "Abril":"4",
            "Maio":"5",
            "Junho":"6",
            "Julho":"7",
            "Agosto":"8",
            "Setembro":"9",
            "Outubro":'10',
            "Novembro":"11",
            "Dezembro":"12",
        }
        
        df_mes = df_composicoes.loc[
            (df_composicoes["Descrição"] == composicao_selecionada)
            & (df_composicoes["mes"]
            == int(mes_selecionado_numero[mes_selecionado]))
        ].reset_index(drop=True)
        lista_estados = session["dados_carregados"]["dados_auxiliares"]["estados"].copy()
        df_mapa = preparar_dataframe_para_grafico(df_mes,lista_estados)

        fig = px.choropleth(
            df_mapa,
            geojson=geojson,
            locations="estado",  # coluna com as siglas
            featureidkey="properties.sigla",  # no geojson, a chave que contém a sigla
            color="preco",
            color_continuous_scale="YlOrRd",
            title=f"Preços por estado - {mes_selecionado}",
            labels={"preco": "Preço (R$)"},
        )

        
        fig.update_geos(fitbounds="locations", visible=False)

        # 7. Mostre o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)