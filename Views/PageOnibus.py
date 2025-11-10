# Views/PageOnibus.py
import streamlit as st
import pandas as pd
from Models.Onibus import Onibus
from Controllers.OnibusController import (
    incluir_onibus, 
    consultar_onibus, 
    excluir_onibus, 
    alterar_onibus
)
from Controllers.CoordenadorController import consultar_coordenadores
from Views.theme import create_header, create_section_title, create_info_box

def show_onibus_page():
    
    create_header('🚌 Gestão de Ônibus', 'Cadastre e gerenciar os ônibus da frota')
    
    operacao = st.sidebar.selectbox("📋 Operações", ["Incluir", "Consultar", "Excluir", "Alterar"])

    # Carrega coordenadores para a lista de seleção (Foreign Key)
    coordenadores_data = consultar_coordenadores()
    coordenador_options = {c[0]: f"{c[1]} (ID: {c[0]})" for c in coordenadores_data}
    coordenador_ids = list(coordenador_options.keys())
    
    if operacao == "Incluir":
        create_section_title("Incluir Novo Ônibus", "➕")
        
        if not coordenador_ids:
            create_info_box("Cadastre Coordenadores antes de cadastrar Ônibus.", "warning")
            return

        with st.form(key="incluir_onibus_form"):
            onibus = Onibus(0, "", None)
            
            col1, col2 = st.columns(2)
            with col1:
                onibus.set_id(st.number_input("ID do Ônibus:", min_value=1, step=1))
            with col2:
                onibus.set_motorista(st.text_input("Nome do Motorista:"))
            
            # Seleção da Chave Estrangeira
            selected_coordenador_id = st.selectbox(
                "👨‍💼 Coordenador Responsável:",
                options=coordenador_ids,
                format_func=lambda id: coordenador_options[id]
            )
            onibus.set_id_coordenador(selected_coordenador_id)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Cadastrar Ônibus", use_container_width=True):
                    if incluir_onibus(onibus):
                        st.success(f"✅ Ônibus {onibus.get_id()} cadastrado com sucesso!")
                    else:
                        st.error("❌ Erro ao cadastrar. O ID pode já existir.")

    elif operacao == "Consultar":
        create_section_title("Lista de Ônibus", "📊")
        if st.button("🔍 Consultar Ônibus", use_container_width=True):
            onibus_list = consultar_onibus()
            if onibus_list:
                df = pd.DataFrame(onibus_list)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                create_info_box("Nenhum ônibus cadastrado no sistema.", "info")
                
    elif operacao == "Excluir":
        create_section_title("Excluir Ônibus", "🗑️")
        with st.form(key="excluir_onibus_form"):
            id_onibus = st.number_input("ID do Ônibus a ser excluído:", min_value=1, step=1)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("🗑️ Excluir Ônibus", use_container_width=True):
                    if excluir_onibus(id_onibus):
                        st.success(f"✅ Ônibus {id_onibus} excluído com sucesso!")
                    else:
                        st.error("❌ Erro ao excluir. Verifique se o ID existe.")

    elif operacao == "Alterar":
        create_section_title("Alterar Ônibus", "✏️")
        
        if not coordenador_ids:
            create_info_box("Cadastre Coordenadores antes de alterar Ônibus.", "warning")
            return
            
        with st.form(key="alterar_onibus_form"):
            onibus = Onibus(0, "", None)
            
            col1, col2 = st.columns(2)
            with col1:
                onibus.set_id(st.number_input("ID do Ônibus a ser alterado:", min_value=1, step=1))
            with col2:
                onibus.set_motorista(st.text_input("Novo nome do Motorista:"))
            
            # Seleção da Chave Estrangeira
            selected_coordenador_id = st.selectbox(
                "👨‍💼 Novo Coordenador Responsável:",
                options=coordenador_ids,
                format_func=lambda id: coordenador_options[id]
            )
            onibus.set_id_coordenador(selected_coordenador_id)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Alterar Ônibus", use_container_width=True):
                    if alterar_onibus(onibus):
                        st.success(f"✅ Ônibus {onibus.get_id()} alterado com sucesso!")
                    else:
                        st.error("❌ Erro ao alterar. Verifique se o ID existe.")