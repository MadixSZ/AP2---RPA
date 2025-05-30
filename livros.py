import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def banco_livros():
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        preco REAL,
        avaliacao TEXT,
        disponibilidade TEXT,
        data_consulta TEXT
    )''')
    conn.commit()
    conn.close()

def extrair_livros():
    url = 'https://books.toscrape.com/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Erro ao acessar o site.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    livros = soup.find_all('article', class_='product_pod')[:10]
    
    dados = []
    rating_map = {
        'One': '★',
        'Two': '★★',
        'Three': '★★★',
        'Four': '★★★★',
        'Five': '★★★★★'
    }
    
    for livro in livros:
        rating_class = livro.find('p')['class'][1]
        avaliacao = rating_map.get(rating_class, rating_class)
        
        dados.append({
            'titulo': livro.h3.a['title'],
            'preco': float(livro.find('p', class_='price_color').text.replace('Â£', '').replace('£', '')),
            'avaliacao': avaliacao,
            'disponibilidade': livro.find('p', class_='instock availability').text.strip(),
            'data_consulta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return dados

def salvar_livros(livros):
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    for livro in livros:
        cursor.execute('''
        INSERT INTO livros (titulo, preco, avaliacao, disponibilidade, data_consulta)
        VALUES (?, ?, ?, ?, ?)
        ''', (livro['titulo'], livro['preco'], livro['avaliacao'], livro['disponibilidade'], livro['data_consulta']))
    conn.commit()
    conn.close()

def coleta_livros():
    conn = sqlite3.connect('livraria.db')
    conn.execute("DELETE FROM livros")
    conn.commit()
    conn.close()
    
    # Coletar novos
    livros = extrair_livros()
    if livros:
        salvar_livros(livros)
        print(f" {len(livros)} livros salvos!")
    else:
        print("Nenhum livro encontrado.")

if __name__ == '__main__':
    coleta_livros()