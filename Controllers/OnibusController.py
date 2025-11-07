# Controllers/OnibusController.py
import sqlite3
from Models.Onibus import Onibus
from Controllers.CoordenadorController import conectaBD, coordenador_existe

def incluir_onibus(onibus):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        id_coordenador = onibus.get_id_coordenador()
        if id_coordenador is not None and not coordenador_existe(id_coordenador):
            raise ValueError(f"Coordenador com Id {id_coordenador} não existe.")
            
        cursor.execute("""
            INSERT INTO ONIBUS (Id, motorista, id_coordenador)
            VALUES (?, ?, ?)
        """, (onibus.get_id(), onibus.get_motorista(), id_coordenador))
        conexao.commit()
        return True
    except (sqlite3.Error, ValueError) as e:
        print(f"Erro ao inserir Ônibus: {e}")
        return False
    finally:
        conexao.close()

def consultar_onibus():
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Consulta com JOIN para obter o nome do Coordenador (similar ao VendaController)
        cursor.execute("""
            SELECT 
                o.Id, 
                o.motorista, 
                o.id_coordenador, 
                c.nome 
            FROM ONIBUS o
            LEFT JOIN Coordenador c ON o.id_coordenador = c.Id
        """)
        
        results = []
        for row in cursor.fetchall():
            onibus_id, motorista, id_coordenador, nome_coordenador = row
            results.append({
                "Id": onibus_id,
                "Motorista": motorista,
                "Id Coordenador": id_coordenador,
                "Coordenador": nome_coordenador if nome_coordenador else "N/A"
            })
        return results
    except sqlite3.Error as e:
        print(f"Erro ao consultar Ônibus: {e}")
        return []
    finally:
        conexao.close()

def excluir_onibus(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM ONIBUS WHERE Id = ?", (id,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao excluir Ônibus: {e}")
        return False
    finally:
        conexao.close()

def alterar_onibus(onibus):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        id_coordenador = onibus.get_id_coordenador()
        if id_coordenador is not None and not coordenador_existe(id_coordenador):
            raise ValueError(f"Coordenador com Id {id_coordenador} não existe.")

        cursor.execute("""
            UPDATE ONIBUS 
            SET motorista = ?, id_coordenador = ?
            WHERE Id = ?
        """, (onibus.get_motorista(), id_coordenador, onibus.get_id()))
        conexao.commit()
        return cursor.rowcount > 0
    except (sqlite3.Error, ValueError) as e:
        print(f"Erro ao alterar Ônibus: {e}")
        return False
    finally:
        conexao.close()

def onibus_existe(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT 1 FROM ONIBUS WHERE Id = ?", (id,))
        return cursor.fetchone() is not None
    finally:
        conexao.close()