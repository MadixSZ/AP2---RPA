import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

def gerar_relatorio(nome_aluno):
    wb = Workbook()
    
    # ===== PAÍSES =====
    ws_paises = wb.active
    ws_paises.title = "Países"
    
    # Cabeçalho Original do Enunciado
    ws_paises.append([
        'Nome Comum', 
        'Nome Oficial', 
        'Capital', 
        'Continente', 
        'Região', 
        'Sub-região', 
        'População', 
        'Área', 
        'Moeda (Nome)', 
        'Moeda (Símbolo)', 
        'Idioma Principal', 
        'Fuso Horário', 
        'URL da Bandeira', 
        'Data de Consulta'
    ])
    
    # Buscar dados
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paises")
    for linha in cursor.fetchall():
        # Ajuste para garantir a ordem correta
        ws_paises.append([
            linha[1],  # nome_comum
            linha[2],  # nome_oficial
            linha[3],  # capital
            linha[4],  # continente
            linha[5],  # regiao
            linha[6],  # subregiao
            linha[7],  # populacao
            linha[8],  # area
            linha[9],  # moeda_nome
            linha[10], # moeda_simbolo
            linha[11], # idioma_principal
            linha[12], # fuso_horario
            linha[13], # url_bandeira
            linha[14]  # data_consulta
        ])
    conn.close()
    
    # ===== LIVROS =====
    ws_livros = wb.create_sheet("Livros")
    ws_livros.append([
        'Título', 
        'Preço', 
        'Avaliação (Estrelas)', 
        'Disponibilidade', 
        'Data de Consulta'
    ])
    
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    for linha in cursor.fetchall():
        avaliacao = linha[3].replace('One', '★').replace('Two', '★★').replace('Three', '★★★')
        ws_livros.append([linha[1], linha[2], avaliacao, linha[4], linha[5]])
    conn.close()
    
    # Formatação Profissional
    for sheet in wb:
        for cell in sheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="4F81BD")
            cell.alignment = Alignment(horizontal='center')
        
        for col in sheet.columns:
            max_length = max(len(str(cell.value)) for cell in col)
            sheet.column_dimensions[col[0].column_letter].width = max_length + 2
    
    # Salvar
    nome_arquivo = f"Relatório_Completo_{datetime.now().strftime('%d%m%Y')}.xlsx"
    wb.save(nome_arquivo)
    print(f"✅ Relatório gerado: {nome_arquivo}")

if __name__ == '__main__':
    nome = input("Seu nome: ").strip()
    gerar_relatorio(nome)