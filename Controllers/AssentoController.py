# Controllers/AssentoController.py
import sqlite3
from Models.Assento import Assento
from Services.database_setup import conectaBD
from Controllers.OnibusController import onibus_existe

def incluir_assento(assento):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        if not onibus_existe(assento.get_onibus_id()):
            raise ValueError(f"Ônibus com ID {assento.get_onibus_id()} não existe.")

        cursor.execute("""
            INSERT INTO Assento (onibus_id, Localizacao, Disponibilidade)
            VALUES (?, ?, ?)
        """, (assento.get_onibus_id(), assento.get_localizacao(), assento.get_disponibilidade()))
        conexao.commit()
        return True
    except (sqlite3.Error, ValueError) as e:
        print(f"Erro ao inserir Assento: {e}")
        return False
    finally:
        conexao.close()

def consultar_assentos():
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT a.Id, a.onibus_id, o.motorista, a.Localizacao, a.Disponibilidade 
            FROM Assento a
            JOIN ONIBUS o ON a.onibus_id = o.Id
            ORDER BY a.onibus_id, a.Localizacao
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar Assentos: {e}")
        return []
    finally:
        conexao.close()

def excluir_assento(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM Assento WHERE Id = ?", (id,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao excluir Assento: {e}")
        return False
    finally:
        conexao.close()

# Função para consultar assentos por ônibus (útil para a View de Reserva)
def consultar_assentos_por_onibus(onibus_id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM Assento WHERE onibus_id = ? ORDER BY Localizacao", (onibus_id,))
        return cursor.fetchall()
    finally:
        conexao.close()

# Função para verificar se assento existe
def assento_existe(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT 1 FROM Assento WHERE Id = ?", (id,))
        return cursor.fetchone() is not None
    finally:
        conexao.close()