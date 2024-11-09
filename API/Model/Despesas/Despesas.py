
from datetime import datetime
from flask import Flask, request, jsonify,json
from flask_restful import Resource, abort

from  API.DB.dbAcess import DBAcess

class Despesas(Resource):

    def get(self, id=None):
        conn = DBAcess.db_mysql()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT 
                id,
                DATE_FORMAT(dateTime, '%Y-%m-%d') as dataCadastro,
                descricao as descricaoGasto,
                Parcelas as parcelas,
                (SELECT tagName FROM DadosSistemaFinancas.tbTagGastos WHERE id = tagGastos) as tipogasto,
                valor,
                quantidade,
                notaFiscal 
            FROM 
                DadosSistemaFinancas.tbGastosFinanceiros            
        """
        # Se um ID for fornecido, adicionar a condição WHERE para o ID
        if id is not None and int(id) !=0:
            sql += f"""WHERE 
                MONTH(dateTime) = {id} 
                AND YEAR(dateTime) = YEAR(CURRENT_DATE()) 
                ORDER BY dataCadastro DESC"""
            
        elif id is not None and int(id) ==0:
            sql += "ORDER BY dataCadastro DESC"
            
        else:
            sql += """WHERE 
                MONTH(dateTime) = MONTH(CURRENT_DATE()) 
                AND YEAR(dateTime) = YEAR(CURRENT_DATE()) 
                ORDER BY dataCadastro DESC"""
        cursor.execute(sql)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)    
    
    def post(self,id=None):
        try:
            new_user = request.get_json()
            dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if new_user:
                with DBAcess.db_mysql() as mysql:
                    with mysql.cursor() as mysqlCursor:
                        for user in new_user:
                            insert_query = """
                                INSERT INTO DadosSistemaFinancas.tbGastosFinanceiros 
                                    (`dateTime`, descricao, Parcelas, tagGastos, valor, quantidade,notaFiscal)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """
                            values = (
                                user["dataCadastro"] if user["dataCadastro"] != "" else dateTime,
                                user["descricaoGasto"],
                                user["parcelas"],
                                user["tipogasto"],
                                user["valor"],
                                user["quantidade"] if user["quantidade"] != "" else 0,
                                user["notaFiscal"]
                            )
                            mysqlCursor.execute(insert_query, values)
                        mysql.commit()

            response = {"message": "Dados inseridos com sucesso!"}
            return response, 201 
        
        except Exception as e:
            error_message = {"error": str(e)}
            # print("Erro capturado: ", error_message)
            return error_message, 500  
     
    def delete(self,id):
        try:
            with DBAcess.db_mysql() as mysql:
                with mysql.cursor() as mysqlCursor:
                    delete_query = f"""
                        DELETE FROM DadosSistemaFinancas.tbGastosFinanceiros
                        WHERE id={id}
                    """
                    mysqlCursor.execute(delete_query)
                    mysql.commit()

            response = {"message": "Dados deletados com sucesso!"}
            return response, 201  
        
        except Exception as e:
            error_message = {"error": str(e)}
            return error_message, 500 

