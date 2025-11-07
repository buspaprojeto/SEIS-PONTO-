\
# Views/utils.py
import streamlit as st
import base64
from pathlib import Path

def set_background(image_file):
    """
    Define o plano de fundo de uma página do Streamlit.
    O usuário deve criar uma pasta 'assets' no diretório raiz e colocar as imagens lá.
    Por exemplo: 'assets/coordenador.jpg'

    Args:
        image_file (str): O caminho para o arquivo de imagem.
    """
    image_path = Path(image_file)
    if image_path.is_file():
        with open(image_path, "rb") as f:
            img = f.read()
        b64 = base64.b64encode(img).decode()
        page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{{b64}}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
            right: 2rem;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
