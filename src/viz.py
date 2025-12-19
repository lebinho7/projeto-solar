import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot_monthly_savings(old_costs, new_costs):
    dif = old_costs - new_costs
    color = '#27AE60' if dif >= 0 else '#F39C12'
    label = "ECONOMIA" if dif >= 0 else "INVESTIMENTO"
    
    plt.bar([0, 1], [old_costs, new_costs], color=['#E74C3C', color], width=0.5)
    plt.xticks([0, 1], ['Hoje', 'Com Solar'])
    plt.title(f"FLUXO MENSAL: {label} DE R$ {abs(dif):.2f}", fontweight='bold')
    plt.show()

def plot_total_savings(total_without_solar, total_with_solar):
    plt.barh([0, 1], [total_without_solar, total_with_solar], color=['#E74C3C', '#27AE60'])
    plt.yticks([0, 1], ['Sem Solar', 'Com Solar'])
    total_savings = total_without_solar - total_with_solar
    plt.text(total_without_solar * 0.5, 0.5, f"VOCÊ DEIXA DE GASTAR:\\nR$ {total_savings:,.2f}", 
             ha='center', fontsize=14, fontweight='bold', bbox=dict(fc='white', ec='green'))
    plt.title("ECONOMIA ACUMULADA (25 ANOS)", fontweight='bold')
    plt.show()

def plot_wealth_growth(wealth_over_time):
    years = np.arange(len(wealth_over_time))
    plt.fill_between(years, 0, wealth_over_time, where=(wealth_over_time >= 0), color='#27AE60', alpha=0.5)
    plt.fill_between(years, 0, wealth_over_time, where=(wealth_over_time < 0), color='#F39C12', alpha=0.5)
    plt.plot(years, wealth_over_time, color='#333333')
    plt.title("CRESCIMENTO PATRIMONIAL", fontweight='bold')
    plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f"{int(x/1000):,}k"))
    plt.grid(alpha=0.3)
    plt.show()

import os
import logging
from datetime import datetime

def plotar_dashboard_final(cidade, sistema_wp, conta_antiga, custo_novo, saldo, total_sem, total_com, parc, financiado, show=True, out_dir=None):
    plt.rcParams['text.color'] = '#333333'
    fig = plt.figure(figsize=(16, 10), facecolor='#F9F9F9')
    gs = fig.add_gridspec(3, 2, height_ratios=[0.15, 1, 1])

    # Cabeçalho
    ax_head = fig.add_subplot(gs[0, :]); ax_head.axis('off')
    try:
        kWp = sistema_wp/1000.0
    except Exception:
        kWp = sistema_wp
    ax_head.text(0.5, 0.5, f"PROJETO SOLAR: {cidade.upper()} ({kWp:.2f} kWp)", ha='center', fontsize=18, fontweight='bold')

    # 1. Mensal (usar o primeiro mês como referência)
    ax1 = fig.add_subplot(gs[1, 0], facecolor='#F9F9F9')
    try:
        old0 = float(conta_antiga[0])
    except Exception:
        old0 = float(conta_antiga)
    try:
        new0 = float(custo_novo[0])
    except Exception:
        new0 = float(custo_novo)
    dif = old0 - new0
    cor, lbl = ('#27AE60', "ECONOMIA") if dif >= 0 else ('#F39C12', "INVESTIMENTO")
    ax1.bar([0, 1], [old0, new0], color=['#E74C3C', cor], width=0.5)
    ax1.set_xticks([0,1]); ax1.set_xticklabels(['Hoje', 'Com Solar'])
    ax1.set_title(f"FLUXO MENSAL: {lbl} DE R$ {abs(dif):.2f}", fontweight='bold')

    # 2. Total (25 anos)
    ax2 = fig.add_subplot(gs[1, 1], facecolor='#F9F9F9')
    ax2.barh([0,1], [total_sem, total_com], color=['#E74C3C', '#27AE60'])
    ax2.set_yticks([0,1]); ax2.set_yticklabels(['Sem Solar', 'Com Solar'])
    eco_tot = total_sem - total_com
    ax2.text(max(total_sem, total_com)*0.5, 0.5, f"VOCÊ DEIXA DE GASTAR:\nR$ {eco_tot:,.2f}", ha='center', fontsize=14, fontweight='bold', bbox=dict(fc='white', ec='green'))
    ax2.set_title("ECONOMIA ACUMULADA (25 ANOS)", fontweight='bold')

    # 3. Patrimônio (saldo ao longo do tempo)
    ax3 = fig.add_subplot(gs[2, :], facecolor='#F9F9F9')
    try:
        saldo_arr = np.array(saldo, dtype=float)
    except Exception:
        saldo_arr = np.array([float(saldo)])
    anos = np.arange(len(saldo_arr))/12.0 if len(saldo_arr) > 1 else np.arange(len(saldo_arr))
    ax3.fill_between(anos, 0, saldo_arr, where=(saldo_arr>=0), color='#27AE60', alpha=0.5)
    ax3.fill_between(anos, 0, saldo_arr, where=(saldo_arr<0), color='#F39C12', alpha=0.5)
    ax3.plot(anos, saldo_arr, color='#333333')
    ax3.set_title("CRESCIMENTO PATRIMONIAL", fontweight='bold')
    ax3.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: f"{int(x/1000):,}k"))
    ax3.grid(alpha=0.3)

    plt.tight_layout()
    # Salvar PNG em reports/ com timestamp
    out_dir = out_dir or os.path.join(os.getcwd(), "reports")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception:
        out_dir = os.getcwd()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_city = cidade.split()[0]
    nome_img = os.path.join(out_dir, f"Projeto_{safe_city}_{ts}.png")
    try:
        plt.savefig(nome_img, dpi=150)
        logging.info("Dashboard salvo em %s", nome_img)
    except Exception as e:
        logging.warning("Falha ao salvar dashboard: %s", e)
        nome_img = None
    if show:
        plt.show()
    else:
        plt.close()
    return nome_img