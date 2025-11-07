# Controllers/ReservaController.py
import sqlite3
from Models.Reserva import Reserva
from Services.database_setup import conectaBD
from Controllers.PassageiroController import passageiro_existe
from Controllers.AssentoController import assento_existe

def incluir_reserva(reserva):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        if not passageiro_existe(reserva.get_passageiro_id()):
            raise ValueError("Passageiro não encontrado.")
        if not assento_existe(reserva.get_assento_id()):
            raise ValueError("Assento não encontrado.")

        cursor.execute("""
            INSERT INTO Reserva (passageiro_id, assento_id, Data_viagem, Status)
            VALUES (?, ?, ?, ?)
        """, (
            reserva.get_passageiro_id(), 
            reserva.get_assento_id(),
            reserva.get_data_viagem(),
            reserva.get_status()
        ))
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        # Erro de UNIQUE (assento_id, Data_viagem)
        st.error(f"Erro: O assento {reserva.get_assento_id()} já está reservado para esta data.")
        return False
    except (sqlite3.Error, ValueError) as e:
        print(f"Erro ao inserir Reserva: {e}")
        return False
    finally:
        conexao.close()

def consultar_reservas():
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT 
                r.Id, 
                r.Data_viagem, 
                p.nome as Nome_Passageiro, 
                a.Localizacao as Assento,
                o.Id as ID_Onibus,
                r.Status
            FROM Reserva r
            JOIN PASSAGEIRO p ON r.passageiro_id = p.Id
            JOIN Assento a ON r.assento_id = a.Id
            JOIN ONIBUS o ON a.onibus_id = o.Id
            ORDER BY r.Data_viagem DESC, p.nome
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar Reservas: {e}")
        return []
    finally:
        conexao.close()

def excluir_reserva(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM Reserva WHERE Id = ?", (id,))
        conexao.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao excluir Reserva: {e}")
        return False
    finally:
        conexao.close()