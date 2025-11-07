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
from Views.utils import set_background

def show_onibus_page():
    set_background('assets/onibus.jpg')
    st.title('Cadastro de Ônibus')
    
    operacao = st.sidebar.selectbox("Operações Ônibus", ["Incluir", "Consultar", "Excluir", "Alterar"])

    # Carrega coordenadores para a lista de seleção (Foreign Key)
    coordenadores_data = consultar_coordenadores()
    coordenador_options = {c[0]: f"{c[1]} (ID: {c[0]})" for c in coordenadores_data}
    coordenador_ids = list(coordenador_options.keys())
    
    if operacao == "Incluir":
        st.header("Incluir Novo Ônibus")
        
        if not coordenador_ids:
            st.warning("⚠️ Cadastre Coordenadores antes de cadastrar Ônibus.")
            return

        with st.form(key="incluir_onibus_form"):
            onibus = Onibus(0, "", None)
            
            onibus.set_id(st.number_input("ID do Ônibus:", min_value=1, step=1))
            onibus.set_motorista(st.text_input("Nome do Motorista:"))
            
            # Seleção da Chave Estrangeira
            selected_coordenador_id = st.selectbox(
                "Coordenador Responsável:",
                options=coordenador_ids,
                format_func=lambda id: coordenador_options[id]
            )
            onibus.set_id_coordenador(selected_coordenador_id)
            
            if st.form_submit_button("Cadastrar Ônibus"):
                if incluir_onibus(onibus):
                    st.success(f"Ônibus {onibus.get_id()} cadastrado com sucesso!")
                else:
                    st.error("Erro ao cadastrar Ônibus. Verifique se o ID já existe.")

    elif operacao == "Consultar":
        st.header("Lista de Ônibus")
        if st.button("Consultar Ônibus"):
            onibus_list = consultar_onibus()
            if onibus_list:
                df = pd.DataFrame(onibus_list)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhum Ônibus cadastrado.")
                
    # Lógicas de Excluir e Alterar (análogas à do PageCoordenador.py)
    # ...
    st.markdown("---")
    st.markdown("*(A lógica completa para 'Excluir' e 'Alterar' seria implementada aqui.)*")