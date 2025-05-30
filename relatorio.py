import sqlite3
from openpyxl import Workbook
from datetime import datetime

def gerar_relatorio(nome_aluno):
    wb = Workbook()
    ws_paises = wb.active
    ws_paises.title = "Países"
    ws_paises.append([f"Relatório gerado por: {nome_aluno}"])
    ws_paises.append([f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}"])
    ws_paises.append([])  
    ws_paises.append([
        'Nome Comum', 'Nome Oficial', 'Capital', 'Continente', 'Região', 
        'Sub-região', 'População', 'Área', 'Moeda (Nome)', 'Moeda (Símbolo)', 
        'Idioma Principal', 'Fuso Horário', 'URL da Bandeira', 'Data de Consulta'
    ])

    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paises")
    for linha in cursor.fetchall():
        ws_paises.append(linha[1:])
    conn.close()
    
    ws_livros = wb.create_sheet("Livros")
    ws_livros.append([f"Relatório gerado por: {nome_aluno}"])
    ws_livros.append([f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}"])
    ws_livros.append([])  
    ws_livros.append([
        'Título', 'Preço', 'Avaliação (Estrelas)', 
        'Disponibilidade', 'Data de Consulta'
    ])
    
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, preco, avaliacao, disponibilidade, data_consulta FROM livros")
    for linha in cursor.fetchall():
        ws_livros.append(linha)
    conn.close()
    
    # Salva
    nome_arquivo = f"Relatório_{datetime.now().strftime('%d%m%Y')}.xlsx"
    wb.save(nome_arquivo)
    print(f"Relatório gerado: {nome_arquivo}")

if __name__ == '__main__':
    nome = input("Seu nome: ").strip()
    gerar_relatorio(nome)