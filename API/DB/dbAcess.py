import mysql.connector
import env

class DBAcess():
    '''
        Acessar o banco de dados
    '''
    def db_mysql():
        Mysql = None
        try:
            hosts = env.hosts  
            porta= env.porta  
            username= env.username  
            password= env.password  
            database= env.database  
            Mysql = mysql.connector.connect(
                host=hosts,
                user=username,
                password=password,
                database=database,
                port=porta)
            return Mysql        
        except Exception as err:
            print(err)

    def db_LogErro(Erro):
        with DBAcess.db_mysql() as SQLServe:
            with SQLServe.cursor() as sqlserver:
                insertErroAPI = f"""
                    INSERT INTO logapi
                        (erro)
                        VALUES(%s)
                """
                sqlserver.execute(insertErroAPI, (Erro,))
                SQLServe.commit()            
            SQLServe.close()