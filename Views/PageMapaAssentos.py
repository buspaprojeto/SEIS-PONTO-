# Views/PageMapaAssentos.py
import streamlit as st
import pandas as pd
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

def create_bus_layout():
    st.markdown("""
        <style>
        .bus-layout {
            display: flex;
            justify-content: space-between;
            margin: 20px;
            padding: 20px;
            border: 2px solid #333;
            border-radius: 10px;
        }
        .column {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .seat-button {
            width: 60px;
            height: 40px;
            margin: 5px;
            border: 1px solid #333;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            cursor: pointer;
        }
        .seat-occupied {
            background-color: #808080 !important;
            cursor: not-allowed;
        }
        .bus-front {
            width: 100%;
            height: 50px;
            background-color: #333;
            border-radius: 20px 20px 0 0;
            margin-bottom: 20px;
            text-align: center;
            color: white;
            line-height: 50px;
        }
        </style>
    """, unsafe_allow_html=True)

def show_mapa_assentos_page():
    st.title('Mapa de Assentos do Ônibus')
    
    # Selecionar Ônibus
    onibus_data = consultar_onibus()
    if not onibus_data:
        st.warning("Não há ônibus cadastrados.")
        return
        
    onibus_options = {o["Id"]: f"ID {o['Id']} - Motorista: {o['Motorista']}" for o in onibus_data}
    selected_onibus = st.selectbox(
        "Selecione o Ônibus:",
        options=list(onibus_options.keys()),
        format_func=lambda x: onibus_options[x]
    )
    
    # Selecionar Passageiro
    passageiros = consultar_passageiros()
    if not passageiros:
        st.warning("Não há passageiros cadastrados.")
        return
        
    passageiro_options = {p[0]: f"{p[3]} (ID: {p[0]})" for p in passageiros}
    selected_passageiro = st.selectbox(
        "Selecione o Passageiro:",
        options=list(passageiro_options.keys()),
        format_func=lambda x: passageiro_options[x]
    )
    
    # Criar layout do ônibus
    create_bus_layout()
    
    # Consultar assentos ocupados
    assentos_ocupados = consultar_assentos()
    assentos_ocupados_dict = {}
    for a in assentos_ocupados:
        if a[1] == selected_onibus:
            try:
                num_assento = int(a[3])
                assentos_ocupados_dict[(a[1], num_assento)] = a[4]
            except ValueError:
                continue
    
    # Criar layout do ônibus com colunas
    st.markdown('<div class="bus-front">FRENTE DO ÔNIBUS</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="bus-layout">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    def processar_assento(assento_num):
        passageiro_info = get_passageiro_do_assento(selected_onibus, str(assento_num))
        
        # O assento só está realmente ocupado se tiver um passageiro vinculado
        ocupado = passageiro_info is not None
        
        button_text = f"Assento {assento_num}"
        if ocupado:
            button_text = f"Assento {assento_num}\n(Ocupado por {passageiro_info[0]})"
        
        if st.button(button_text, 
                    key=f"assento_{assento_num}",
                    disabled=ocupado,
                    type="secondary" if ocupado else "primary"):
            try:
                if ocupado:
                    st.error(f"Este assento já está ocupado pelo passageiro {passageiro_info[0]}")
                else:
                    # Criar ou obter assento
                    novo_assento = Assento(0, selected_onibus, str(assento_num), True)  # Disponível por padrão
                    assento_id = incluir_assento(novo_assento)
                    
                    if assento_id is not None:
                        if vincular_passageiro_assento(assento_id, selected_passageiro):
                            st.success(f"Assento {assento_num} reservado para o passageiro {passageiro_options[selected_passageiro]}")
                            st.rerun()
                        else:
                            st.error("Erro ao vincular o passageiro ao assento.")
                    else:
                        st.error("Erro ao criar o assento. Por favor, tente novamente.")
            except Exception as e:
                st.error(f"Erro ao processar a reserva: {str(e)}")
    
    # Coluna da esquerda (assentos 1-20)
    with col1:
        for i in range(20):
            processar_assento(i + 1)
    
    # Coluna da direita (assentos 21-40)
    with col2:
        for i in range(20):
            processar_assento(i + 21)
                    
    st.markdown('</div>', unsafe_allow_html=True)
                    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Legenda:")
    st.markdown("🟩 **Verde** - Assento disponível")
    st.markdown("⬜ **Cinza** - Assento ocupado (passe o mouse sobre o assento para ver quem está ocupando)")
