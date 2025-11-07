# Controllers/CoordenadorController.py
import sqlite3
from Models.Coordenador import Coordenador
from Services.database_setup import conectaBD, DATABASE_NAME

def incluir_coordenador(coordenador):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO Coordenador (Id, nome, Numero)
            VALUES (?, ?, ?)
        """, (coordenador.get_id(), coordenador.get_nome(), coordenador.get_numero()))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao inserir Coordenador: {e}")
        return False
    finally:
        conexao.close()

def consultar_coordenadores():
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM Coordenador")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar Coordenadores: {e}")
        return []
    finally:
        conexao.close()

def excluir_coordenador(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM Coordenador WHERE Id = ?", (id,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao excluir Coordenador: {e}")
        return False
    finally:
        conexao.close()

def alterar_coordenador(coordenador):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE Coordenador 
            SET nome = ?, Numero = ?
            WHERE Id = ?
        """, (coordenador.get_nome(), coordenador.get_numero(), coordenador.get_id()))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao alterar Coordenador: {e}")
        return False
    finally:
        conexao.close()

def coordenador_existe(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT 1 FROM Coordenador WHERE Id = ?", (id,))
        return cursor.fetchone() is not None
    finally:
        conexao.close()