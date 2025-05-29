import sqlite3

def verificar_paises():
    print("\n📌 DADOS DOS PAÍSES (paises.db):")
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    
    # Mostra todos os países cadastrados
    cursor.execute("SELECT nome_comum, capital, populacao FROM paises")
    for linha in cursor.fetchall():
        print(f"→ {linha[0]} | Capital: {linha[1]} | População: {linha[2]:,}")
    
    conn.close()

def verificar_livros():
    print("\n📚 DADOS DOS LIVROS (livraria.db):")
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    # Mostra todos os livros cadastrados
    cursor.execute("SELECT titulo, preco FROM livros LIMIT 5")
    for linha in cursor.fetchall():
        print(f"→ {linha[0]} | Preço: £{linha[1]:.2f}")
    
    conn.close()

if __name__ == '__main__':
    verificar_paises()
    verificar_livros()
    print("\n✅ Verificação concluída!")