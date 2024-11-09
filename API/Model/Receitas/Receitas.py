
from datetime import datetime
from flask import Flask, request, jsonify,json
from flask_restful import Resource, abort

from  API.DB.dbAcess import DBAcess

class Receitas(Resource):

    def get(self, id=None):
        conn = DBAcess.db_mysql()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT 
                id, 
                valor, 
                descricao as descricaoGanho,                     
                DATE_FORMAT(dataCadastro, '%Y-%m-%d') as dataCadastro,
                (SELECT tagName FROM DadosSistemaFinancas.tbTagGastos WHERE id = tipoGanhos) as tipoGanho
            FROM DadosSistemaFinancas.tbGanhosFinanceiros         
        """

        if id is not None and int(id) !=0:
            sql += f"""WHERE 
                MONTH(dataCadastro) = {id} 
                AND YEAR(dataCadastro) = YEAR(CURRENT_DATE()) 
                ORDER BY dataCadastro DESC"""
            
        elif id is not None and int(id) ==0:
            sql += "ORDER BY dataCadastro DESC"      

        else:
            sql += """WHERE 
                MONTH(dataCadastro) = MONTH(CURRENT_DATE()) 
                AND YEAR(dataCadastro) = YEAR(CURRENT_DATE()) 
                ORDER BY dataCadastro DESC"""
                       
        cursor.execute(sql)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    
    
    def post(self,id=None):
        try:
            new_user = request.get_json()
            dateTime = datetime.now().strftime('%Y-%m-%d')

            if new_user:
                with DBAcess.db_mysql() as mysql:
                    with mysql.cursor() as mysqlCursor:
                        for user in new_user:
                            insert_query = """
                                INSERT INTO DadosSistemaFinancas.tbGanhosFinanceiros
                                    (valor, descricao, dataCadastro, tipoGanhos)
                                VALUES(%s, %s, %s, %s)
                            """
                            values = (
                                user["valor"],
                                user["descricaoGanho"],
                                user["dataCadastro"] if user["dataCadastro"] != "" else dateTime,
                                user["tipoGanho"]
                            )
                            mysqlCursor.execute(insert_query, values)
                        mysql.commit()

            response = {"message": "Dados inseridos com sucesso!"}
            return response, 201 
        
        except Exception as e:
            error_message = {"error": str(e)}
            return error_message, 500 
     
    def delete(self,id):
        try:
            with DBAcess.db_mysql() as mysql:
                with mysql.cursor() as mysqlCursor:
                    delete_query = f"""
                        DELETE FROM DadosSistemaFinancas.tbGanhosFinanceiros
                        WHERE id={id}
                    """
                    mysqlCursor.execute(delete_query)
                    mysql.commit()

            response = {"message": "Dados deletados com sucesso!"}
            return response, 201  # Retorna o dicionário diretamente
        
        except Exception as e:
            error_message = {"error": str(e)}
            return error_message, 500  # Retorna o dicionário de erro diretamente

