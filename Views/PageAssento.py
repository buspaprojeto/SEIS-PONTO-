# Views/PageAssento.py
import streamlit as st
import pandas as pd
from Models.Assento import Assento
from Controllers.AssentoController import incluir_assento, consultar_assentos, excluir_assento, consultar_assentos_por_onibus
from Controllers.OnibusController import consultar_onibus
from Views.utils import set_background

def show_assento_page():
    set_background('assentoViews/Images/.jpg')
    st.title('Gerenciamento de Assentos')
    
    operacao = st.sidebar.selectbox("Operações Assento", ["Incluir", "Consultar", "Excluir"])

    # Carrega ônibus para a lista de seleção
    onibus_data = consultar_onibus()
    onibus_options = {o["Id"]: f"ID {o['Id']} - Motorista: {o['Motorista']}" for o in onibus_data}
    onibus_ids = list(onibus_options.keys())

    if operacao == "Incluir":
        st.header("Cadastrar Novo Assento")

        if not onibus_ids:
            st.warning("⚠️ Cadastre um Ônibus antes de cadastrar assentos.")
            return

        selected_onibus_id = st.selectbox(
            "Selecione o Ônibus:",
            options=onibus_ids,
            format_func=lambda id: onibus_options.get(id, f"ID {id}")
        )

        if selected_onibus_id:
            assentos_no_onibus = consultar_assentos_por_onibus(selected_onibus_id)
            assentos_ocupados = [int(a[2]) for a in assentos_no_onibus if a[2].isdigit()]

            total_assentos = 40
            todos_assentos = list(range(total_assentos + 1))

            assentos_disponiveis = [a for a in todos_assentos if a not in assentos_ocupados]

            if not assentos_disponiveis:
                st.warning("Todos os assentos de 0 a 40 já estão cadastrados para este ônibus.")
                return

            with st.form(key="incluir_assento_form"):
                localizacao = st.selectbox("Selecione o número do assento:", options=assentos_disponiveis)
                disponivel = st.checkbox("Disponível", value=True)

                submit_button = st.form_submit_button("Cadastrar Assento")

                if submit_button:
                    assento = Assento(0, selected_onibus_id, str(localizacao), disponivel)
                    if incluir_assento(assento):
                        st.success(f"Assento {localizacao} cadastrado com sucesso para o ônibus {selected_onibus_id}!")
                        st.rerun()
                    else:
                        st.error("Erro ao cadastrar Assento.")

    elif operacao == "Consultar":
        st.header("Lista de Assentos")
        assentos = consultar_assentos()
        if assentos:
            df = pd.DataFrame(assentos, columns=["ID", "ID Ônibus", "Motorista", "Localização", "Disponível"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum assento cadastrado.")

    elif operacao == "Excluir":
        st.header("Excluir Assento")
        assentos = consultar_assentos()
        if assentos:
            df = pd.DataFrame(assentos, columns=["ID", "ID Ônibus", "Motorista", "Localização", "Disponível"])
            st.table(df)

            id_excluir = st.number_input("ID do Assento a excluir:", min_value=1, step=1)
            if st.button("Excluir Assento"):
                if excluir_assento(id_excluir):
                    st.success(f"Assento {id_excluir} excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Falha ao excluir. O assento pode estar em uma reserva.")
        else:
            st.info("Nenhum assento para excluir.")