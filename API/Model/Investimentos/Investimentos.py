
from  API.DB.dbAcess import DBAcess
from datetime import datetime
from flask import Flask, request, jsonify,json
from flask_restful import Resource, abort

class Investimentos(Resource):

    def get(self, id=None):
        conn = DBAcess.db_mysql()
        cursor = conn.cursor(dictionary=True)
        if id is not None:
            cursor.execute("""
                SELECT 
                    id, 
                    DATE_FORMAT(dataInvestimento, '%Y-%m-%d') as dataCadastro,
                    (SELECT tagName FROM DadosSistemaFinancas.tbTagGastos WHERE id = tagInvestimento) as tagInvestimento, 
                    valorTotal, 
                    ticket, 
                    descricaoInvestimento, 
                    valorAtual,
                    valorUnitario,
                    Quantidade
                FROM DadosSistemaFinancas.tbInvestimentos
                    order by 
                        id 
                    desc
            """)
        else:
            cursor.execute("""
                SELECT 
                    id, 
                    tagName, 
                    IO 
                FROM 
                    DadosSistemaFinancas.tbTagGastos 
                WHERE 
                    IO = 2
            """)
        
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    
    
    def post(self,id=None):
        try:
            # Directly parse JSON data from the request
            new_user = request.get_json()
            dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if new_user:
                with DBAcess.db_mysql() as mysql:
                    with mysql.cursor() as mysqlCursor:
                        for user in new_user:
                            insert_query = """
                                INSERT INTO DadosSistemaFinancas.tbInvestimentos
                                    (dataInvestimento, tagInvestimento, valorTotal, ticket, descricaoInvestimento, valorAtual,valorUnitario,Quantidade)
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            values = (
                                dateTime,
                                user["tagInvestimento"],
                                user["valorTotal"],
                                user["ticket"],
                                user["descricaoInvestimento"],
                                user["valorAtual"],
                                user["valorUnitario"],
                                user["Quantidade"]
                            )
                            mysqlCursor.execute(insert_query, values)
                        mysql.commit()

            response = {"message": "Dados inseridos com sucesso!"}
            print("Resposta de sucesso: ", response)
            return response, 201  
        
        except Exception as e:
            error_message = {"error": str(e)}
            print("Erro capturado: ", error_message)
            return error_message, 500 
     
    def delete(self,id):
        try:
            with DBAcess.db_mysql() as mysql:
                with mysql.cursor() as mysqlCursor:
                    delete_query = f"""
                        DELETE FROM DadosSistemaFinancas.tbInvestimentos
                        WHERE id={id}
                    """
                    mysqlCursor.execute(delete_query)
                    mysql.commit()

            response = {"message": "Dados deletados com sucesso!"}
            print("Resposta de sucesso: ", response)
            return response, 201  # Retorna o dicionário diretamente
        
        except Exception as e:
            error_message = {"error": str(e)}
            print("Erro capturado: ", error_message)
            return error_message, 500  # Retorna o dicionário de erro diretamente


