# main.py
import streamlit as st
import sys
from pathlib import Path
import importlib

# 1. Adiciona o diretório raiz ao path para importação dos módulos
# Isso é essencial para que os imports funcionem corretamente
sys.path.append(str(Path(__file__).parent))

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
    "Assento": "Views.PageAssento", # Assumindo a criação
    "Passageiro": "Views.PagePassageiro", # Assumindo a criação
    "Reservas": "Views.PageReserva" # Assumindo a criação
}

# 4. Função para carregar páginas de forma dinâmica
def load_page(page_name):
    """Carrega um módulo de página dinamicamente."""
    try:
        module_path = PAGES[page_name]
        module = importlib.import_module(module_path)
        # Formata o nome da função (ex: show_coordenador_page, show_onibus_page)
        page_name_clean = page_name.lower().replace("ô", "o")
        return getattr(module, f"show_{page_name_clean}_page")
    except (ImportError, AttributeError, KeyError) as e:
        st.error(f"Erro ao carregar a página {page_name}. Verifique se o arquivo e a função existem: {e}")
        return None

# 5. Função principal
def main():
    st.set_page_config(page_title="Sistema de Reserva de Ônibus", layout="wide", initial_sidebar_state="auto")
    st.title('Sistema de Gestão de Transporte')
    
    with st.sidebar:
        st.title("Menu")
        page_selection = st.selectbox("Selecione uma opção", list(PAGES.keys()))
    
    # Carrega e exibe a página selecionada
    show_page = load_page(page_selection)
    if show_page: show_page()

# 6. Ponto de entrada
if __name__ == "__main__":
    main()