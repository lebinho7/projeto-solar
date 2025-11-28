import pytest
from src.finance import calcular_tudo

def test_calcular_tudo():
    # Teste com dados de entrada conhecidos
    consumo = 300  # kWh
    taxa_min = 30  # kWh
    irr = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5]  # Irradiação média mensal
    temp = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]  # Temperatura média mensal
    financiar = False
    fin_dados = None

    qtd, pot_wp, capex, parc, vec_antiga, vec_novo, vec_saldo, total_sem, total_com = calcular_tudo(consumo, taxa_min, irr, temp, financiar, fin_dados)

    # Verificações
    assert qtd > 0  # Deve haver pelo menos um módulo
    assert pot_wp > 0  # Potência do sistema deve ser positiva
    assert capex > 0  # Custo de capital deve ser positivo
    assert total_sem >= 0  # Total sem solar não pode ser negativo
    assert total_com >= 0  # Total com solar não pode ser negativo

def test_calcular_tudo_financiado():
    # Teste com financiamento
    consumo = 300  # kWh
    taxa_min = 30  # kWh
    irr = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5]  # Irradiação média mensal
    temp = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]  # Temperatura média mensal
    financiar = True
    fin_dados = (5.0, 24)  # Taxa de 5% ao ano por 24 meses

    qtd, pot_wp, capex, parc, vec_antiga, vec_novo, vec_saldo, total_sem, total_com = calcular_tudo(consumo, taxa_min, irr, temp, financiar, fin_dados)

    # Verificações
    assert qtd > 0  # Deve haver pelo menos um módulo
    assert pot_wp > 0  # Potência do sistema deve ser positiva
    assert capex > 0  # Custo de capital deve ser positivo
    assert parc > 0  # Parcela mensal deve ser positiva
    assert total_sem >= 0  # Total sem solar não pode ser negativo
    assert total_com >= 0  # Total com solar não pode ser negativo