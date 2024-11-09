import env
import requests
from API.DB.dbAcess import DBAcess


def ticke_acoes():
    conn = DBAcess.db_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, ticket FROM DadosSistemaFinancas.tbInvestimentos ORDER BY id DESC
    """)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users  # Returning list of dictionaries with 'id' and 'ticket'

def update_valor_atual(investment_id, valor_atual):
    conn = DBAcess.db_mysql()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE DadosSistemaFinancas.tbInvestimentos
        SET valorAtual = %s
        WHERE id = %s
    """, (valor_atual, investment_id))
    conn.commit()
    cursor.close()
    conn.close()

def pegar_valores():
    for user in ticke_acoes():
        ticket = user['ticket']
        investment_id = user['id']
        
        url = f"https://brapi.dev/api/quote/{ticket}"

        # Cabeçalhos com o token de autenticação
        headers = {
            "Authorization": f"Bearer {env.token_api_financeira}"
        }

        # Fazendo a requisição GET
        response = requests.get(url, headers=headers)

        # Verificando o status da resposta e atualizando o valor no banco de dados
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and data['results']:
                valor_atual = data['results'][0]['regularMarketPrice']  # Obtendo o preço atual
                print(f"Atualizando ID {investment_id} com valor: {valor_atual}")
                update_valor_atual(investment_id, valor_atual)
            else:
                print(f"Erro ao obter dados para {ticket}: Nenhum resultado encontrado.")
        else:
            print(f"Erro: {response.status_code}")

if __name__ == "__main__":
    pegar_valores()

