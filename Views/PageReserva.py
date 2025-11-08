# Views/PageReserva.py
import streamlit as st
import pandas as pd
import datetime
from Models.Reserva import Reserva
from Controllers.ReservaController import incluir_reserva, consultar_reservas, excluir_reserva
from Controllers.PassageiroController import consultar_passageiros
from Controllers.AssentoController import consultar_assentos

def show_reserva_page():
    
    st.title('Sistema de Reservas')
    
    operacao = st.sidebar.selectbox("Operações Reserva", ["Registrar", "Consultar", "Cancelar"])

    # Carrega dados para os selectbox
    passageiros_data = consultar_passageiros()
    passageiro_options = {p[0]: f"{p[3]} (ID: {p[0]})" for p in passageiros_data}
    
    assentos_data = consultar_assentos()
    # Filtra apenas assentos disponíveis
    assento_options = {a[0]: f"Assento {a[3]} (Ônibus {a[1]})" for a in assentos_data if a[4] == 1} # a[4] é Disponibilidade

    if operacao == "Registrar":
        st.header("Registrar Nova Reserva")
        
        if not passageiro_options or not assento_options:
            st.warning("⚠️ Cadastre Passageiros e Assentos (disponíveis) antes de registrar uma reserva.")
            return

        with st.form(key="form_reserva"):
            selected_passageiro = st.selectbox(
                "Passageiro*:",
                options=list(passageiro_options.keys()),
                format_func=lambda x: passageiro_options[x]
            )
            
            selected_assento = st.selectbox(
                "Assento Disponível*:",
                options=list(assento_options.keys()),
                format_func=lambda x: assento_options[x]
            )
            
            data_viagem = st.date_input("Data da Viagem:", value=datetime.date.today())
            
            status_reserva = st.checkbox("Reserva Confirmada (Paga)", value=True)

            if st.form_submit_button("✅ Registrar Reserva"):
                try:
                    data_str = data_viagem.strftime("%Y-%m-%d")
                    nova_reserva = Reserva(0, selected_passageiro, selected_assento, data_str, status_reserva)
                    
                    if incluir_reserva(nova_reserva):
                        st.success("Reserva registrada com sucesso!")
                        st.balloons()
                    # A msg de erro de duplicidade é tratada no Controller
                except Exception as e:
                    st.error(f"Erro: {str(e)}")

    elif operacao == "Consultar":
        st.header("Histórico de Reservas")
        reservas = consultar_reservas()
        if reservas:
            df = pd.DataFrame(reservas, columns=["ID Reserva", "Data Viagem", "Passageiro", "Assento", "ID Ônibus", "Confirmada"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma reserva registrada.")

    elif operacao == "Cancelar":
        st.header("Cancelar Reserva")
        reservas = consultar_reservas()
        if reservas:
            reserva_options = {r[0]: f"ID {r[0]} - {r[1]} - {r[2]}" for r in reservas}
            selected_reserva_id = st.selectbox(
                "Selecione a Reserva para cancelar:",
                options=list(reserva_options.keys()),
                format_func=lambda id: reserva_options[id]
            )
            
            if st.button("🗑️ Cancelar Reserva", type="primary"):
                if excluir_reserva(selected_reserva_id):
                    st.success("Reserva cancelada com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao cancelar reserva.")
        else:
            st.info("Nenhuma reserva para cancelar.")