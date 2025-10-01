import streamlit as st
from ProcessarComposicao import PrecificarComposicao
from utils import calcular_custo_composicao, gerar_dicionario_trechos_rede


def custo_total_agua_potavel(escopo):
    """Precifica todas as composições pertinentes a categoria de Água Potável."""
    session = st.session_state

    PrecificarComposicao.iniciar_sincronizacao(escopo)

    itens_comuns = {
        "COMP-AGUA-001": "input_agua_ligacao_predial",
        "COMP-AGUA-002": "input_agua_hidrometro",
    }

    calcular_custo_composicao(session, escopo, itens_comuns)

    composicoes_rede_agua = {
        "defofo": {
            150: "COMP-AGUA-006",
            200: "COMP-AGUA-007",
            250: "COMP-AGUA-008",
            300: "COMP-AGUA-009",
        },
        "pba": {50: "COMP-AGUA-003", 75: "COMP-AGUA-004", 100: "COMP-AGUA-005"},
    }

    dicionario_rede_pba = gerar_dicionario_trechos_rede(
        session,
        "input_agua_qtd_trechos_pba",
        "input_agua_diametro_pba_",
        "input_agua_comprimento_pba_",
        composicoes_rede_agua,
    )
    calcular_custo_composicao(
        session,
        escopo,
        dicionario_rede_pba,
    )

    dicionario_rede_pvc = gerar_dicionario_trechos_rede(
        session,
        "input_agua_qtd_trechos_defofo",
        "input_agua_diametro_defofo_",
        "input_agua_comprimento_defofo_",
        composicoes_rede_agua
    )
    calcular_custo_composicao(session, escopo, dicionario_rede_pvc)



