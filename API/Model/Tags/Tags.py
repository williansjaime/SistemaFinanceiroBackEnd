
from flask import jsonify
from flask_restful import Resource

from  API.DB.dbAcess import DBAcess

class Tags(Resource):
    def get(self, id=None):
        conn = DBAcess.db_mysql()
        cursor = conn.cursor(dictionary=True)
        users = []
        if id is not None:
            cursor.execute(f"""
                SELECT 
                    id, 
                    tagName, 
                    IO 
                FROM 
                    DadosSistemaFinancas.tbTagGastos 
                WHERE 
                    IO = {id}
            """)           
        
            users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    