import sqlite3
import requests
from datetime import datetime

def banco_paises():
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS paises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_comum TEXT,
        nome_oficial TEXT,
        capital TEXT,
        continente TEXT,
        regiao TEXT,
        subregiao TEXT,
        populacao INTEGER,
        area REAL,
        moeda_nome TEXT,
        moeda_simbolo TEXT,
        idioma_principal TEXT,
        fuso_horario TEXT,
        url_bandeira TEXT,
        data_consulta TEXT
    )''')
    conn.commit()
    conn.close()

def dados_pais(nome_pais):
    url = f'https://restcountries.com/v3.1/name/{nome_pais}'
    response = requests.get(url)
    
    if response.status_code == 404:
        print(f"País '{nome_pais}' não encontrado.")
        return None
    elif response.status_code != 200:
        print(f"Erro na API: {response.status_code}")
        return None
    
    dados = response.json()[0]
    moeda = list(dados.get('currencies', {}).values())[0] if dados.get('currencies') else {}
    
    return {
        'nome_comum': dados['name']['common'],
        'nome_oficial': dados['name']['official'],
        'capital': ', '.join(dados.get('capital', ['N/A'])),
        'continente': dados.get('continent', 'N/A'),
        'regiao': dados.get('region', 'N/A'),
        'subregiao': dados.get('subregion', 'N/A'),
        'populacao': dados.get('population', 0),
        'area': dados.get('area', 0),
        'moeda_nome': moeda.get('name', 'N/A'),
        'moeda_simbolo': moeda.get('symbol', 'N/A'),
        'idioma_principal': ', '.join(dados.get('languages', {}).values()) if dados.get('languages') else 'N/A',
        'fuso_horario': ', '.join(dados.get('timezones', ['N/A'])),
        'url_bandeira': dados['flags']['png'],
        'data_consulta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def salvar_pais(pais_info):
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO paises (
        nome_comum, nome_oficial, capital, continente, regiao, subregiao,
        populacao, area, moeda_nome, moeda_simbolo, idioma_principal,
        fuso_horario, url_bandeira, data_consulta
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        pais_info['nome_comum'], pais_info['nome_oficial'], pais_info['capital'],
        pais_info['continente'], pais_info['regiao'], pais_info['subregiao'],
        pais_info['populacao'], pais_info['area'], pais_info['moeda_nome'],
        pais_info['moeda_simbolo'], pais_info['idioma_principal'],
        pais_info['fuso_horario'], pais_info['url_bandeira'], pais_info['data_consulta']
    ))
    
    conn.commit()
    conn.close()