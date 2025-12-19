import numpy as np
from .geodata import get_data
from .engineering import calcular_tudo, imprimir_relatorio_tecnico
# from .finance import calcular_financiamento  # (não utilizado no fluxo atual)
from .viz import plotar_dashboard_final

def ler_numero_valido(mensagem, tipo=float):
    """
    Lê um número do usuário com validação e mensagens amigáveis.
    Aceita vírgula como separador decimal e rejeita valores negativos.
    tipo: float (valores decimais) ou int (inteiros).
    """
    while True:
        try:
            bruto = input(mensagem).strip().replace(',', '.')
            valor = tipo(bruto)
            if valor < 0:
                print("⚠️  Por favor, digite um valor positivo.")
                continue
            return valor
        except ValueError:
            exemplo = "350.5" if tipo is float else "12"
            print(f"❌ Entrada inválida. Digite apenas números (ex: {exemplo})")

def main():
    print("\n=== ☀️ SISTEMA SOLAR V11 (HÍBRIDO) ☀️ ===")
    while True:
        cidade = input("\nCidade: ").strip()
        if cidade.lower() == 'sair':
            return
        irr, temp = get_data(cidade)
        if irr is not None:
            break
        print("⚠️ Não foi possível obter dados (cidade inválida ou sem conexão). Tente novamente.")

    consumo = ler_numero_valido("Média de Consumo (kWh): ", float)
    taxa_min = ler_numero_valido("Taxa mínima de conexão (kWh): ", int)
    
    financiar = input("Cliente quer financiar? (s/n): ").strip().lower() == 's'
    if financiar:
        taxa_aa = ler_numero_valido("Taxa (% a.a): ", float)
        meses = ler_numero_valido("Meses: ", int)
        fin_data = (taxa_aa, meses)
    else:
        fin_data = None

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