# Montagem da API para fazer conexão entre o banco de dados e o Sistema Financeiro

import logging
import traceback
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from API.Model.Tags.Tags import Tags
from API.Model.Despesas.Despesas import Despesas
from API.Model.Receitas.Receitas import Receitas
from API.Model.Processos.Processos import Processos
from API.Model.Investimentos.Investimentos import Investimentos


app = Flask(__name__) 
api = Api(app)


CORS(app, resources={r"/api/*": {"Access-Control-Allow-Origin": "*"}})
logging.getLogger("flask_cors").level = logging.DEBUG


# Adicionar as rotas de API
api.add_resource(Tags,"/api/v1/tags/<id>")
api.add_resource(Processos,"/api/v1/processos")
api.add_resource(Despesas,"/api/v1/despesas","/api/v1/despesas/<id>")
api.add_resource(Receitas,"/api/v1/receitas","/api/v1/receitas/<id>")
api.add_resource(Investimentos,"/api/v1/investimentos","/api/v1/investimentos/<id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 




