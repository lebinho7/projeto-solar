import numpy as np
from math import ceil
from . import config
import logging
logger = logging.getLogger(__name__)

# Parâmetros básicos de hardware usados nos cálculos
DB_HARDWARE = {
    'MODULO': {'W': config.MODULO_W, 'AREA': config.MODULO_AREA_M2, 'PESO': config.MODULO_PESO_KG},
}

def imprimir_relatorio_tecnico(qtd, pot_inv_w):
    """Imprime os detalhes físicos e elétricos no console."""
    area = qtd * DB_HARDWARE['MODULO']['AREA']
    peso = qtd * (DB_HARDWARE['MODULO']['PESO'] + 2)  # +2kg estrutura

    # Cálculo Elétrico Básico
    i_nom = pot_inv_w / 220
    disj = next((d for d in [10, 16, 20, 25, 32, 40, 50, 63, 80] if d >= i_nom * 1.25), 63)
    cabo = "4.0mm²" if disj > 20 else "2.5mm²"
    if disj > 32: cabo = "6.0mm²"
    if disj > 50: cabo = "10.0mm²"

    print("\n" + "=" * 60)
    print("🛠️  RELATÓRIO TÉCNICO DE ENGENHARIA (ESTRUTURA & ELÉTRICA)  🛠️")
    print("=" * 60)
    logger.info("Engenharia: qtd_modulos=%s, inversor_w=%s, area_m2=%.2f, peso_kg=%.0f", qtd, pot_inv_w, area, peso)
    print(f"🏗️  ESTRUTURA E TELHADO:")
    print(f"    • Área Necessária: {area:.1f} m² (Livre de sombras)")
    print(f"    • Peso Total (Carga): {peso:.0f} kg")
    print(f"    • Distribuição: {peso / area:.1f} kg/m²")
    print("-" * 60)
    print(f"⚡  CONEXÃO ELÉTRICA:")
    print(f"    • Inversor Selecionado: {pot_inv_w / 1000:.1f} kW")
    print(f"    • Corrente de Saída: {i_nom:.1f} A")
    print(f"    • Disjuntor Recomendado: {disj} A (Curva C)")
    print(f"    • Cabo CA Recomendado: {cabo}")
    print("=" * 60)


def _to_month_array(data):
    """Converte dict mensal {'JAN':..., ...} ou sequência em np.array de 12 meses."""
    if isinstance(data, dict):
        order = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        return np.array([data.get(m) for m in order], dtype=float)
    return np.asarray(data, dtype=float)

def calcular_tudo(consumo_kwh_mes, taxa_min_kwh, irr_mensal, temp_mensal, financiar=False, fin_dados=None, inflacao_override=None, degradacao_override=None):
    """
    Dimensiona o sistema, estima custos e simula fluxo de caixa em 25 anos (300 meses).

    Retorna:
        (qtd_modulos, potencia_wp, capex, parcela_mensal, conta_antiga[], conta_nova[], saldo[], total_sem, total_com)
    """
    irr = _to_month_array(irr_mensal)
    temp = _to_month_array(temp_mensal)
    irr_media = float(np.mean(irr)) if irr.size else 4.5  # HSP média
    temp_media = float(np.mean(temp)) if temp.size else 25.0

    perda_termica = max(0.0, (temp_media + 20 - 25) * 0.0035)  # coeficiente simplificado
    PR = max(config.PR_MINIMO, config.PR_BASE - perda_termica)

    pot_necessaria_kwp = (consumo_kwh_mes / (irr_media * 30.0 * PR))
    qtd = max(2, ceil((pot_necessaria_kwp * 1000) / DB_HARDWARE['MODULO']['W']))
    if qtd % 2 != 0:
        qtd += 1
    pot_wp = qtd * DB_HARDWARE['MODULO']['W']

    # Seleção simples de inversor
    if pot_wp < 4000:
        inv_w = 3000
    elif pot_wp < 6500:
        inv_w = 5000
    elif pot_wp < 10000:
        inv_w = 8000
    else:
        inv_w = 10000

    # Custos aproximados
    custo_hardware = (qtd * 620.0) + (inv_w * 0.8)
    capex = custo_hardware * 2.1

    # Financiamento (Price)
    parcela = 0.0
    meses = 0
    if financiar and fin_dados:
        taxa_aa, meses = fin_dados
        try:
            i = (1.0 + float(taxa_aa) / 100.0) ** (1.0 / 12.0) - 1.0
            if meses and meses > 0:
                parcela = capex * ((i * (1 + i) ** meses) / ((1 + i) ** meses - 1))
        except Exception:
            parcela = 0.0

    # Simulação mensal 25 anos
    inflacao = float(inflacao_override) if inflacao_override is not None else config.INFLACAO_ENERGETICA_AA
    tarifa_base = config.TARIFA_BASE_R_KWH
    fio_b = (tarifa_base * config.FIO_B_COMPONENTE) * config.FIO_B_FATOR

    conta_antiga = []
    conta_nova = []
    saldo = []
    saldo_acum = -capex if not financiar else 0.0

    for m in range(300):
        ano = m // 12
        idx = m % 12
        tar = tarifa_base * ((1 + inflacao) ** ano)

        # Consumo sem solar
        conta_full = consumo_kwh_mes * tar
        conta_antiga.append(conta_full)

        # Geração estimada no mês
        hsp = irr[idx] if irr.size == 12 else irr_media
        degr = float(degradacao_override) if degradacao_override is not None else config.DEGRADACAO_ANUAL
        ger_kwh = (pot_wp / 1000.0) * hsp * 30.0 * PR * (1 - degr * ano)

        inj, auto = ger_kwh * 0.65, ger_kwh * 0.35
        cons_rede = max(0.0, consumo_kwh_mes - auto)
        cred = min(inj, cons_rede)
        taxa_uso = (cons_rede - cred) * tar + (cred * fio_b * ((1 + inflacao) ** ano))
        conta_mes = max(taxa_uso, taxa_min_kwh * tar)

        pgto_fin = parcela if (m < meses) else 0.0
        desembolso = conta_mes + pgto_fin
        conta_nova.append(desembolso)

        saldo_acum += (conta_full - desembolso)
        saldo.append(saldo_acum)

    total_sem = float(np.sum(conta_antiga))
    total_com = float(np.sum(conta_nova)) + (0.0 if financiar else capex)

    return (
        qtd,
        pot_wp,
        float(capex),
        float(parcela),
        conta_antiga,
        conta_nova,
        saldo,
        total_sem,
        total_com,
    )