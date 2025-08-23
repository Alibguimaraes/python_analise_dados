import pandas as pd 

#carregar dados da planilha 

caminho = 'C:/Users/sabado/Desktop/Python AD Aline/01_base_vendas.xlsx'

df1 = pd.read_excel(caminho,sheet_name='Relatório de Vendas')
df2 = pd.read_excel(caminho, sheet_name='Relatório de Vendas1')

# exibir as primeiras linhas das tabelas

print('----------Primeiro Relatório')
print(df1.head())

print('--------Segundo Relatório-----')
print(df2.head())

#verificar se há duplicatas 

print('Duplicatas no relatório 01')
print(df1.duplicated().sum())

print('Duplicata no relatório 02')
print(df2.duplicated().sum())

#vamos consolidar as duas tabelas

print('Dados consolidados!')

dfConsolidado = pd.concat([df1,df2],ignore_index=True)

print(dfConsolidado.head())


#Vamos exibir o numero de clientes por cidade
clientesPorCidade = dfConsolidado.groupby('Cidade')['Cliente'].nunique().sort_values(ascending =False)

print('clientes por cidade')
print(clientesPorCidade)

#numero de vendas por plano
VendasPorPlano = dfConsolidado ['Plano Vendido'].value_counts()
print('Numero de vendas por plano')
print(VendasPorPlano)

#exibir as 3 cidades com mais clientes:
top3Cidades = clientesPorCidade.head(3)

#top3Cidades = clientesPorcidade.sort_values(ascending=False).head(3)

print('Top  3 cidades')
print(top3Cidades)

#adicionar uma nova coluna de status ( exemplo ficticio de analise)
#vamos classificar os planos como 'premium' se for enterprise , os demais serão 'padrão

dfConsolidado['Status'] = dfConsolidado['Plano Vendido'].apply(lambda x:'Premium' if x == 'Enterprise' else 'Padrão')


#exibir a distribuição dos status
statusDist = dfConsolidado ['Status'].value_counts

print('Distribuição dos status')
print(statusDist)

#Salvar a tabela em um arquivo novo
# Primeiro em Excel

dfConsolidado.to_excel('dados_consolidados.xlsx', index =False)

print('Dados salvos na planilha do Excel')

#Depois em csv

dfConsolidado.to_csv('dados_consolidados.csv',index=False)
print('Dados salvos em CSV')

#mensagem final

print('---Programa Finalizado---')