from ProcessarComposicao import PrecificarComposicao
import pandas as pd


def calcular_custo_total() -> float:
    """Retorna o custo total da simulação."""

    dicionario_composicoes = PrecificarComposicao.dicionario_resultante
    total_simulado = 0
    for _, dic in dicionario_composicoes.items():
        total_simulado += dic["custo_total"]
    return total_simulado


def calcular_custo_composicao(
    session, escopo: str, dicionario_composicoes: dict
) -> None:
    """Processa as composições e calcula o preço unitário e custo total."""
    for composicao, quantidade in dicionario_composicoes.items():
        PrecificarComposicao(session, composicao, quantidade, escopo).gerar_resultado()


def gerar_dicionario_trechos_rede(
    session,
    chave_qtd_trechos: str,
    prefixo_diametro_rede: str,
    prefixo_comprimento_rede: str,
    composicoes_rede: dict,
) -> dict:
    """Retonar um dicionário com o código da composição e a chave para acessar a quantidade simulada."""
    dicionario_iteravel = {}
    qtd_trechos = session[chave_qtd_trechos]
    tipo_rede = chave_qtd_trechos.split("_")[-1]
    for trecho in range(qtd_trechos):
        diametro_trecho = session[f"{prefixo_diametro_rede}{trecho + 1}"]
        composicao_trecho = composicoes_rede[tipo_rede][diametro_trecho]
        dicionario_iteravel[composicao_trecho] = (
            f"{prefixo_comprimento_rede}{trecho + 1}"
        )

    return dicionario_iteravel


def montar_relatorio_final():
    dicionario_composicoes = PrecificarComposicao.dicionario_resultante
    try:
        df_final = pd.DataFrame.from_dict(dicionario_composicoes, orient="index")
        df_final = df_final[
            ["_escopo", "descricao", "quantidade", "custo_unitario", "custo_total"]
        ]
        df_final = df_final.rename(
            columns={
                "custo_unitario": "Custo Unitário (R$)",
                "custo_total": "Custo Total (R$)",
                "quantidade": "Quantidade",
                "descricao": "Descrição",
                "_escopo": "Escopo",
            }
        )
    except:
        df_final = pd.DataFrame(
            columns=(
                "Escopo",
                "Descrição",
                "Quantidade",
                "Custo Unitário (R$)",
                "Custo Total (R$)",
            )
        )

    return df_final
