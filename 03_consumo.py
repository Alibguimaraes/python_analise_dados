from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random
import os



caminho = "C:/Users/sabado/Desktop/Python AD Aline/"
tabela = ["drinks.csv" , "avengers.csv"]

codHtml =''' 
<h1>Dashboards -Consumo de Alcool</h1>
<h2>Parte 01</h2>
    <ul>
        <li><a href="/grafico1"> Top 10 paisses em consumo de alcool  </a></li>
        <li><a href="/grafico2">  Media de consumo por região </a></li>
        <li><a href="/grafico3"> Consumo total por Região  </a></li>
        <li><a href="/grafico4">  Comparativo entre tipo de bebidas </a></li>
        <li><a href="/pais">   Insights por pais </a></li>
    </ul>
<h2> Parte  02</h2>
      <ul>
        <li><a href="comparar"> Comparar  </a> </li>
        <li><a href="/upload">  Upload CVS Vingadores </a> </li>
        <li><a href="/apagar">  Apagar Tabela </a> </li>
        <li><a href="/ver">  Ver Tabela </a> </li>
        <li><a href="/vaaa">  V.A.A (Vingadores Alcolicos Anonimos) </a> </li>
    </ul>
'''


#carregar csv
def carregarCsv():


    #carregar o arquivo drinnks
    #dfDrinks = pd.read_csv ("C:/Users/sabado/Desktop/Python AD Aline/drinks.csv")      
 
    #caminho = "C:/Users/sabado/Desktop/Python AD Aline"
    #tabela01 = "drinks.csv"
    #tabela02 = "avengers.csv"
    #tabela = ["drinks.csv" , "avengers.csv"]
    #dfdrinks = pd.read_csv (f"{caminho}{tabela [0]}")
    #dfAvengers = pd.read_csv (f"{caminho}{tabela [1]}")
    try:
        dfDrinks = pd.read_csv(os.path.join(caminho,tabela[0]))
        dfAvengers = pd.read_csv(os.path.join(caminho,tabela[1]),encoding='latin1')
        return dfDrinks, dfAvengers
    except Exception as erro:
        print(f"Erro ao carregar os arquivos CSV:{erro}")
        return None , None

def criarBancoDados():
    conn = sqlite3.connect(f"{caminho}banco01.bd")
    #carregar dados usando nossa função criada anteriormente
    dfDrinks ,dfAvengers = carregarCsv()
    
    if dfDrinks is None or dfAvengers is None:
        print("Falha no carregar os dados!")
        return
    
# inserir as tabelas no banco do dados
    dfDrinks.to_sql("bebidas", conn,  if_exists="replace", index=False)
    dfAvengers.to_sql("vingadores", conn,if_exists="replace",index=False)
    conn.commit()
    conn.close()

app = Flask (__name__)
# O mundo fica aqui!!!

@app.route('/')
def index():
    return render_template_string(codHtml)

@app.route('/grafico1')
def  grafico1():
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        df = pd.read_sql_query(""" 
            SELECT country, total_litres_of_pure_alcohol
            FROM bebidas 
            ORDER BY total_litres_of_pure_alcohol DESC
            LIMIT 10                      
          """, conn)

    figuraGrafico01 = px.bar(
        df,
        x = "country",
        y = "total_litres_of_pure_alcohol",
        title = "Top 10 paises com maior consumo de alcool"
    )
    return figuraGrafico01.to_html()


@app.route('/grafico2')
def  grafico2():
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        df = pd.read_sql_query(""" 
            SELECT AVG  (beer_servings) AS cerveja , AVG (spirit_servings) AS destilados, AVG(wine_servings)
            AS vinhos FROM bebidas 
                                  
          """, conn)



    df_melted = df.melt (var_name ='Bebidas', value_name ='Media de Porcoes')
    figuraGrafico02 = px.bar(
        df_melted,
        x = "Bebidas",
        y = "Media de Porcoes",
        title = "Media de consumo global por tipo"

    )
    return figuraGrafico02.to_html()

@app.route("/grafico3")
def grafico3():
    regioes ={
        "Europa":['França','Germany','Spain','Italy','Portugal'],
        "Asia":['China','Japan','India','Thailand'],
        "Africa":['Angola','Nigeria','Egypt','Algeria'],
        "Americas":['USA','Canada','Brazil','Argentina','Mexico']
    }
    dados =[]
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        # itera sobre o dicionario,de regios onde cada chave (regiao tem uma lista de paises)
        for regiao , paises in regioes.items():
            placeholders =",".join(f"'{pais}'" for pais in paises)
            query = f"""
               SELECT SUM(total_litres_of_pure_alcohol) AS total
               FROM Bebidas
               WHERE country IN ({placeholders})
            """
            total = pd.read_sql_query(query, conn).iloc[0,0]   
            dados.append({
                "Região":regiao,
                "Consumo Total":total
                })
    dfRegioes = pd.DataFrame(dados)
    figuraGrafico3 = px.pie(
        dfRegioes,
        names= "Região",
        values="Consumo Total",
        title="Consumo total por Região!"
        )
    return figuraGrafico3.to_html()

if __name__ == '__main__':
  criarBancoDados()
  app.run(debug=True)


