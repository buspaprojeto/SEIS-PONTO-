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
from Views.theme import create_header, create_section_title, create_info_box

def show_passageiro_page():
    create_header('👥 Gestão de Passageiros', 'Gerencie os passageiros cadastrados')
    
    operacao = st.sidebar.selectbox("📋 Operações", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if operacao == "Incluir":
        create_section_title("Cadastrar Novo Passageiro", "➕")
        with st.form(key="incluir_passageiro_form"):
            nome = st.text_input("✏️ Nome do Passageiro:")
            col1, col2 = st.columns(2)
            with col1:
                numero = st.number_input("📞 Número (Telefone/Matrícula):", min_value=1, step=1)
            with col2:
                carteirinha = st.text_input("🎫 Carteirinha (Opcional):")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Cadastrar Passageiro", use_container_width=True):
                    passageiro = Passageiro(0, numero, None, carteirinha, nome)
                    if incluir_passageiro(passageiro):
                        st.success("✅ Passageiro cadastrado com sucesso!")
                    else:
                        st.error("❌ Erro ao cadastrar. O 'Número' pode já existir.")

    elif operacao == "Consultar":
        create_section_title("Lista de Passageiros", "📊")
        passageiros = consultar_passageiros()
        if passageiros:
            df = pd.DataFrame(passageiros, columns=["ID", "Número", "Carteirinha", "Nome", "ID Assento", "Local"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            create_info_box("Nenhum passageiro cadastrado.", "info")
            
    elif operacao == "Excluir":
        create_section_title("Excluir Passageiro", "🗑️")
        passageiros = consultar_passageiros()
        if passageiros:
            df = pd.DataFrame(passageiros, columns=["ID", "Número", "Carteirinha", "Nome", "ID Assento", "Local"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                id_excluir = st.number_input("ID do Passageiro a excluir:", min_value=1, step=1)
            with col2:
                if st.button("🗑️ Excluir", use_container_width=True):
                    if excluir_passageiro(id_excluir):
                        st.success(f"✅ Passageiro {id_excluir} excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Falha ao excluir. Verifique se o ID existe.")
        else:
            create_info_box("Nenhum passageiro para excluir.", "warning")
            
    elif operacao == "Alterar":
        create_section_title("Alterar Passageiro", "✏️")
        passageiros = consultar_passageiros()
        if passageiros:
            df = pd.DataFrame(passageiros, columns=["ID", "Número", "Carteirinha", "Nome", "ID Assento", "Local"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            with st.form(key="alterar_passageiro_form"):
                id_alterar = st.number_input("ID do Passageiro a alterar:", min_value=1, step=1)
                nome = st.text_input("✏️ Novo Nome do Passageiro:")
                col1, col2 = st.columns(2)
                with col1:
                    numero = st.number_input("📞 Novo Número (Telefone/Matrícula):", min_value=1, step=1)
                with col2:
                    carteirinha = st.text_input("🎫 Nova Carteirinha (Opcional):")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Alterar Passageiro", use_container_width=True):
                        passageiro = Passageiro(id_alterar, numero, None, carteirinha, nome)
                        if alterar_passageiro(passageiro):
                            st.success(f"✅ Passageiro {id_alterar} alterado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao alterar. Verifique se o ID existe.")
        else:
            create_info_box("Nenhum passageiro cadastrado para alterar.", "info")