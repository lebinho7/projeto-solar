import argparse
import logging
from .geodata import get_data, clear_cache
from .engineering import calcular_tudo
from .viz import plotar_dashboard_final

logger = logging.getLogger(__name__)


def main():
    if not logging.getLogger().handlers:
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
    parser.add_argument("--clear-cache", action="store_true", help="Remove cache da cidade antes de coletar")
    parser.add_argument("--output", help="Diretório para salvar o relatório PNG")
    parser.add_argument("--no-cache-fallback", action="store_true", help="Não usa cache vencido se a coleta falhar")
    parser.add_argument("--cache-ttl-dias", type=float, default=None, help="TTL do cache em dias (padrão 30). Use 0 para desativar TTL")
    parser.add_argument("--nasa-retries", type=int, default=3, help="Número de tentativas para consultar a NASA (padrão 3)")
    parser.add_argument("--nasa-timeout", type=int, default=15, help="Timeout (s) por tentativa ao consultar a NASA (padrão 15)")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"], help="Nível de log")
    args = parser.parse_args()
    # Ajuste de log dinâmico
    try:
        logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    except Exception:
        pass

    if args.clear_cache:
        if clear_cache(args.cidade):
            print(f"🧹 Cache removido para: {args.cidade}")
        else:
            print(f"ℹ️ Nenhum cache removido para: {args.cidade}")

    if args.financiar:
        if args.meses <= 0 or args.taxa_aa <= 0:
            logger.error("Para financiar, informe --taxa-aa > 0 e --meses > 0")
            raise SystemExit(2)
    # TTL em segundos (None usa padrão do módulo)
    ttl_seconds = None
    if args.cache_ttl_dias is not None:
        try:
            ttl_seconds = max(0, int(args.cache_ttl_dias * 86400))
        except Exception:
            ttl_seconds = None

    irr, temp = get_data(
        args.cidade,
        refresh_cache=args.refresh_cache,
        allow_stale_fallback=(not args.no_cache_fallback),
        ttl_seconds=ttl_seconds if ttl_seconds is not None else None,
        retries=max(0, args.nasa_retries),
        nasa_timeout=max(1, args.nasa_timeout)
    )
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
        args.cidade, pot, ant, novo, saldo, tot_sem, tot_com, parc, args.financiar,
        show=(not args.no_show), out_dir=args.output
    )
    if path_png:
        print(f"\n✅ Arquivo gerado: {path_png}")


if __name__ == "__main__":
    main()
