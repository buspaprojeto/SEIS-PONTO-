# main.py
import streamlit as st
import sys
from pathlib import Path
import importlib
from Views.theme import apply_custom_theme

# 1. Adiciona o diretório raiz ao path para importação dos módulos
# Isso é essencial para que os imports funcionem corretamente
sys.path.append(str(Path(__file__).parent))

# Aplica o tema customizado
apply_custom_theme()

# 2. Inicializa o banco de dados e cria as tabelas
try:
    from Services.database_setup import criar_tabelas
    # Cria as tabelas na inicialização do aplicativo
    criar_tabelas() 
except Exception as e:
    st.error(f"Erro crítico ao inicializar o banco de dados: {e}")
    sys.exit()

# 3. Dicionário de páginas disponíveis
PAGES = {
    "Coordenador": "Views.PageCoordenador", 
    "Ônibus": "Views.PageOnibus",
    "Passageiro": "Views.PagePassageiro",
    "Mapa de Assentos (Moderno)": "Views.PageMapaAssentosModerno"
}

# 4. Função para carregar páginas de forma dinâmica
def load_page(page_name):
    """Carrega um módulo de página dinamicamente."""
    try:
        module_path = PAGES[page_name]
        module = importlib.import_module(module_path)
        
        # Mapeamento especial para nomes de funções
        function_mapping = {
            "Mapa de Assentos (Moderno)": "show_mapa_assentos_page",
            "Coordenador": "show_coordenador_page",
            "Ônibus": "show_onibus_page",
            "Assento": "show_assento_page",
            "Passageiro": "show_passageiro_page"
        }
        
        function_name = function_mapping.get(page_name)
        if not function_name:
            # Fallback para o comportamento padrão
            page_name_clean = page_name.lower().replace("ô", "o")
            function_name = f"show_{page_name_clean}_page"
            
        return getattr(module, function_name)
    except (ImportError, AttributeError, KeyError) as e:
        st.error(f"Erro ao carregar a página {page_name}. Verifique se o arquivo e a função existem: {e}")
        return None

# 5. Função principal
def main():
    st.set_page_config(
        page_title="🚌 Sistema de Gestão de Transporte", 
        layout="wide", 
        initial_sidebar_state="auto",
        menu_items={
            "Get help": "https://github.com",
            "Report a Bug": "https://github.com",
            "About": "Sistema de Gestão de Transporte e Reserva de Ônibus v1.0"
        }
    )
    
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 20px 0;">
                <h2 style="color: white; margin: 0; font-size: 1.8em;">🚌 Transporte</h2>
                <p style="color: #ecf0f1; margin: 5px 0; font-size: 0.9em;">Sistema de Gestão</p>
            </div>
            <hr style="border-color: #34495e; margin: 20px 0;">
        """, unsafe_allow_html=True)
        
        st.title("📋 Menu Principal")
        page_selection = st.selectbox(
            "Selecione uma opção:",
            list(PAGES.keys()),
            label_visibility="collapsed"
        )
    
    # Carrega e exibe a página selecionada
    show_page = load_page(page_selection)
    if show_page: show_page()

# 6. Ponto de entrada
if __name__ == "__main__":
    main()