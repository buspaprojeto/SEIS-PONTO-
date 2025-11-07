# Views/PagePassageiro.py
import streamlit as st
import pandas as pd
from Models.Passageiro import Passageiro
from Controllers.PassageiroController import incluir_passageiro, consultar_passageiros
from Views.utils import set_background

def show_passageiro_page():
    set_background('assets/passageiro.jpg')
    st.title('Cadastro de Passageiros')
    
    operacao = st.sidebar.selectbox("Operações Passageiro", ["Incluir", "Consultar"])

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