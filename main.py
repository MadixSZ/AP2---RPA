from app import coleta_paises
from livros import coleta_livros
from relatorio import gerar_relatorio
import sqlite3

def verificar_dados():
    print("\n🔍 Verificação rápida:")
    
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM paises")
    print(f"- Países: {cursor.fetchone()[0]}")
    conn.close()
    
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM livros")
    print(f"- Livros: {cursor.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    coleta_paises()
    coleta_livros()
    verificar_dados()
    nome = input("\nSeu nome para o relatório: ").strip()
    gerar_relatorio(nome)