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
from Views.theme import create_header, create_section_title, create_info_box

def show_mapa_assentos_page():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #f0f2f5 100%);
        }
        
        div[data-testid="stButton"] button {
            width: 48px !important;
            height: 48px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 16px !important;
            font-weight: bold !important;
            margin: 6px !important;
            background-color: #27ae60 !important;
            color: white !important;
            border: 2px solid #229954 !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3) !important;
        }

        div[data-testid="stButton"] button:disabled {
            background-color: #e74c3c !important;
            border-color: #c0392b !important;
            cursor: not-allowed !important;
            opacity: 1 !important;
            box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3) !important;
        }

        div[data-testid="stButton"] button:hover:not(:disabled) {
            transform: translateY(-2px) scale(1.05) !important;
            box-shadow: 0 6px 16px rgba(39, 174, 96, 0.4) !important;
            opacity: 0.95 !important;
        }
        
        div[data-testid="stButton"] button:active:not(:disabled) {
            transform: translateY(0) scale(1) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    create_header("🛋️ Sistema de Reserva de Assentos", "Selecione um ônibus e escolha seus assentos")
    
    # Seletores em um container estilizado
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            onibus_data = consultar_onibus()
            if not onibus_data:
                create_info_box("Não há ônibus cadastrados.", "warning")
                return
            
            onibus_options = {o["Id"]: f"🚌 Ônibus {o['Id']} - {o['Motorista']}" for o in onibus_data}
            selected_onibus = st.selectbox(
                "🚌 Selecione o Ônibus",
                options=list(onibus_options.keys()),
                format_func=lambda x: onibus_options[x]
            )
        
        with col2:
            passageiros = consultar_passageiros()
            if not passageiros:
                create_info_box("Não há passageiros cadastrados.", "warning")
                return
            
            passageiro_options = {p[0]: f"👤 {p[3]} (ID: {p[0]})" for p in passageiros}
            selected_passageiro = st.selectbox(
                "👤 Selecione o Passageiro",
                options=list(passageiro_options.keys()),
                format_func=lambda x: passageiro_options[x]
            )
    
    st.markdown("---")
    create_section_title("Mapa de Assentos", "🗺️")
    
    # Container do mapa de assentos
    with st.container():
        # Frente do ônibus
        st.markdown("""
            <div style='text-align: center; background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); 
                        color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; 
                        font-weight: 700; font-size: 1.2em; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                🚌 FRENTE DO ÔNIBUS
            </div>
        """, unsafe_allow_html=True)
        
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
                                   help="Ocupado ❌" if ocupado else "Disponível ✅"):
                            try:
                                novo_assento = Assento(0, selected_onibus, str(assento_num), True)
                                assento_id = incluir_assento(novo_assento)
                                
                                if assento_id and vincular_passageiro_assento(assento_id, selected_passageiro):
                                    placeholder = st.empty()
                                    placeholder.success(f"✅ Assento {assento_num} reservado para {passageiro_options[selected_passageiro]}")
                                    time.sleep(2)
                                    placeholder.empty()
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao reservar o assento.")
                            except Exception as e:
                                st.error(f"❌ Erro: {str(e)}")

        # Corredor (coluna do meio)
        with corredor:
            st.markdown("""
                <div style='background: linear-gradient(180deg, #ecf0f1 0%, #bdc3c7 100%); 
                           height: 100%; min-height: 500px; border-radius: 10px; 
                           box-shadow: inset 0 2px 8px rgba(0,0,0,0.1);'></div>
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
                                   help="Ocupado ❌" if ocupado else "Disponível ✅"):
                            try:
                                novo_assento = Assento(0, selected_onibus, str(assento_num), True)
                                assento_id = incluir_assento(novo_assento)
                                
                                if assento_id and vincular_passageiro_assento(assento_id, selected_passageiro):
                                    placeholder = st.empty()
                                    placeholder.success(f"✅ Assento {assento_num} reservado para {passageiro_options[selected_passageiro]}")
                                    time.sleep(2)
                                    placeholder.empty()
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao reservar o assento.")
                            except Exception as e:
                                st.error(f"❌ Erro: {str(e)}")

    st.markdown("---")
    
    # Legenda
    st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 12px; margin-top: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #ecf0f1;'>
            <h3 style='margin-bottom: 15px; color: #2c3e50;'>📋 Legenda dos Assentos</h3>
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; background: #27ae60; border-radius: 6px; 
                           margin-right: 15px; box-shadow: 0 2px 6px rgba(39, 174, 96, 0.3);'></div>
                <span style='color: #2c3e50; font-size: 1.05em;'><b>Assento Disponível</b> - Clique para reservar</span>
            </div>
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='width: 24px; height: 24px; background: #e74c3c; border-radius: 6px; 
                           margin-right: 15px; box-shadow: 0 2px 6px rgba(231, 76, 60, 0.3);'></div>
                <span style='color: #2c3e50; font-size: 1.05em;'><b>Assento Ocupado</b> - Não disponível para reserva</span>
            </div>
        </div>
    """, unsafe_allow_html=True)