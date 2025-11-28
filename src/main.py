import numpy as np
import pandas as pd
from geodata import get_data
from engineering import calcular_tudo, imprimir_relatorio_tecnico
from finance import calcular_financiamento
from viz import plotar_dashboard_final

def main():
    print("\n=== ☀️ SISTEMA SOLAR V11 (HÍBRIDO) ☀️ ===")
    while True:
        cidade = input("\nCidade: ").strip()
        if cidade.lower() == 'sair':
            return
        irr, temp = get_data(cidade)
        if irr is not None:
            break
        print("❌ Cidade não encontrada. Tente 'Macapa, AP'")

    consumo = float(input("Média de Consumo (kWh): "))
    taxa_min = int(input("Taxa mínima de conexão (kWh): "))
    
    financiar = input("Cliente quer financiar? (s/n): ").strip().lower() == 's'
    fin_data = (float(input("Taxa (% a.a): ")), int(input("Meses: "))) if financiar else None

    print("\n⏳ Calculando Engenharia e Financeiro...")
    qtd, pot, capex, parc, ant, novo, saldo, tot_sem, tot_com = calcular_tudo(consumo, taxa_min, irr, temp, financiar, fin_data)

    print(f"\n💰 RESUMO COMERCIAL:")
    print(f"   Investimento Total: R$ {capex:,.2f}")
    if financiar:
        print(f"   Parcela Mensal: R$ {parc:,.2f}")

    input("\n[ENTER] para abrir os Gráficos...")
    plotar_dashboard_final(cidade, pot, ant, novo, saldo, tot_sem, tot_com, parc, financiar)

if __name__ == "__main__":
    main()