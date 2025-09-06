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


@app.route('/comparar',methods =['POST','GET'])
def comparar():
   opcoes =[
       'beer_servings',
       'spirit_servings',
       'wine_servings' ]

   if request.method == "POST":
        eixoX = request.form.get('eixo_x')
        eixoY = request.form.get('eixo_y')
        if eixoX == eixoY:
         return "<marquee> Você fez besteira ... escolha tabelas diferentes.... </marquee>"
        conn = sqlite3.connect(f'{caminho}banco01.bd') 
        df = pd.read_sql_query("SELECT country, {}, {} FROM Bebidas".format(eixoX, eixoY), conn)
        conn.close()
        figuraComparar = px.scatter(
            df,
            x = eixoX,
            y = eixoY,
            title= f"Comparação entre {eixoX} VS {eixoY}"            
        )

        figuraComparar.update_traces(
            textposition = "top center"
        )

        return figuraComparar.to_html()

   

   return render_template_string('''
    <!--Isso é um comentario em html --> 
       <style>
     /* Estilo global com logo de fundo */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(to right, #f2f6f9, #dbe9f4);
    background-image: url('https://cdn-icons-png.flaticon.com/512/1046/1046784.png'); /* Logo de bebida (pode trocar) */
    background-repeat: no-repeat;
    background-position: center;
    background-size: 200px;
    background-attachment: fixed;
    opacity: 1;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
}

/* Fundo branco do formulário */
form {
    background-color: white;
    padding: 30px 40px;
    margin-top: 60px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 90%;
    z-index: 1;
}

/* Título */
h2 {
    text-align: center;
    color: #333;
    font-size: 24px;
    margin-bottom: 20px;
}

/* Labels */
label {
    display: block;
    margin: 15px 0 5px;
    font-weight: 600;
    color: #444;
}

/* Selects */
select {
    width: 100%;
    padding: 10px;
    font-size: 15px;
    border: 1px solid #ccc;
    border-radius: 6px;
    background-color: #f9f9f9;
    transition: border-color 0.3s;
}

select:focus {
    border-color: #28a745;
    outline: none;
    background-color: #fff;
}

/* Espaçamento entre quebras de linha */
br + br {
    margin-bottom: 15px;
    display: block;
}

/* Botão verde */
input[type="submit"] {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    background-color: #28a745; /* Verde */
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin-top: 20px;
    transition: background-color 0.3s;
}

input[type="submit"]:hover {
    background-color: #218838;
}

    background-image: url('https://cdn-icons-png.flaticon.com/512/1046/1046784.png');


       </style>                                                     
    <h2> Comparar Campos</h2>  
    <form method="POST">
        <label for="eixo_x"> Eixo X:</label>
        <select name="eixo_x">
          {% for opcao in opcoes %}                   
          <option value="{{opcao}}">{{opcao}}</option>
          {% endfor %}
        </select>
        <br></br>

        <label for="eixo_y"> Eixo Y: </label>
        <select name="eixo_y">
         {% for opcao in opcoes%}
         <option value="{{opcao}}">{{opcao}}</option>
         {% endfor %}
        </select>
        <br></br>

        <input type="submit" "value="--Comparar--">
    </form>    
''', opcoes = opcoes)


@app.route('/ver', methods=['GET', 'POST'])
def ver_tabela():
    if request.method =="POST":
       nome_tabela =request.form.get('tabela')
       if nome_tabela not in ['Bebidas','vingadores']:
        return "Tabela errada rapaz...pensa que vai onde?"
       conn = sqlite3.connect(f'{caminho}banco01.bd' )
       df = pd.read_sql_query(f"SELECT * FROM, {nome_tabela} ",conn)
       conn.close()
       tabela_html =df.to.html(classes='table-striped')
       return f'''
       <h3> Conteudo da tabela{nome_tabela}:</h3>
       {tabela_html}
      '''
    return render_template_string("""
    <h3> Visualizar tabelas!</h3>
    <form>
      <label for ="tabela">Selecione uma tabela:</label>
      <select name ="tabela">
      <option value ="Bebidas"> BEBIDAS </option>
      <option value ="vingadores"> Vingadores</option>
      </select>
      <input type ="submit" value=" Consultar">
     </form>

 """)

@app.route('/upload',methods =['GET','POST'])
def upload():
    if request.method == "POST":
        recebido = request.files ['c_arquivo']
        if not recebido:
          return "Nenhum arquivo foi recebido"
        dfAvengers =pd.read_csv(recebido, encoding='latin1')
        conn = sqlite3.connect(f'{caminho}banco01.bd' )
        dfAvengers.to_sql("vingadores",conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        return " Sucesso! Tabela vingadores armazenada no banco de dados"
    
    return ''' 

   <h2> Upload da tabela Avengers</h2>
   <form methods ="POST" enctype ='multipart/form_data'>
    <input type ='file' name='c_arquivo' accept ='.csv'>
    <input type = 'submit' value ='Carregar'>
     
       </form>
    '''
   

if __name__ == '__main__':
  criarBancoDados()
  app.run(debug=True)


