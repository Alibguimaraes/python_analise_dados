#     _       _                  _   _   U _____ u
# U  /"\  u  |"|        ___     | \ |"|  \| ___"|/
#  \/ _ \/ U | | u     |_"_|   <|  \| |>  |  _|"  
#  / ___ \  \| |/__     | |    U| |\  |u  | |___  
# /_/   \_\  |_____|  U/| |\u   |_| \_|   |_____| 
#  \\    >>  //  \\.-,_|___|_,-.||   \\,-.<<   >> 
# (__)  (__)(_")("_)\_)-' '-(_/ (_")  (_/(__) (__)

# Autor: Seu Nome Completo
# Data: 20/09/25 
# Version: 1.0.0

from flask import Flask , request , jsonify, render_template_string
import pandas as pd
import sqlite3
import os
import plotly.graph_objs as go
from dash import Dash , html , dcc
import numpy as np
import config        # Nosso config.py
from sklearn.cluster import KMeans   
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
pasta = config.FOLDER
caminhoBD = config.DB_PATH
rotas = config.ROTAS
vazio = 0

def init_db():
    with sqlite3.connect(f'{pasta}{caminhoBD}') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia(
                mes TEXT PRIMARY KEY,
                inadimplencia REAL)
                       ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic(
                mes TEXT PRIMARY KEY,
                selic_diaria REAL)
                       ''')
        conn.commit()

@app.route(rotas[0])
def index():
    return render_template_string(f'''
        <h1> Upload de dados Economicos </h1>
        <form action= {rotas[1]} method="POST" enctype="multipart/form-data">
            <label for="campo_inadimplencia"> Arquivo de Inadimplencia (CSV): </label>
            <input name="campo_inadimplencia" type="file" required>              

            <label for="campo_selic"> Arquivo de Taxa Selic (CSV): </label>
            <input name="campo_selic" type="file" required><br>
            <input type ="submit" value ="Fazer Upoload "><br>
            </form>
            <br><br>
            <a href ="{rotas[2]}">Consultar dados Armazenados </a> <br> 
            <a href ="{rotas[3]}">Visualizar Graficos </a> <br>
            <a href ="{rotas[4]}">Editar Inadimplencia </a> <br>
            <a href ="{rotas[5]}"> Analiar Crorrelação </a> <br>       
                              
      ''')
@app.route(rotas[1], methods=['POST','GET'])
def upload():
    inad_file=request.files.get('campo_inadimplencia')
    selic_file =request.files.get('campo_selic')
    
    if not inad_file or not selic_file:
        return jsonify({"Erro":" Ambos arquivos deve ser envidados" }),406
    

    inad_df = pd.read_csv(
        inad_file,
        sep =';',
        nomes =['data','inadimplencia '],
        header = 0
    )

   
    selic_df = pd.read_csv(
        selic_file ,
        sep =';',
        nomes =['data','selic_diaria'],
        header = 0
    )
    inad_df['data'] =pd.to_datetime(
         inad_df['data'],
         format='%d/%m/%Y'
    )
    selic_df['data'] =pd.to_datetime(
        selic_df['data'],
        format='%d/%m/%Y')
    
    inad_df['mes'] = inad_df['data'].dt.to_period ('M').astype(str).drop_duplicates()
    selic_df['mes'] = selic_df['data'].dt.to_period ('M').astype(str)

    #inad_df ['mes'] =inad_df [['mes','inadimplencia']].drop_duplicates()
    selic_mensal = selic_df.groupby('mes')['selic_diaria'].mean().reset_index()
    with sqlite3.connect(f'{pasta}{caminhoBD}' ) as conn:
        inad_df.to.sql(
            'inadimplancia',
            conn ,
            if_exists ="replace",
            index =False

        )
        selic_df.to.sql(
            'selic',
            conn ,
            if_exists ="replace",
            index =False

        )
    return jsonify({" Mensagem":" Dados cadastrados com sucesso!"}),200
@app.route(rotas[2],methods=['POST','GET'])
def consultar():
    if request.method =="POST":
        tabela =request.form.get("campo_tabela")
        if tabela not in ['inadimplencia','selic']:
            return jsonify({"Erro": "Tabela"}),400
        with sqlite3.connect(f'{pasta}{caminhoBD}') as conn:
            df= pd.read_sql_query(f'SELECT * FROM {tabela}', conn)
            return df.to_html(index=False)

    #aqui tem um cone """(reservando esse espaço para mais tarde)"


    return render_template_string(f'''
   <h1>Consultar de Tabelas</h1>
        <form method ="POST">
        <label nome =" campo_tabela> Escolha uma tabela:</label>
         <selec name ="campo_tabela">
             <option value ="inadimplencia"> Inadimplencia</option>
             <option value = "selec"> Taxa Selic</option>
            <option value = "usuarios"> Usuarios</option>
              </select>
              <input type ="submit" value="Consultar">
        </form>
        <br>
        <a href ="{rotas[0]}"> Voltar </a>                          
                             
    
