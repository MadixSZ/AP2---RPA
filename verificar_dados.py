import sqlite3

def verificar_paises():
    print("\n📌 DADOS DOS PAÍSES (paises.db):")
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome_comum, capital, populacao FROM paises")
    for linha in cursor.fetchall():
        print(f"→ {linha[0]} | Capital: {linha[1]} | População: {linha[2]:,}")
    
    conn.close()

def verificar_livros():
    print("\n📚 DADOS DOS LIVROS (livraria.db):")
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT titulo, preco, avaliacao FROM livros")
    for linha in cursor.fetchall():
        print(f"→ {linha[0]} | Preço: £{linha[1]:.2f} | Avaliação: {linha[2]}")
    
    conn.close()

if __name__ == '__main__':
    verificar_paises()
    verificar_livros()
    print("\n Verificação concluída!")