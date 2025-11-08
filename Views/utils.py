\
# Views/utils.py
import streamlit as st

# Arquivo utilitário para funções comuns
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
