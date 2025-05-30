import requests
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
from openpyxl import Workbook

def coletar_dados_pais(nome_pais):
    url = f"https://restcountries.com/v3.1/name/{nome_pais}"
    resposta = requests.get(url)

    if resposta.status_code != 200:
        print(f"Erro ao buscar dados de {nome_pais}")
        return None

    dados = resposta.json()[0]

    nome_comum = dados.get('name', {}).get('common', 'N/A')
    nome_oficial = dados.get('name', {}).get('official', 'N/A')
    capital = dados.get('capital', ['N/A'])[0]
    continente = dados.get('continents', ['N/A'])[0]
    regiao = dados.get('region', 'N/A')
    sub_regiao = dados.get('subregion', 'N/A')
    populacao = dados.get('population', 0)
    area = dados.get('area', 0)

    moedas = dados.get('currencies', {})
    if moedas:
        moeda_codigo = list(moedas.keys())[0]
        moeda_info = moedas[moeda_codigo]
        moeda_nome = moeda_info.get('name', 'N/A')
        moeda_simbolo = moeda_info.get('symbol', 'N/A')
    else:
        moeda_nome = 'N/A'
        moeda_simbolo = 'N/A'

    idiomas = dados.get('languages', {})
    idioma_principal = list(idiomas.values())[0] if idiomas else 'N/A'

    fusos = dados.get('timezones', ['N/A'])
    fuso_horario = ', '.join(fusos)

    url_bandeira = dados.get('flags', {}).get('png', 'N/A')

    data_consulta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return (
        nome_comum, nome_oficial, capital, continente, regiao, sub_regiao,
        populacao, area, moeda_nome, moeda_simbolo,
        idioma_principal, fuso_horario, url_bandeira, data_consulta
    )

def criar_tabela_paises():
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS paises')
    cursor.execute('''
        CREATE TABLE paises (
            nome_comum TEXT,
            nome_oficial TEXT,
            capital TEXT,
            continente TEXT,
            regiao TEXT,
            sub_regiao TEXT,
            populacao INTEGER,
            area REAL,
            moeda_nome TEXT,
            moeda_simbolo TEXT,
            idioma_principal TEXT,
            fuso_horario TEXT,
            url_bandeira TEXT,
            data_consulta TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_dados_pais(dados):
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO paises VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    conn.close()

def coletar_livros():
    url = "https://books.toscrape.com/"
    resposta = requests.get(url)
    soup = BeautifulSoup(resposta.text, 'html.parser')

    livros = []
    artigos = soup.select('article.product_pod')[:10]

    for artigo in artigos:
        titulo = artigo.h3.a['title']
        preco = artigo.select_one('.price_color').text
        disponibilidade = artigo.select_one('.availability').text.strip()
        estrelas = artigo.select_one('p.star-rating')['class'][1]
        livros.append((titulo, preco, estrelas, disponibilidade))
    return livros

def criar_tabela_livros():
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS livros')
    cursor.execute('''
        CREATE TABLE livros (
            titulo TEXT,
            preco TEXT,
            avaliacao TEXT,
            disponibilidade TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_livros(livros):
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO livros VALUES (?, ?, ?, ?)
    ''', livros)
    conn.commit()
    conn.close()

def gerar_relatorio_excel(nome_aluno):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Países"
    ws1.append([f"Relatório gerado por: {nome_aluno}"])
    ws1.append([f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}"])
    ws1.append([])

    conn1 = sqlite3.connect('paises.db')
    cursor1 = conn1.cursor()
    cursor1.execute('SELECT * FROM paises')
    ws1.append([
        'Nome Comum', 'Nome Oficial', 'Capital', 'Continente', 'Região', 'Sub-região',
        'População', 'Área', 'Moeda (Nome)', 'Moeda (Símbolo)', 'Idioma Principal',
        'Fuso Horário', 'URL da Bandeira', 'Data de Consulta'
    ])
    for linha in cursor1.fetchall():
        ws1.append(linha)
    conn1.close()

    ws2 = wb.create_sheet("Livros")
    ws2.append([f"Relatório gerado por: {nome_aluno}"])
    ws2.append([f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}"])
    ws2.append([])

    conn2 = sqlite3.connect('livraria.db')
    cursor2 = conn2.cursor()
    cursor2.execute('SELECT * FROM livros')
    ws2.append(['Título', 'Preço', 'Avaliação', 'Disponibilidade'])
    for linha in cursor2.fetchall():
        ws2.append(linha)
    conn2.close()

    wb.save("relatorio_final.xlsx")

def main():
    criar_tabela_paises()
    criar_tabela_livros()

    print("Digite o nome de 3 países:")
    paises = []
    for i in range(3):
        pais = input(f"País {i+1}: ")
        paises.append(pais)

    for nome_pais in paises:
        dados = coletar_dados_pais(nome_pais)
        if dados:
            salvar_dados_pais(dados)

    livros = coletar_livros()
    salvar_livros(livros)

    nome = input("Digite seu nome: ")
    gerar_relatorio_excel(nome)

if __name__ == "__main__":
    main()
