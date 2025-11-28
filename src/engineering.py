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