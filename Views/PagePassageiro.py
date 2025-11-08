# Views/PagePassageiro.py
import streamlit as st
import pandas as pd
from Models.Passageiro import Passageiro
from Controllers.PassageiroController import (
    incluir_passageiro,
    consultar_passageiros,
    excluir_passageiro,
    alterar_passageiro
)

def show_passageiro_page():
    st.title('Cadastro de Passageiros')
    
    operacao = st.sidebar.selectbox("Operações Passageiro", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if operacao == "Incluir":
        st.header("Cadastrar Novo Passageiro")
        with st.form(key="incluir_passageiro_form"):
            nome = st.text_input("Nome do Passageiro:")
            numero = st.number_input("Número (Telefone/Matrícula):", min_value=1, step=1)
            carteirinha = st.text_input("Carteirinha (Opcional):")
            # Nota: A lógica de vincular assento_id foi omitida aqui por simplicidade
            # Idealmente, o assento é vinculado apenas na Reserva.
            
            if st.form_submit_button("Cadastrar Passageiro"):
                passageiro = Passageiro(0, numero, None, carteirinha, nome)
                if incluir_passageiro(passageiro):
                    st.success("Passageiro cadastrado com sucesso!")
                else:
                    st.error("Erro ao cadastrar Passageiro. O 'Número' pode já existir.")

    elif operacao == "Consultar":
        st.header("Lista de Passageiros")
        passageiros = consultar_passageiros()
        if passageiros:
            df = pd.DataFrame(passageiros, columns=["ID", "Número", "Carteirinha", "Nome", "ID Assento Fixo", "Local Assento"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum passageiro cadastrado.")
            
    elif operacao == "Excluir":
        st.header("Excluir Passageiro")
        passageiros = consultar_passageiros()
        if passageiros:
            df = pd.DataFrame(passageiros, columns=["ID", "Número", "Carteirinha", "Nome", "ID Assento Fixo", "Local Assento"])
            st.table(df)
            
            id_excluir = st.number_input("ID do Passageiro a excluir:", min_value=1, step=1)
            if st.button("Excluir"):
                if excluir_passageiro(id_excluir):
                    st.success(f"Passageiro com ID {id_excluir} excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Falha ao excluir. Verifique se o ID existe.")
        else:
            st.info("Nenhum Passageiro para excluir.")
            
    elif operacao == "Alterar":
        st.header("Alterar Passageiro")
        passageiros = consultar_passageiros()
        if passageiros:
            df = pd.DataFrame(passageiros, columns=["ID", "Número", "Carteirinha", "Nome", "ID Assento Fixo", "Local Assento"])
            st.table(df)
            
            with st.form(key="alterar_passageiro_form"):
                id_alterar = st.number_input("ID do Passageiro a alterar:", min_value=1, step=1)
                nome = st.text_input("Novo Nome do Passageiro:")
                numero = st.number_input("Novo Número (Telefone/Matrícula):", min_value=1, step=1)
                carteirinha = st.text_input("Nova Carteirinha (Opcional):")
                
                if st.form_submit_button("Alterar Passageiro"):
                    passageiro = Passageiro(id_alterar, numero, None, carteirinha, nome)
                    if alterar_passageiro(passageiro):
                        st.success(f"Passageiro com ID {id_alterar} alterado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao alterar Passageiro. Verifique se o ID existe.")
        else:
            st.info("Nenhum Passageiro cadastrado para alterar.")