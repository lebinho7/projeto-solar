import numpy as np
from src.engineering import calcular_tudo


def test_calcular_tudo_shapes():
    irr = {m: 5.0 for m in ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']}
    temp = {m: 26.0 for m in ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']}

    qtd, pot, capex, parc, ant, novo, saldo, tot_sem, tot_com = calcular_tudo(
        consumo_kwh_mes=300.0,
        taxa_min_kwh=50,
        irr_mensal=irr,
        temp_mensal=temp,
        financiar=False,
        fin_dados=None,
    )

    assert isinstance(qtd, int) and qtd > 0
    assert isinstance(pot, (int, float)) and pot > 0
    assert isinstance(capex, float) and capex > 0
    assert len(ant) == 300 and len(novo) == 300 and len(saldo) == 300
    assert isinstance(tot_sem, float) and isinstance(tot_com, float)
import pytest
from src.engineering import calcular_tudo, imprimir_relatorio_tecnico

def test_calcular_tudo():
    # Teste com dados de entrada conhecidos
    consumo = 300  # kWh
    taxa_min = 30  # kWh
    irr = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5]  # Irradiação média mensal
    temp = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]  # Temperatura média mensal
    financiar = False
    fin_dados = None

    qtd, pot_wp, capex, parc, vec_antiga, vec_novo, vec_saldo, total_sem, total_com = calcular_tudo(consumo, taxa_min, irr, temp, financiar, fin_dados)

    assert qtd > 0
    assert pot_wp > 0
    assert capex > 0
    assert total_sem >= 0
    assert total_com >= 0

def test_imprimir_relatorio_tecnico(capfd):
    qtd = 10
    pot_inv_w = 5000

    imprimir_relatorio_tecnico(qtd, pot_inv_w)

    captured = capfd.readouterr()
    assert "RELATÓRIO TÉCNICO DE ENGENHARIA" in captured.out
    assert "Área Necessária" in captured.out
    assert "Peso Total" in captured.out
    assert "Inversor Selecionado" in captured.out