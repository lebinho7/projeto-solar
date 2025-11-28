# Projeto Solar

Este projeto é uma aplicação para o dimensionamento e análise de sistemas de energia solar. Ele permite que os usuários insiram dados sobre consumo de energia e localização geográfica, e fornece estimativas de custo, dimensionamento do sistema e visualizações dos resultados.

## Estrutura do Projeto

O projeto é organizado da seguinte forma:

- **src/**: Contém os módulos principais da aplicação.
  - **__init__.py**: Torna o diretório um pacote Python.
  - **main.py**: Ponto de entrada da aplicação.
  - **geodata.py**: Funções para obter dados geográficos e climáticos.
  - **engineering.py**: Funções para cálculos de engenharia e relatórios técnicos.
  - **finance.py**: Funções para cálculos financeiros e simulações.
  - **viz.py**: Funções para visualização de dados e geração de gráficos.

- **notebooks/**: Contém um notebook Jupyter para execução interativa do projeto.
  - **projeto_solar.ipynb**: Implementação interativa do projeto.

- **data/**: Contém dados utilizados no projeto.
  - **sample_inputs.csv**: Dados de entrada de exemplo.
  - **README.md**: Informações sobre os dados utilizados.

- **tests/**: Contém testes automatizados para garantir a funcionalidade do projeto.
  - **test_engineering.py**: Testes para o módulo de engenharia.
  - **test_finance.py**: Testes para o módulo financeiro.

- **requirements.txt**: Lista de dependências do projeto.

- **pyproject.toml**: Configurações do projeto.

- **.gitignore**: Arquivos e diretórios a serem ignorados pelo Git.

## Instalação

Para instalar as dependências do projeto, execute:

```
pip install -r requirements.txt
```

## Uso

Para executar a aplicação, utilize o seguinte comando:

```
python src/main.py
```

Siga as instruções na tela para inserir os dados necessários e obter os resultados.