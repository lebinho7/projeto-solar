def calcular_custos(capex, taxa_juros, meses):
    """Calcula a parcela mensal de um financiamento."""
    i = (1 + taxa_juros / 100) ** (1 / 12) - 1
    parcela = capex * (i * (1 + i) ** meses) / ((1 + i) ** meses - 1)
    return parcela

def estimar_economia(consumo_mensal, tarifa_atual, tarifa_solar):
    """Estima a economia mensal ao trocar para energia solar."""
    custo_atual = consumo_mensal * tarifa_atual
    custo_novo = consumo_mensal * tarifa_solar
    economia = custo_atual - custo_novo
    return economia

def calcular_retorno_investimento(capex, economia_mensal):
    """Calcula o tempo de retorno do investimento em energia solar."""
    tempo_retorno = capex / economia_mensal
    return tempo_retorno

def simular_financiamento(capex, taxa_juros, meses, consumo_mensal, tarifa_atual, tarifa_solar):
    """Simula o financiamento e a economia gerada pela energia solar."""
    parcela_mensal = calcular_custos(capex, taxa_juros, meses)
    economia_mensal = estimar_economia(consumo_mensal, tarifa_atual, tarifa_solar)
    retorno_investimento = calcular_retorno_investimento(capex, economia_mensal)

    return {
        "parcela_mensal": parcela_mensal,
        "economia_mensal": economia_mensal,
        "tempo_retorno": retorno_investimento
    }