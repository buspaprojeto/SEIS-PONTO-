# Controllers/PassageiroController.py
import sqlite3
from Models.Passageiro import Passageiro
from Services.database_setup import conectaBD
from Controllers.AssentoController import assento_existe

def incluir_passageiro(passageiro):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Permite assento_id ser Nulo (None)
        assento_id = passageiro.get_assento_id()
        if assento_id is not None and not assento_existe(assento_id):
            raise ValueError(f"Assento com ID {assento_id} não existe.")

        cursor.execute("""
            INSERT INTO PASSAGEIRO (numero, assento_id, Carteirinha, nome)
            VALUES (?, ?, ?, ?)
        """, (
            passageiro.get_numero(), 
            assento_id, 
            passageiro.get_carteirinha(), 
            passageiro.get_nome()
        ))
        conexao.commit()
        return True
    except (sqlite3.Error, ValueError) as e:
        print(f"Erro ao inserir Passageiro: {e}")
        return False
    finally:
        conexao.close()

def consultar_passageiros():
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT p.Id, p.numero, p.Carteirinha, p.nome, p.assento_id, a.Localizacao 
            FROM PASSAGEIRO p
            LEFT JOIN Assento a ON p.assento_id = a.Id
            ORDER BY p.nome
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar Passageiros: {e}")
        return []
    finally:
        conexao.close()

def passageiro_existe(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT 1 FROM PASSAGEIRO WHERE Id = ?", (id,))
        return cursor.fetchone() is not None
    finally:
        conexao.close()

def excluir_passageiro(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM PASSAGEIRO WHERE Id = ?", (id,))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao excluir Passageiro: {e}")
        return False
    finally:
        conexao.close()

def alterar_passageiro(passageiro):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Permite assento_id ser Nulo (None)
        assento_id = passageiro.get_assento_id()
        if assento_id is not None and not assento_existe(assento_id):
            raise ValueError(f"Assento com ID {assento_id} não existe.")

        cursor.execute("""
            UPDATE PASSAGEIRO 
            SET numero = ?, assento_id = ?, Carteirinha = ?, nome = ?
            WHERE Id = ?
        """, (
            passageiro.get_numero(),
            assento_id,
            passageiro.get_carteirinha(),
            passageiro.get_nome(),
            passageiro.get_id()
        ))
        conexao.commit()
        return cursor.rowcount > 0
    except (sqlite3.Error, ValueError) as e:
        print(f"Erro ao alterar Passageiro: {e}")
        return False
    finally:
        conexao.close()