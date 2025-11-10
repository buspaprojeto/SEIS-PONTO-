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
from Views.theme import create_header, create_section_title, create_info_box

def show_coordenador_page():
    
    create_header('👨‍💼 Gestão de Coordenadores', 'Gerencie todos os coordenadores do sistema')
    
    operacao = st.sidebar.selectbox("📋 Operações", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if operacao == "Incluir":
        create_section_title("Incluir Novo Coordenador", "➕")
        with st.form(key="incluir_coordenador_form"):
            coordenador = Coordenador(0, "", 0)
            
            coordenador.set_id(st.number_input("ID do Coordenador:", min_value=1, step=1))
            coordenador.set_nome(st.text_input("Nome do Coordenador:"))
            coordenador.set_numero(st.number_input("Número de Contato:", min_value=0))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Cadastrar Coordenador", use_container_width=True):
                    try:
                        if incluir_coordenador(coordenador):
                            st.success(f"✅ Coordenador {coordenador.get_nome()} cadastrado com sucesso!")
                        else:
                            st.error("❌ Erro ao cadastrar. O ID pode já existir ou o campo Nome está vazio.")
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")

    elif operacao == "Consultar":
        create_section_title("Lista de Coordenadores", "📊")
        if st.button("🔍 Consultar Coordenadores", use_container_width=True):
            coordenadores = consultar_coordenadores()
            if coordenadores:
                df = pd.DataFrame(coordenadores, columns=["ID", "Nome", "Número"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                create_info_box("Nenhum coordenador cadastrado no sistema.", "info")

    elif operacao == "Excluir":
        create_section_title("Excluir Coordenador", "🗑️")
        coordenadores = consultar_coordenadores()
        if coordenadores:
            df = pd.DataFrame(coordenadores, columns=["ID", "Nome", "Número"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            col1, col2 = st.columns([3, 1])
            with col1:
                id_excluir = st.number_input("ID do Coordenador a excluir:", min_value=1, step=1)
            with col2:
                if st.button("🗑️ Excluir", use_container_width=True):
                    if excluir_coordenador(id_excluir):
                        st.success(f"✅ Coordenador {id_excluir} excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Falha ao excluir. Verifique se o ID existe ou se está vinculado a algum Ônibus.")
        else:
            create_info_box("Nenhum coordenador para excluir.", "warning")
            
    elif operacao == "Alterar":
        create_section_title("Alterar Coordenador", "✏️")
        
        coordenadores = consultar_coordenadores()
        if coordenadores:
            df = pd.DataFrame(coordenadores, columns=["ID", "Nome", "Número"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            with st.form(key="alterar_coordenador_form"):
                coordenador = Coordenador(0, "", 0)
                
                coordenador.set_id(st.number_input("ID do Coordenador a alterar:", min_value=1, step=1))
                coordenador.set_nome(st.text_input("Novo Nome do Coordenador:"))
                coordenador.set_numero(st.number_input("Novo Número de Contato:", min_value=0))
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Alterar Coordenador", use_container_width=True):
                        try:
                            if alterar_coordenador(coordenador):
                                st.success(f"✅ Coordenador {coordenador.get_id()} alterado com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao alterar. Verifique se o ID existe e os campos estão preenchidos.")
                        except Exception as e:
                            st.error(f"❌ Erro: {e}")
        else:
            create_info_box("Nenhum coordenador cadastrado para alterar.", "info")