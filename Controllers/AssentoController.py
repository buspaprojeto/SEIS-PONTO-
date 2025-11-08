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

        # Verifica se já existe um assento com esta localização neste ônibus
        cursor.execute("""
            SELECT Id FROM Assento 
            WHERE onibus_id = ? AND Localizacao = ?
        """, (assento.get_onibus_id(), assento.get_localizacao()))
        
        existing_assento = cursor.fetchone()
        if existing_assento:
            # Se existe, retorna o ID do assento existente
            return existing_assento[0]
            
        # Se não existe, cria um novo
        cursor.execute("""
            INSERT INTO Assento (onibus_id, Localizacao, Disponibilidade)
            VALUES (?, ?, ?)
        """, (assento.get_onibus_id(), assento.get_localizacao(), assento.get_disponibilidade()))
        conexao.commit()
        
        # Retorna o ID do assento recém-criado
        return cursor.lastrowid
    except (sqlite3.Error, ValueError) as e:
        print(f"Erro ao inserir Assento: {e}")
        return None
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

# Função para verificar se assento existe e retornar suas informações
def assento_existe(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT 1 FROM Assento WHERE Id = ?", (id,))
        return cursor.fetchone() is not None
    finally:
        conexao.close()

def get_passageiro_do_assento(onibus_id, localizacao):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT p.nome, p.Id, a.Id as assento_id
            FROM Assento a
            LEFT JOIN Passageiro p ON p.assento_id = a.Id
            WHERE a.onibus_id = ? AND a.Localizacao = ?
        """, (onibus_id, localizacao))
        resultado = cursor.fetchone()
        if resultado:
            # Se o assento existe mas não tem passageiro, retorna None
            if resultado[0] is None:
                return None
            return resultado
        return None
    except sqlite3.Error as e:
        print(f"Erro ao consultar passageiro do assento: {e}")
        return None
    finally:
        conexao.close()

def vincular_passageiro_assento(assento_id, passageiro_id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Primeiro, verifica se o passageiro já está vinculado a outro assento
        cursor.execute("""
            UPDATE Passageiro 
            SET assento_id = ?
            WHERE Id = ?
        """, (assento_id, passageiro_id))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao vincular passageiro ao assento: {e}")
        return False
    finally:
        conexao.close()

def alterar_assento(assento):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        if not onibus_existe(assento.get_onibus_id()):
            raise ValueError(f"Ônibus com ID {assento.get_onibus_id()} não existe.")

        cursor.execute("""
            UPDATE Assento 
            SET onibus_id = ?, Localizacao = ?, Disponibilidade = ?
            WHERE Id = ?
        """, (
            assento.get_onibus_id(),
            assento.get_localizacao(),
            assento.get_disponibilidade(),
            assento.get_id()
        ))
        conexao.commit()
        return cursor.rowcount > 0
    except (sqlite3.Error, ValueError) as e:
        print(f"Erro ao alterar Assento: {e}")
        return False
    finally:
        conexao.close()