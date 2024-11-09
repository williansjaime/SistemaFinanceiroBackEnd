from API.DB.dbAcess import DBAcess
from datetime import datetime
from flask import Flask, request, jsonify
from flask_restful import Resource

class Processos(Resource):
    def post(self):
        try:
            # Recebe os dados JSON da requisição
            processos = request.get_json()

            if not processos:
                return {"message": "Nenhum dado recebido."}, 400

            with DBAcess.db_mysql_database("ProcessosLudymila") as mysql:
                with mysql.cursor() as mysqlCursor:
                    for processo in processos:
                        numeroProcesso = processo.get("numeroProcesso")
                        estado = processo.get("estado")

                        # Verifica se os campos obrigatórios estão presentes
                        if not numeroProcesso or not estado:
                            return {"message": "Campos 'numeroProcesso' e 'estado' são obrigatórios."}, 400

                        # Define a URL com base no estado
                        url = ""
                        if estado == "GO":
                            url = "https://projudi.tjgo.jus.br/BuscaProcesso?PaginaAtual=4&TipoConsultaProcesso=24"
                        elif estado == "MT":
                            url = "https://hellsgate.tjmt.jus.br"
                        elif estado == "SP":
                            url = "https://esaj.tjsp.jus.br"
                        elif estado == "MG":
                            url = "https://dje.tjmg.jus.br/diarioJudiciarioData.do"
                        elif estado == "RS":
                            url = "https://www.tjrs.jus.br/novo/busca/?return=proc&client=wp_index"
                        else:
                            return {"message": f"Estado '{estado}' não é suportado."}, 400

                        dataSolicitacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Query para inserir os dados
                        insert_query = """
                            INSERT INTO ProcessosLudymila.tbnumeroprocessos (
                                numeroProcesso, 
                                Estado, 
                                urlSite, 
                                dataHoraCadastro, 
                                status
                            ) VALUES (%s, %s, %s, %s, 0)
                        """
                        values = (numeroProcesso, estado, url, dataSolicitacao)
                        mysqlCursor.execute(insert_query,values)

                mysql.commit()

            return {"message": "Processos inseridos com sucesso!"}, 201
        
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500
