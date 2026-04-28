import streamlit as st
from datetime import datetime

# 1. Configuração Visual
st.set_page_config(page_title="Pangeia Nazaré - Gestão", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #D4AF37; }
    .mesa-box {
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 15px; border-radius: 8px; text-align: center;
        background: rgba(255, 255, 255, 0.02); margin-bottom: 10px;
        min-height: 100px;
    }
    .mesa-ocupada { 
        background: linear-gradient(145deg, #D4AF37, #B8860B) !important;
        color: #000 !important; font-weight: bold; border: none;
    }
    .label-zona { color: #444; font-size: 0.7em; text-align: center; letter-spacing: 3px; margin-bottom: 10px; }
    .escadas { background: #111; border: 1px dashed #444; padding: 15px; text-align: center; color: #555; font-size: 0.7em; }
    </style>
    """, unsafe_allow_html=True)

# 2. Estado das Mesas
MESAS_INFO = {
    1: "2p", 2: "4-7p", 3: "2p", 4: "4-7p", 6: "2p", 7: "2p", 8: "4-6p", 
    9: "4-6p", 10: "2p", 11: "2p", 12: "2p", 14: "2p", 16: "4-7p", 
    17: "4-7p", 18: "2-3p", 19: "2p", 20: "2p"
}

if 'sala' not in st.session_state:
    st.session_state.sala = {m: {"ocupada": False, "nome": ""} for m in MESAS_INFO}

# --- SIDEBAR ---
with st.sidebar:
    st.title("RESERVA")
    nome_reserva = st.text_input("Nome Cliente")
    pax_reserva = st.number_input("Nº Pessoas", 1, 20, 2)

# --- FUNÇÃO DE RENDERIZAÇÃO ---
def exibir_mesa(m_id, col):
    info = st.session_state.sala[m_id]
    estilo = "mesa-box mesa-ocupada" if info["ocupada"] else "mesa-box"
    status = info['nome'] if info["ocupada"] else "LIVRE"
    
    col.markdown(f'<div class="{estilo}"><b>M{m_id}</b><br><small>{MESAS_INFO[m_id]}</small><br>{status}</div>', unsafe_allow_html=True)
    
    c_btn1, c_btn2 = col.columns(2)
    if not info["ocupada"]:
        if c_btn1.button("SENTAR", key=f"s{m_id}"):
            if nome_reserva:
                st.session_state.sala[m_id] = {"ocupada": True, "nome": f"{nome_reserva} ({pax_reserva}p)"}
                st.rerun()
            else: st.sidebar.error("Falta o nome!")
    else:
        if c_btn1.button("LIBERTAR", key=f"l{m_id}"):
            st.session_state.sala[m_id] = {"ocupada": False, "nome": ""}
            st.rerun()

# --- LAYOUT DE SALA ---
st.markdown("<h2 style='text-align:center; letter-spacing:5px;'>PANGEIA NAZARÉ</h2>", unsafe_allow_html=True)

col_esq, col_meio, col_dir = st.columns(3)

with col_esq: # ALA PAREDE
    st.markdown("<div class='label-zona'>PAREDE</div>", unsafe_allow_html=True)
    for m in [11, 10, 9, 8]: exibir_mesa(m, col_esq)
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True) # Alinhamento
    exibir_mesa(7, col_esq) # NIVELADA COM A 6

with col_meio: # CENTRO
    st.markdown("<div class='label-zona'>CENTRO</div>", unsafe_allow_html=True)
    exibir_mesa(12, col_meio)
    exibir_mesa(19, col_meio)
    exibir_mesa(20, col_meio)
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    exibir_mesa(6, col_meio) # NIVELADA COM A 7
    st.markdown("<div style='height:115px;'></div>", unsafe_allow_html=True) # Espaço para alinhar 4 com 2
    exibir_mesa(4, col_meio) # NIVELADA COM A 2

with col_dir: # ALA JANELA
    st.markdown("<div class='label-zona'>JANELA</div>", unsafe_allow_html=True)
    for m in [14, 16, 17, 18]: exibir_mesa(m, col_dir)
    st.markdown("<div class='escadas'>ESCADAS</div><br>", unsafe_allow_html=True)
    exibir_mesa(1, col_dir)
    exibir_mesa(2, col_dir) # NIVELADA COM A 4
    exibir_mesa(3, col_dir)

if st.button("LIMPAR MAPA"):
    st.session_state.sala = {m: {"ocupada": False, "nome": ""} for m in MESAS_INFO}
    st.rerun()
