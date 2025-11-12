# Views/theme.py
import streamlit as st

def apply_custom_theme():
    """Aplica tema minimalista sofisticado com sombras e bordas características."""
    st.markdown("""
        <style>
        :root {
            --primary-color: #000000;
            --secondary-color: #3498db;
            --accent-color: #1abc9c;
            --danger-color: #e74c3c;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --light-bg: #f8f9fa;
            --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            --hover-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
            --menu-bg: #000000;
            --menu-text: #ffffff;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #f0f2f5 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #000000;
        }

        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #f0f2f5 100%);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #000000;
            box-shadow: 2px 0 12px rgba(0, 0, 0, 0.15);
        }

        [data-testid="stSidebar"] > div:first-child {
            background: #000000;
        }

        /* Header */
        h1 {
            background: linear-gradient(135deg, #000000 0%, #3498db 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 30px;
            font-size: 2.5em;
            font-weight: 700;
            letter-spacing: -1px;
        }

        h2 {
            color: #000000;
            margin-bottom: 20px;
            border-bottom: 3px solid #1abc9c;
            padding-bottom: 12px;
            font-weight: 600;
        }

        h3, h4, h5, h6 {
            color: #000000;
            font-weight: 600;
            letter-spacing: -0.5px;
        }

        /* Form Container */
        [data-testid="stForm"] {
            background: white;
            border-radius: 14px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            padding: 28px;
            border: 1px solid #ecf0f1;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        [data-testid="stForm"]:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }

        /* Container */
        [data-testid="stContainer"] {
            background: white;
            border-radius: 14px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            padding: 24px;
            border: 1px solid #ecf0f1;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 20px;
        }

        [data-testid="stContainer"]:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }

        /* Input Fields */
        input, textarea, select {
            border-radius: 10px;
            border: 2px solid #ecf0f1;
            background: #f8f9fa;
            padding: 12px 16px;
            font-size: 1em;
            transition: all 0.3s ease;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #000000;
        }

        input:focus, textarea:focus, select:focus {
            border-color: #3498db;
            background: white;
            box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.1);
            outline: none;
            color: #000000 !important;
        }

        input::placeholder {
            color: #999999;
        }

        textarea::placeholder {
            color: #999999;
        }

        /* Selectbox and dropdown options styling */
        select option {
            background: white;
            color: #000000;
        }

        select option:checked {
            background: #3498db;
            color: #000000;
        }

        /* Buttons */
        [data-testid="stButton"] > button {
            border-radius: 12px;
            border: none;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            padding: 12px 28px !important;
            cursor: pointer;
            background: linear-gradient(135deg, #3498db 0%, #1abc9c 100%) !important;
            color: #000000 !important;
            font-size: 1em;
        }

        [data-testid="stButton"] > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(52, 152, 219, 0.3);
        }

        [data-testid="stButton"] > button:active {
            transform: translateY(-1px);
        }

        [data-testid="stButton"] > button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        /* Primary Button */
        [data-testid="stButton"] > button[type="button"]:not(:disabled) {
            background: linear-gradient(135deg, #3498db 0%, #1abc9c 100%) !important;
        }

        /* Secondary Button (selectbox, etc) */
        [data-testid="stButton"] > button[type="secondary"] {
            background: #f8f9fa !important;
            color: #000000 !important;
            border: 2px solid #3498db;
        }

        /* Alert Messages */
        [data-testid="stAlert"] {
            border-radius: 12px;
            border-left: 5px solid;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            padding: 16px;
        }

        .stSuccess [data-testid="stAlert"] {
            border-left-color: #27ae60;
            background-color: rgba(39, 174, 96, 0.06);
        }

        .stError [data-testid="stAlert"] {
            border-left-color: #e74c3c;
            background-color: rgba(231, 76, 60, 0.06);
        }

        .stWarning [data-testid="stAlert"] {
            border-left-color: #f39c12;
            background-color: rgba(243, 156, 18, 0.06);
        }

        .stInfo [data-testid="stAlert"] {
            border-left-color: #3498db;
            background-color: rgba(52, 152, 219, 0.06);
        }

        /* Dataframe */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            border: 1px solid #ecf0f1;
            overflow: hidden;
        }

        /* Expander */
        [data-testid="stExpander"] {
            border: 2px solid #ecf0f1;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            overflow: hidden;
            margin-bottom: 12px;
        }

        [data-testid="stExpander"] button {
            border-radius: 10px;
            background: #000000;
            border: none;
            transition: all 0.3s ease;
            font-weight: 600;
            color: #ffffff;
        }

        [data-testid="stExpander"] button:hover {
            background: #111111;
        }

        /* Column */
        [data-testid="stColumn"] {
            transition: all 0.3s ease;
        }

        /* Scroll bar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #3498db 0%, #1abc9c 100%);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #2980b9 0%, #16a085 100%);
        }

        /* Selectbox */
        [data-testid="stSelectbox"] > div > div {
            background: white;
            border-radius: 10px;
            border: 2px solid #ecf0f1;
            color: #000000 !important;
        }

        [data-testid="stSelectbox"] [role="option"],
        [data-testid="stSelectbox"] [role="listbox"] {
            background: white !important;
            color: #000000 !important;
        }

        [data-testid="stSelectbox"] [role="option"][aria-selected="true"],
        [data-testid="stSelectbox"] [aria-selected="true"] {
            background: #3498db !important;
            color: #000000 !important;
        }

        /* Table */
        table {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }

        table tr:hover {
            background-color: #f8f9fa;
        }

        /* Cards customizados */
        .card {
            background: white;
            border-radius: 14px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            padding: 24px;
            margin: 16px 0;
            border: 1px solid #ecf0f1;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }

        .metric-card {
            background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
            border-radius: 14px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            border-top: 4px solid #3498db;
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }

        /* Markdown containers em geral (garante texto preto sobre fundo claro) */
        [data-testid="stMarkdownContainer"] {
            color: #000000 !important;
        }

        /* Sidebar text */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: white !important;
        }

        /* Menu Select Box styling */
        [data-testid="stSelectbox"] {
            margin-bottom: 20px;
        }

        [data-testid="stSelectbox"] > label {
            font-weight: 600;
            color: #000000;
            letter-spacing: 0.5px;
        }
        </style>
    """, unsafe_allow_html=True)

