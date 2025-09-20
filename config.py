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

# Configurações comuns dos sistema:
FOLDER = 'C:/Users/sabado/Desktop/Aline/AIS/'
DB_PATH = "bancoDeDadosAIS.db"
FLASK_DEBUG = True
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000

# Rotas comuns do sistema
ROTAS = [
    '/',                    # rota 00
    '/upload',              # rota 01
    '/consultar',           # rota 02
    '/graficos',            # rota 03
    '/editar_inadimplencia',# rota 04
    '/correlacao'           # rota 05
]
