import requests
from bs4 import BeautifulSoup

# URL da página de preços e taxas do Tesouro Direto
url = "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm"

# Fazer a requisição HTTP
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parsear o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontre a tabela de preços e taxas
    tabela = soup.find('table', {'class': 'tabela-titulos'})

    # Verificar se a tabela foi encontrada
    if tabela:
        # Iterar sobre as linhas da tabela
        for linha in tabela.find_all('tr')[1:]:  # Pulando o cabeçalho
            colunas = linha.find_all('td')
            nome_titulo = colunas[0].text.strip()
            vencimento = colunas[1].text.strip()
            taxa_compra = colunas[2].text.strip()
            taxa_venda = colunas[3].text.strip()
            preco_unitario = colunas[4].text.strip()

            print(f'Título: {nome_titulo}')
            print(f'Vencimento: {vencimento}')
            print(f'Taxa Compra: {taxa_compra}')
            print(f'Taxa Venda: {taxa_venda}')
            print(f'Preço Unitário: {preco_unitario}')
            print('-' * 40)
    else:
        print("Tabela de preços e taxas não encontrada.")
else:
    print(f"Erro ao acessar a página: {response.status_code}")