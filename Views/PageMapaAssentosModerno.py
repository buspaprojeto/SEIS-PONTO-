# Views/PageMapaAssentosModerno.py
import streamlit as st
import time
from Models.Assento import Assento
from Controllers.AssentoController import (
    consultar_assentos,
    alterar_assento,
    get_passageiro_do_assento,
    vincular_passageiro_assento,
    incluir_assento
)
from Controllers.PassageiroController import consultar_passageiros
from Controllers.OnibusController import consultar_onibus

def show_mapa_assentos_page():
    st.markdown("""
        <style>
        .stApp {
            background: #f5f7fa;
        }
        
        div[data-testid="stButton"] button {
            width: 45px !important;
            height: 45px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 16px !important;
            font-weight: bold !important;
            margin: 5px !important;
            background-color: #4CAF50 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }

        div[data-testid="stButton"] button:disabled {
            background-color: #f44336 !important;
            cursor: not-allowed !important;
            opacity: 1 !important;
        }

        div[data-testid="stButton"] button:hover:not(:disabled) {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            opacity: 0.9 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>Sistema de Reserva de Assentos</h1>", unsafe_allow_html=True)
    
    # Seletores em um container estilizado
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            onibus_data = consultar_onibus()
            if not onibus_data:
                st.warning("⚠️ Não há ônibus cadastrados.")
                return
            
            onibus_options = {o["Id"]: f"🚌 Ônibus {o['Id']} - {o['Motorista']}" for o in onibus_data}
            selected_onibus = st.selectbox(
                "Selecione o Ônibus",
                options=list(onibus_options.keys()),
                format_func=lambda x: onibus_options[x]
            )
        
        with col2:
            passageiros = consultar_passageiros()
            if not passageiros:
                st.warning("⚠️ Não há passageiros cadastrados.")
                return
            
            passageiro_options = {p[0]: f"👤 {p[3]} (ID: {p[0]})" for p in passageiros}
            selected_passageiro = st.selectbox(
                "Selecione o Passageiro",
                options=list(passageiro_options.keys()),
                format_func=lambda x: passageiro_options[x]
            )
    
    # Container do mapa de assentos
    with st.container():
        # Layout principal com 3 colunas (assentos esquerda, corredor, assentos direita)
        col_esq, corredor, col_dir = st.columns([4, 1, 4])

        # Coluna da esquerda (assentos 1-20)
        with col_esq:
            for i in range(0, 20, 2):  # 10 linhas com 2 assentos cada
                cols = st.columns(2)
                for j, col in enumerate(cols):
                    with col:
                        assento_num = i + j + 1
                        passageiro_info = get_passageiro_do_assento(selected_onibus, str(assento_num))
                        ocupado = passageiro_info is not None
                        
                        if st.button(f"{assento_num}", key=f"seat_{assento_num}", disabled=ocupado,
                                   help="Ocupado" if ocupado else "Disponível"):
                            try:
                                novo_assento = Assento(0, selected_onibus, str(assento_num), True)
                                assento_id = incluir_assento(novo_assento)
                                
                                if assento_id and vincular_passageiro_assento(assento_id, selected_passageiro):
                                    placeholder = st.empty()
                                    placeholder.success(f"✅ Assento {assento_num} reservado com sucesso!")
                                    time.sleep(3)
                                    placeholder.empty()
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao reservar o assento.")
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

        # Corredor (coluna do meio)
        with corredor:
            st.markdown("""
                <div style='background: #e0e0e0; height: 100%; min-height: 500px; border-radius: 10px;'></div>
            """, unsafe_allow_html=True)

        # Coluna da direita (assentos 21-40)
        with col_dir:
            for i in range(20, 40, 2):  # 10 linhas com 2 assentos cada
                cols = st.columns(2)
                for j, col in enumerate(cols):
                    with col:
                        assento_num = i + j + 1
                        passageiro_info = get_passageiro_do_assento(selected_onibus, str(assento_num))
                        ocupado = passageiro_info is not None
                        
                        if st.button(f"{assento_num}", key=f"seat_{assento_num}", disabled=ocupado,
                                   help="Ocupado" if ocupado else "Disponível"):
                            try:
                                novo_assento = Assento(0, selected_onibus, str(assento_num), True)
                                assento_id = incluir_assento(novo_assento)
                                
                                if assento_id and vincular_passageiro_assento(assento_id, selected_passageiro):
                                    placeholder = st.empty()
                                    placeholder.success(f"✅ Assento {assento_num} reservado com sucesso!")
                                    time.sleep(3)
                                    placeholder.empty()
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao reservar o assento.")
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")

    # Legenda
    st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 10px; margin-top: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='margin-bottom: 15px;'>Legenda dos Assentos</h3>
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 20px; height: 20px; background: #4CAF50; border-radius: 5px; margin-right: 10px;'></div>
                <span>Assento Disponível</span>
            </div>
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 20px; height: 20px; background: #f44336; border-radius: 5px; margin-right: 10px;'></div>
                <span>Assento Ocupado</span>
            </div>
        </div>
    """, unsafe_allow_html=True)