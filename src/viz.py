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