''')

@app.route(rotas[4], methods=['POST','GET'])
def editar_inadimplencia():

    #######################
    if request.method =="PST":
        mes= request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:

         novo_valor = float(novo_valor) 

        except:
            return jsonify({"Erro:":"Valoe invalido"}),418
        with sqlite3.connect(f'{pasta}{caminhoBD}') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE inadimplencia
            SET inadimplencia =?
            WHERE mes = ?
                        
        ''', (novo_valor, mes))
            conn.commit()
            
    return render_template_string(f'''
   <h1>Editar Inadimplencia </h1>
        <form method ="POST">
        <label for ="campo-mes" >Mês (AAAA-MM) </label>
        <input type ="text" name="campo-mes"><br>
                               
        <label for ="campo-mes"> Novo valor </label>
        <input type ="text" name=" campo_valor"><br>
              <input type ="subimt" value="Salvar">
        </form>
        <br>
        <a href ="{rotas[0]}"> Voltar </a>                          
                             
    
''')


@app.route(rotas[5])
def correlacao():
    with sqlite3.connect(f'{pasta}{caminhoBD}') as conn:
        inad_df = pd.read_sql_query("SELECT * FORM inadimplencia",conn)
        selic_df= pd.read_sql_query("SELECT * FORM  selic",conn)

        ## realiza uma junção entre dois dataframes usando a coluna de mes como chave
        merged =pd.merge(inad_df,selic_df, on='mes')
        
        ## calcula o coeficiente da correlação de pearson entre as duas variaveis
        correl = merged['inadimplencia'].corr(merged['selic_diaria'])
        #registra as variaveis para a regressão linear onde X é a variavel
        #independente e y é a variavel dependente

        x= merged['selic_diaria']
        y= merged['inadimplencia']
        #calcula o coeficiente da reta de regressão linear onde M é a 
        #inclinação e B é a intersercção
        m , b = np.polyfit(x,y,1 )
#oba !!! Graficos ☺☻♥♣ ◘○  ♣○♠♥ 

        fig= go.Figure()
        fig.add_trace(go.Scatter(
           x=x,
           y=y,
           mode='markers',
           name='Inadimplencia x Selic',
           marker=dict(
               color= 'rgba(0,123,255,0,8)',
               size= 12,
               line= dict(width =2 ,color = 'white'),
               symbol='circle'
           ),
           hovertemplate= 'Selic:%{x:.2f}%  <br>Inadimplencia :%{y:.2f}%<extra> </extra>'

    ))
    fig.add_trace (go.scatter(
        x= x,
        y= m* x + b,
        mode ='lines',
        line = dict(
            color= 'rgba(255,53,69,1)',
            width= 4,
            dash ='dot'

        )
    ))

    fig.update_layout(
        title = {
        'text':f'<b> Correlação entre Selic e Inadimplencia<b><span style="font-size:16 px;"> Coeficiente de Correção:{correl:.2f}</span>',
        'y':0.95,
        'x':0.85,
        'xanchor': 'center',
        'yanchor': 'top'
        },
        xaxis_title =dict(
          text ='SELIC  Média Mensal (%)',
          font =dict(
              size=18,
              family ='Arial',
              color='gray'
          )
        ),
        yaxis_title =dict(
          text ='Inadimplencia (%)',
          font =dict(
              size=18,
              family ='Arial',
              color='gray'
          )
        ),
        xaxis =dict(
            tickfont=dict(
              size=14,
              family ='Arial',
              color='black'
              ),           
            gridcolor='lightgray'
        ),
        yaxis =dict(
            tickfont=dict(
              size=14,
              family ='Arial',
              color='black'
               ), 
            gridcolor='lightgray'
        ),
        font=dict(
            size=14,
            family ='Arial',
            color='black'
        ),
        legend=dict(
            orientation= 'h',
            yanchor='bottom',
            xanchor='center',
            x=0.5,
            y=1.05,
            bgcolor='rgba(0,0,0,0)',
            borderwidth =0

        ),
        margin=dict(l =60 ,r =60 , t=120, b=60),
        plot_bgcolor ="#faf8fa" ,
        paper_bgcolor='white'
    )
    graph_html= fig.to_html(
        full_html =False ,
        include_plotlyjs='cdn'
    
    )
    return render_template_string('''
         <html>
         <head>
                <title>Correlacão Selic x Inadimplencia </title>
         </head>
         <body> 
          <h1>Correlacão Selic x Inadimplencia</h1>
          <div>{{grafico|safe}}</div>
          <br>
         <a herf="{{voltar}}"> Voltar </a>
         </body>                       
         </html>                               

   ''',grafico = graph_html,voltar =rotas[0])
if __name__ == '__main__':

    init_db()
    app.run (
        debug= config.FLASK_DEBUG,
        host= config.FLASK_HOST,
        port=config.FLASK_PORT

    )
    


