# ☀️ SolarMaster Pro: Sistema Inteligente de Engenharia Fotovoltaica

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Sobre o Projeto

O **SolarMaster Pro** é uma aplicação avançada para dimensionamento técnico e análise de viabilidade financeira de sistemas de energia solar.

Diferente de calculadoras simples, este software integra **Dados Climáticos da NASA**, **Geolocalização Automática** e **Matemática Financeira** (adaptada à Lei 14.300) para gerar propostas comerciais precisas e seguras. O objetivo é eliminar o "achismo" no dimensionamento solar, entregando segurança técnica e clareza financeira.

---

## 🚀 Funcionalidades Principais

* **📍 Inteligência Geográfica:** Localização automática da cidade e coleta de dados de Irradiação Solar e Temperatura via API da NASA POWER.
* **⚡ Engenharia de Detalhe:** Gera um "Datasheet" automático, especificando:
    * Quantidade de módulos e potência do inversor (com Overloading).
    * Área de telhado necessária e carga estática (peso).
    * Dimensionamento de cabos elétricos e disjuntores de proteção.
* **💰 Análise Financeira "Blindada":**
    * Cálculo de Payback, VPL e Economia Acumulada.
    * Considera a **Lei 14.300** (Taxação do Fio B) e Taxa Mínima de Disponibilidade.
    * Simula cenários de Inflação Energética e Financiamento Bancário.
* **📊 Dashboards Visuais:** Geração de relatórios gráficos (Matplotlib) salvos automaticamente em alta resolução.

---

## 📂 Estrutura do Projeto

A arquitetura foi pensada de forma modular para facilitar a manutenção e escalabilidade:

- **src/**: Núcleo da aplicação (Código Fonte).
  - **main.py**: Orquestrador principal. Recebe inputs e chama os módulos.
  - **geodata.py**: Conexão com APIs externas (Nominatim/NASA).
  - **engineering.py**: Motor de cálculo físico (Dimensionamento, Cabos, Estrutura).
  - **finance.py**: Motor matemático (Fluxo de caixa, Inflação, Financiamento).
  - **viz.py**: Motor gráfico (Geração dos Dashboards e imagens).

- **notebooks/**: Ambiente de testes e prototipagem.
  - **projeto_solar.ipynb**: Versão interativa usada para desenvolvimento exploratório.

- **data/**: Armazenamento de arquivos auxiliares.
  - **sample_inputs.csv**: Planilha para testes em lote (batch).

- **tests/**: Controle de qualidade (QA).
  - **test_engineering.py**: Validação dos cálculos de dimensionamento.
  - **test_finance.py**: Validação das fórmulas financeiras.

---

## 📦 Instalação e Requisitos

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/solar-master.git](https://github.com/seu-usuario/solar-master.git)
    cd solar-master
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Principais libs: numpy, matplotlib, requests, geopy)*

---

## ▶️ Como Usar

Execute o arquivo principal através do terminal:

```bash
python src/main.py

Siga as instruções na tela para inserir os dados necessários e obter os resultados.