# Views/PageCoordenador.py
import streamlit as st
import pandas as pd
from Models.Coordenador import Coordenador
from Controllers.CoordenadorController import (
    incluir_coordenador, 
    consultar_coordenadores, 
    excluir_coordenador, 
    alterar_coordenador
)

def show_coordenador_page():
    
    st.title('Cadastro de Coordenadores')
    
    operacao = st.sidebar.selectbox("Operações Coordenador", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if operacao == "Incluir":
        st.header("Incluir Novo Coordenador")
        with st.form(key="incluir_coordenador_form"):
            coordenador = Coordenador(0, "", 0)
            
            # Nota: Em sistemas reais, o Id seria AUTOINCREMENT. Aqui, usamos o input.
            coordenador.set_id(st.number_input("ID do Coordenador:", min_value=1, step=1))
            coordenador.set_nome(st.text_input("Nome do Coordenador:"))
            coordenador.set_numero(st.number_input("Número de Contato:", min_value=0))
            
            if st.form_submit_button("Cadastrar Coordenador"):
                try:
                    if incluir_coordenador(coordenador):
                        st.success(f"Coordenador {coordenador.get_nome()} cadastrado com sucesso!")
                    else:
                        st.error("Erro ao cadastrar Coordenador. O ID pode já existir ou o campo Nome está vazio.")
                except Exception as e:
                    st.error(f"Erro: {e}")

    elif operacao == "Consultar":
        st.header("Lista de Coordenadores")
        if st.button("Consultar Coordenadores"):
            coordenadores = consultar_coordenadores()
            if coordenadores:
                df = pd.DataFrame(coordenadores, columns=["Id", "Nome", "Número"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhum Coordenador cadastrado.")

    elif operacao == "Excluir":
        st.header("Excluir Coordenador")
        coordenadores = consultar_coordenadores()
        if coordenadores:
            df = pd.DataFrame(coordenadores, columns=["Id", "Nome", "Número"])
            st.table(df)

            id_excluir = st.number_input("ID do Coordenador a excluir:", min_value=1, step=1)
            if st.button("Excluir"):
                if excluir_coordenador(id_excluir):
                    st.success(f"Coordenador com ID {id_excluir} excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Falha ao excluir. Verifique se o ID existe ou se está vinculado a algum Ônibus.")
        else:
            st.info("Nenhum Coordenador para excluir.")
            
    elif operacao == "Alterar":
        st.header("Alterar Coordenador")
        
        # Mostrar coordenadores existentes
        coordenadores = consultar_coordenadores()
        if coordenadores:
            df = pd.DataFrame(coordenadores, columns=["Id", "Nome", "Número"])
            st.table(df)
            
            with st.form(key="alterar_coordenador_form"):
                coordenador = Coordenador(0, "", 0)
                
                coordenador.set_id(st.number_input("ID do Coordenador a alterar:", min_value=1, step=1))
                coordenador.set_nome(st.text_input("Novo Nome do Coordenador:"))
                coordenador.set_numero(st.number_input("Novo Número de Contato:", min_value=0))
                
                if st.form_submit_button("Alterar Coordenador"):
                    try:
                        if alterar_coordenador(coordenador):
                            st.success(f"Coordenador com ID {coordenador.get_id()} alterado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao alterar Coordenador. Verifique se o ID existe e se os campos estão preenchidos corretamente.")
                    except Exception as e:
                        st.error(f"Erro: {e}")
        else:
            st.info("Nenhum Coordenador cadastrado para alterar.")