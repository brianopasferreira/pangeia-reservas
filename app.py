import streamlit as st
from datetime import datetime

# 1. Configuração da Página e Branding Pangeia
st.set_page_config(
    page_title="Pangeia Nazaré - Gestão de Sala",
    page_icon="🔱",
    layout="wide"
)

# 2. Estilo CSS Customizado (Preto e Dourado)
st.markdown("""
    <style>
    /* Fundo principal */
    .stApp {
        background-color: #000000;
        color: #D4AF37;
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: #D4AF37 !important;
        text-align: center;
        font-family: 'serif';
    }
    
    /* Cartão da Mesa */
    .mesa-box {
        border: 1px solid #D4AF37;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 15px;
        transition: 0.3s;
        min-height: 120px;
    }
    
    /* Botões */
    .stButton>button {
        background-color: #D4AF37;
        color: black;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        width: 100%;
        margin-top: 10px;
    }
    
    .stButton>button:hover {
        background-color: #FAFAD2;
        color: black;
    }

    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #111111;
        color: #D4AF37;
        border: 1px solid #444;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Definição das Mesas (Conforme a tua planta)
# Nota: Mesas 5, 13 e 15 foram removidas como pedido
MESAS = {
    1: "2pax", 2: "4-7pax", 3: "3pax", 4: "4-7pax", 6: "2pax", 
    7: "4-6pax", 8: "4-6pax", 9: "4-6pax", 10: "2pax", 11: "2pax", 
    12: "2pax", 14: "2pax", 16: "4-7pax", 17: "4-7pax", 18: "2-3pax", 
    19: "2pax", 20: "2pax"
}

# 4. Inicialização do Estado da Sala (Memória da App)
if 'status_sala' not in st.session_state:
    st.session_state.status_sala = {m: {"estado": "Livre", "cliente": ""} for m in MESAS}

# 5. Cabeçalho
st.markdown("<h1>🔱 PANGEIA NAZARÉ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#D4AF37;'>Gestão de Mesas e Ocupação</p>", unsafe_allow_html=True)
st.write("---")

# 6. Grelha de Mesas (Visualização de Sala)
# Criamos 4 colunas para que no telemóvel fique organizado e no PC espaçoso
cols = st.columns(4)

for i, (m_id, capacidade) in enumerate(MESAS.items()):
    dados_mesa = st.session_state.status_sala[m_id]
