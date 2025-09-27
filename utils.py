import pandas as pd
import os
import streamlit as st
import time
import json


def rename_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Renomeia as colunas 0 a 4."""

    nomes_colunas = ["Grupo", "Código da Composição", "Descrição", "Unidade"]

    for i, nome in zip(range(0, 4), nomes_colunas):
        dataframe = dataframe.rename(columns={f"Unnamed: {i}": nome})
    dataframe = dataframe.rename(
        columns={
            "indica que pelo menos um dos itens da composição não tem custo/preço.": "Código da Composição"
        }
    )

    return dataframe


def del_columns_sinapi(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Deleta as colunas %AS da SINAPI que não serão utilizadas."""

    index_delete = []

    for i in range(5, 58, 2):
        index_delete.append(i)

    index_delete.sort(reverse=True)

    for index in index_delete:

        dataframe = dataframe.drop(dataframe.columns[index], axis=1)

    return dataframe


def gerar_df_insumos_sinapi() -> pd.DataFrame:
    """Gera a tabela completa de insumos com base nos arquivos da pasta data."""

    nomes_arquivos = [
        f
        for f in os.listdir("data/")
        if f.startswith("SINAPI_Referência") and f.endswith(".xlsx") and "_" in f
    ]

    df_insumos_sinapi = pd.DataFrame()
    for arquivo in nomes_arquivos:
        df_arquivo = pd.read_excel(f"data/{arquivo}", sheet_name="ISD", header=9)
        df_arquivo["ano"] = arquivo.split("_")[2]
        df_arquivo["mes"] = arquivo.split("_")[3].split(".")[0]
        df_insumos_sinapi = pd.concat(
            [df_insumos_sinapi, df_arquivo], ignore_index=True
        )
    df_insumos_sinapi.fillna(0, inplace=True)

    return df_insumos_sinapi


def gerar_df_composicoes_sinapi() -> pd.DataFrame:
    """Gera a tabela completa de composições com base nos arquivos da pasta data."""

    nomes_arquivos = [
        f
        for f in os.listdir("data/")
        if f.startswith("SINAPI_Referência") and f.endswith(".xlsx") and "_" in f
    ]

    df_composicoes_sinapi = pd.DataFrame()

    for arquivo in nomes_arquivos:
        df_arquivo = pd.read_excel(f"data/{arquivo}", sheet_name="CSD", header=8)
        df_arquivo = rename_columns(df_arquivo)
        df_arquivo = del_columns_sinapi(df_arquivo)
        df_arquivo = df_arquivo.drop(index=0)
        df_arquivo["ano"] = arquivo.split("_")[2]
        df_arquivo["mes"] = arquivo.split("_")[3].split(".")[0]
        df_composicoes_sinapi = pd.concat(
            [df_composicoes_sinapi, df_arquivo], ignore_index=True
        )
    df_composicoes_sinapi.fillna(0, inplace=True)

    return df_composicoes_sinapi


@st.cache_data(ttl="6h", show_spinner=False)
def carregar_dados_analise():
    session = st.session_state

    if "dados_carregados" not in session:
        progress_placeholder = st.empty()
        progress = progress_placeholder.progress(0)

        session["dados_carregados"] = {}

    if not session["dados_carregados"]:
        with st.spinner(
            "Processando os dados. Esta operação pode levar alguns instantes."
        ):
            arquivos = [
                "dados_auxiliares.json",
                "malha_brasil.json",
                "data/composicoes_sinapi_completo.xlsx",
                "data/insumos_sinapi_completo.xlsx",
                "data/capitais_brasil.xlsx"
            ]
            file_name = {
                "dados_auxiliares.json": "dados_auxiliares",
                "malha_brasil.json":"malha_brasil",
                "data/composicoes_sinapi_completo.xlsx": "df_composicoes",
                "data/insumos_sinapi_completo.xlsx": "df_insumos",
                "data/capitais_brasil.xlsx":"capitais_brasil",
            }
            total = len(arquivos)
            for i, nome in enumerate(arquivos, start=1):
                nome_df = file_name[nome]
                try:
                    time.sleep(1)
                    if nome in ["dados_auxiliares.json","malha_brasil.json"]:
                        with open(nome, "r", encoding="utf-8") as f:
                            dados = json.load(f)
                    else:
                        dados = pd.read_excel(nome)
                    st.session_state["dados_carregados"][nome_df] = dados
                except FileNotFoundError:
                    st.session_state["dados_carregados"][nome_df] = None
                    st.error(f"Arquivo {nome} não encontrado.")
                except Exception as e:
                    st.session_state["dados_carregados"][nome_df] = None
                    st.error(f"Erro ao carregar {nome}: {e}")

                progress.progress(i / total)

            progress_placeholder.empty()


def preparar_dataframe_para_grafico(dataframe, estados_selecionados):
    dataframe_melted = dataframe.melt(
        id_vars="mes", var_name="estado", value_name="preco"
    )
    dataframe_filtrado = dataframe_melted[
        dataframe_melted["estado"].isin(estados_selecionados)
    ].sort_values("mes")

    return dataframe_filtrado
