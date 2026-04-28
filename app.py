import streamlit as st
from datetime import datetime, time

# 1. Configuração Visual e Estética
st.set_page_config(page_title="Pangeia Nazaré - Gestão", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #D4AF37; }
    .mesa-box {
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 15px; border-radius: 8px; text-align: center;
        background: rgba(255, 255, 255, 0.02); margin-bottom: 10px;
        min-height: 105px;
    }
    .mesa-ocupada { 
        background: linear-gradient(145deg, #D4AF37, #B8860B) !important;
        color: #000 !important; font-weight: bold; border: none;
    }
    .label-zona { color: #444; font-size: 0.7em; text-align: center; letter-spacing: 3px; margin-bottom: 10px; }
    .escadas { background: #111; border: 1px dashed #444; padding: 15px; text-align: center; color: #555; font-size: 0.7em; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Dados das Mesas
MESAS_INFO = {
    1: "2p", 2: "4-7p", 3: "2p", 4: "4-7p", 6: "2p", 7: "2p", 8: "4-6p", 
    9: "4-6p", 10: "2p", 11: "2p", 12: "2p", 14: "2p", 16: "4-7p", 
    17: "4-7p", 18: "2-3p", 19: "2p", 20: "2p"
}

if 'sala' not in st.session_state:
    st.session_state.sala = {m: {"ocupada": False, "nome": ""} for m in MESAS_INFO}

# --- SIDEBAR: REGRAS DE FUNCIONAMENTO ---
with st.sidebar:
    st.title("RESERVA")
    data_sel = st.date_input("Data", datetime.now())
    
    # Regra: Segunda-feira Fechado
    bloqueio = data_sel.weekday() == 0 
    
    if bloqueio:
        st.error("FECHADO À SEGUNDA")
    else:
        turno = st.selectbox("Turno", ["Almoço (12:00-15:00)", "Jantar (19:00-22:00)"])
        # Limitação de horários conforme solicitado
        h_lim = (time(12,0), time(15,0)) if "Almoço" in turno else (time(19,0), time(22,0))
        hora_sel = st.slider("Hora", h_lim[0], h_lim[1], h_lim[0])
        
        nome_reserva = st.text_input("Nome Cliente")
        pax_reserva = st.number_input("Nº Pessoas", 1, 20, 2)

# --- FUNÇÃO DE RENDERIZAÇÃO ---
def exibir_mesa(m_id, col):
    info = st.session_state.sala[m_id]
    estilo = "mesa-box mesa-ocupada" if info["ocupada"] else "mesa-box"
    status = info['nome'] if info["ocupada"] else "LIVRE"
    
    col.markdown(f'<div class="{estilo}"><b>M{m_id}</b><br><small>{MESAS_INFO[m_id]}</small><br>{status}</div>', unsafe_allow_html=True)
    
    if not info["ocupada"]:
        if col.button(f"SENTAR M{m_id}", key=f"s{m_id}"):
            if not bloqueio and nome_reserva:
                st.session_state.sala[m_id] = {"ocupada": True, "nome": f"{nome_reserva} ({pax_reserva}p)"}
                st.rerun()
            elif not nome_reserva: st.sidebar.error("Insira o nome!")
    else:
        if col.button(f"LIBERTAR M{m_id}", key=f"l{m_id}"):
            st.session_state.sala[m_id] = {"ocupada": False, "nome": ""}
            st.rerun()

# --- MAPA DE SALA (ALINHAMENTOS CONFORME DESENHO) ---
st.markdown("<h2 style='text-align:center; letter-spacing:5px;'>PANGEIA NAZARÉ</h2>", unsafe_allow_html=True)

if not bloqueio:
    col_esq, col_meio, col_dir = st.columns(3)

    with col_esq: # PAREDE ESQUERDA
        st.markdown("<div class='label-zona'>PAREDE</div>", unsafe_allow_html=True)
        for m in [11, 10, 9, 8]: exibir_mesa(m, col_esq)
        st.markdown("<div style='height:45px;'></div>", unsafe_allow_html=True) # Alinhamento para a 7
        exibir_mesa(7, col_esq) 

    with col_meio: # CENTRO
        st.markdown("<div class='label-zona'>CENT
