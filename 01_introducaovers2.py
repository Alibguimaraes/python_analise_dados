import pandas as pd 

# Carregar dados da planilha 
caminho = 'C:/Users/sabado/Desktop/Python AD Aline/01_base_vendas.xlsx'

# Usando a mesma sheet_name para ambas as tabelas
df1 = pd.read_excel(caminho, sheet_name='Relatório de Vendas')
df2 = pd.read_excel(caminho, sheet_name='Relatório de Vendas')

# Exibir as primeiras linhas das tabelas
print('----------Primeiro Relatório')
print(df1.head())

print('--------Segundo Relatório-----')
print(df2.head())

# Verificar se há duplicatas 
print('Duplicatas no relatório 01')
print(df1.duplicated().sum())

print('Duplicata no relatório 02')
print(df2.duplicated().sum())

# Consolidar as duas tabelas
print('Dados consolidados!')
dfConsolidado = pd.concat([df1, df2], ignore_index=True)
print(dfConsolidado.head())

# Exibir o número de clientes por cidade
clientesPorCidade = dfConsolidado.groupby('Cidade')['Cliente'].nunique().sort_values(ascending=False)
print('Clientes por cidade')
print(clientesPorCidade)

# Número de vendas por plano
VendasPorPlano = dfConsolidado['Plano Vendido'].value_counts() # Corrigido: 'value_counts()'
print('Número de vendas por plano')
print(VendasPorPlano)

# Exibir as 3 cidades com mais clientes:
top3Cidades = clientesPorCidade.head(3)
print('Top 3 cidades')
print(top3Cidades)

# Adicionar uma nova coluna de status (exemplo fictício de análise)
# Classificar os planos como 'Premium' se for 'Enterprise', os demais serão 'Padrão'
dfConsolidado['Status'] = dfConsolidado['Plano Vendido'].apply(lambda x: 'Premium' if x == 'Enterprise' else 'Padrão')

# Opcional: Para ver o resultado da nova coluna
print('\nDataFrame com a nova coluna "Status":')
print(dfConsolidado[['Plano Vendido', 'Status']].head())