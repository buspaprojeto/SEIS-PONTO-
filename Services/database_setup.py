# Services/database_setup.py
import sqlite3

DATABASE_NAME = "Transporte.db"

def conectaBD():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DATABASE_NAME)

def criar_tabelas():
    """Cria todas as tabelas do esquema."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Tabela Coordenador
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Coordenador (
                Id INTEGER PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                Numero INT
            );
        """)

        # Tabela ONIBUS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ONIBUS (
                Id INTEGER PRIMARY KEY,
                motorista VARCHAR(255) NOT NULL,
                id_coordenador INT,
                FOREIGN KEY (id_coordenador) REFERENCES Coordenador(Id) ON DELETE SET NULL
            );
        """)

        # Tabela Assento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Assento (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                onibus_id INT NOT NULL,
                Localizacao VARCHAR(50) NOT NULL,
                Disponibilidade BOOLEAN NOT NULL DEFAULT TRUE,
                FOREIGN KEY (onibus_id) REFERENCES ONIBUS(Id) ON DELETE CASCADE
            );
        """)

        # Tabela PASSAGEIRO
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PASSAGEIRO (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INT UNIQUE NOT NULL,
                assento_id INT,
                Carteirinha VARCHAR(100),
                nome VARCHAR(255) NOT NULL,
                FOREIGN KEY (assento_id) REFERENCES Assento(Id) ON DELETE SET NULL
            );
        """)
        
        # Tabela Reserva (com constraint UNIQUE em assento_id e Data_viagem)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Reserva (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                passageiro_id INT NOT NULL,
                assento_id INT NOT NULL,
                Data_viagem TEXT NOT NULL,
                Status BOOLEAN NOT NULL DEFAULT FALSE,
                FOREIGN KEY (passageiro_id) REFERENCES PASSAGEIRO(Id) ON DELETE CASCADE,
                FOREIGN KEY (assento_id) REFERENCES Assento(Id) ON DELETE CASCADE,
                UNIQUE (assento_id, Data_viagem)
            );
        """)

        conexao.commit()
        # print("Todas as tabelas criadas com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conexao.close()

if __name__ == "__main__":
    criar_tabelas()