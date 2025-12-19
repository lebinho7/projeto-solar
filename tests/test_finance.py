import pytest
from src.finance import simular_financiamento


def test_simular_financiamento_basico():
    capex = 10000.0
    taxa_aa = 12.0
    meses = 24
    consumo = 300.0
    tarifa_atual = 1.00
    tarifa_solar = 0.30

    res = simular_financiamento(capex, taxa_aa, meses, consumo, tarifa_atual, tarifa_solar)

    assert set(res.keys()) == {"parcela_mensal", "economia_mensal", "tempo_retorno"}
    assert res["parcela_mensal"] > 0
    assert res["economia_mensal"] > 0
    assert res["tempo_retorno"] > 0