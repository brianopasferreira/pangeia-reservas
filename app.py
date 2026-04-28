import streamlit as st
from datetime import datetime

# 1. Configuração de Estética Pangeia (Inspirado no Site)
st.set_page_config(page_title="Pangeia Nazaré - Gestão", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #D4AF37; }
    
    /* Cartões das Mesas */
    .mesa-box {
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 15px; border-radius: 8px; text-align: center;
        background: rgba(255, 255, 255, 0.02); margin-bottom: 10px;
    }
    .mesa-ocupada { 
        background: linear-gradient(145deg, #D4AF37, #B8860B) !important;
        color: #000 !important; font-weight: bold; border: none;
    }
    .escadas { 
        background: repeating-linear-gradient(45deg, #111, #111 10px, #222 10px, #222 20px);
        border: 1px solid #444; padding: 20px; text-align: center; color: #666; font-size: 0.8em;
    }
    .janela-label { 
        writing-mode: vertical-rl; text-align: center; color: #444; 
        font-weight: bold; letter-spacing: 5px; opacity: 0.5;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Dados das Mesas
MESAS = {
    1: "2p", 2: "4-7p", 3: "2p", 4: "4-7p", 6: "2p", 7: "2p", 8: "4-6p", 
    9: "4-6p", 10: "2p", 11: "2p", 12: "2p", 14: "2p", 16: "4-7p", 
    17: "4-7p", 18: "2-3p", 19: "2p", 20: "2p"
}

if 'sala' not in st.session_state:
    st.session_state.sala = {m: {"ocupada": False, "nome": ""} for m in MESAS}

# --- SIDEBAR ---
with st.sidebar:
    st.title("RESERVA")
    data_sel = st.date_input("Data", datetime.now())
    if data_sel.weekday() == 0:
        st.error("FECHADO À SEGUNDA")
    nome_reserva = st.text_input("Nome do Cliente")
    pax_reserva = st.number_input("Pessoas", 1, 10, 2)

# --- MAPA DE SALA (Conforme o Desenho) ---
st.markdown("<h1 style='text-align:center; color:#D4AF37;'>PANGEIA NAZARÉ</h1>", unsafe_allow_html=True)

def render_mesa(m_id, col):
    info = st.session_state.sala[m_id]
    estilo = "mesa-box mesa-ocupada" if info["ocupada"] else "mesa-box"
    txt = info['nome'] if info["ocupada"] else "DISPONÍVEL"
    
    col.markdown(f'<div class="{estilo}"><b>MESA {m_id}</b><br><small>{MESAS[m_id]}</small><br>{txt}</div>', unsafe_allow_html=True)
    
    if not info["ocupada"]:
        if col.button(f"SENTAR {m_id}", key=f"s{m_id}"):
            if nome_reserva:
                st.session_state.sala[m_id] = {"ocupada": True, "nome": f"{nome_reserva} ({pax_reserva}p)"}
                st.rerun()
            else: st.warning("Insira o nome na lateral")
    else:
        if col.button(f"LIBERTAR {m_id}", key=f"l{m_id}"):
            st.session_state.sala[m_id] = {"ocupada": False, "nome": ""}
            st.rerun()

# Organização em Colunas Reais
c1, c2, c3, c_janela = st.columns([1, 1, 1, 0.2])

with c1: # Lado Esquerdo (Parede)
    for m in [11, 10, 9, 8, 7]: render_mesa(m, c1)

with c2: # Centro
    render_mesa(12, c2)
    render_mesa(19, c2)
    render_mesa(20, c2)
    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
    render_mesa(6, c2)
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    render_mesa(4, c2) # Mesa 4 isolada em baixo

with c3: # Lado Direito (Escadas e Janela)
    for m in [14, 16, 17, 18]: render_mesa(m, c3)
    st.markdown("<div class='escadas'>ESCADAS</div><br>", unsafe_allow_html=True)
    for m in [1, 2, 3]: render_mesa(m, c3)

with c_janela: # Rótulo da Janela
    st.markdown("<div class='janela-label'><br><br>JANELA</div>", unsafe_allow_html=True)

st.write("---")
if st.button("LIMPAR TURNO"):
    st.session_state.sala = {m: {"ocupada": False, "nome": ""} for m in MESAS}
    st.rerun()
