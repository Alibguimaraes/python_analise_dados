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
def upoload():
    inad_file=request.files.get('campo_inadiplencia')
    selic_file =request.files.get('campo_selic')
    
    if not inad_file or not selic_file:
        return jsonify({"Erro":" Ambos arquivos deve ser envidados" }),406
    

    inad_df = pd.read_cvs(
        inad_file,
        sep =';',
        nomes =['data','inadimplencia '],
        header = 0
    )

   
    selic_df = pd.read_cvs(
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
    
    inad_df['mes'] = inad_df['data'].df.to_period ('M').astype(str).drop_duplicates()
    selic_df['mes'] = selic_df['data'].df.to_period ('M').astype(str)

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
              <input type ="subimt" value="Consultar">
        </form>
        <br>
        <a href ="{rotas[0]}"> Voltar </a>                          
                             
    
''')


if __name__ == '__ main__':
    init_db()
    app.run (
        debug= config.FLASK_DEBUG,
        host= config.FLASK_HOST,
        port=config.FLASK_PORT

    )
    