def create_header(title, subtitle=""):
    """Cria um header estilizado e elegante."""
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="margin-bottom: 10px;">{title}</h1>
            {f'<p style="color: #7f8c8d; font-size: 1.1em; margin: 0;">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)

def create_section_title(title, icon=""):
    """Cria um título de seção estilizado."""
    st.markdown(f"""
        <div style="margin: 30px 0 20px 0; padding-left: 15px; border-left: 5px solid #1abc9c;">
            <h3 style="color: #2c3e50; font-weight: 700; margin: 0;">{icon} {title}</h3>
        </div>
    """, unsafe_allow_html=True)

def create_info_box(text, info_type="info"):
    """Cria caixas de informação estilizadas."""
    colors = {
        "info": ("#3498db", "ℹ️"),
        "success": ("#27ae60", "✅"),
        "warning": ("#f39c12", "⚠️"),
        "error": ("#e74c3c", "❌")
    }
    color, icon = colors.get(info_type, colors["info"])
    
    st.markdown(f"""
        <div style="background-color: {color}15; border-left: 5px solid {color}; 
                    border-radius: 8px; padding: 16px; margin: 10px 0;">
            <p style="color: {color}; font-weight: 600; margin: 0;">{icon} {text}</p>
        </div>
    """, unsafe_allow_html=True)

def create_card(content, title=""):
    """Cria um card estilizado."""
    st.markdown(f"""
        <div style="background: white; border-radius: 14px; 
                    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
                    padding: 24px; margin: 16px 0; border: 1px solid #ecf0f1;">
            {f'<h4 style="color: #2c3e50; margin-bottom: 16px;">{title}</h4>' if title else ''}
            {content}
        </div>
    """, unsafe_allow_html=True)
