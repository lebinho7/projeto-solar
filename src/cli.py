import argparse
import logging
from .geodata import get_data
from .engineering import calcular_tudo
from .viz import plotar_dashboard_final


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Simulador Solar - CLI")
    parser.add_argument("--cidade", required=True, help="Cidade, UF (ex.: Fortaleza, CE)")
    parser.add_argument("--consumo", type=float, required=True, help="Consumo médio mensal em kWh")
    parser.add_argument("--taxa", type=int, choices=[30, 50, 100], required=True, help="Taxa mínima (30, 50, 100 kWh)")
    parser.add_argument("--financiar", action="store_true", help="Ativa simulação com financiamento")
    parser.add_argument("--taxa-aa", type=float, default=0.0, help="Taxa de juros anual (% a.a.) se financiar")
    parser.add_argument("--meses", type=int, default=0, help="Prazo do financiamento em meses")
    parser.add_argument("--no-show", action="store_true", help="Não exibe a janela do gráfico (apenas salva PNG)")
    parser.add_argument("--inflacao", type=float, help="Sobrescreve inflação anual (%)")
    parser.add_argument("--degradacao", type=float, help="Sobrescreve degradação anual dos módulos (%)")
    parser.add_argument("--refresh-cache", action="store_true", help="Ignora cache e coleta dados novamente")
    args = parser.parse_args()

    irr, temp = get_data(args.cidade, refresh_cache=args.refresh_cache)
    if irr is None:
        raise SystemExit("Cidade não encontrada. Verifique o nome (ex.: 'Fortaleza, CE').")

    fin_data = (args.taxa_aa, args.meses) if args.financiar else None
    (qtd, pot, capex, parc, ant, novo, saldo, tot_sem, tot_com) = calcular_tudo(
        args.consumo, args.taxa, irr, temp, args.financiar, fin_data,
        inflacao_override=args.inflacao, degradacao_override=args.degradacao
    )

    print("\n💰 RESUMO COMERCIAL:")
    print(f"   Investimento Total: R$ {capex:,.2f}")
    if args.financiar:
        print(f"   Parcela Mensal: R$ {parc:,.2f}")

    # Plota e salva
    path_png = plotar_dashboard_final(
        args.cidade, pot, ant, novo, saldo, tot_sem, tot_com, parc, args.financiar, show=(not args.no_show)
    )
    if path_png:
        print(f"\n✅ Arquivo gerado: {path_png}")


if __name__ == "__main__":
    main()
