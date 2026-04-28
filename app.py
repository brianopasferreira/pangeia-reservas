import streamlit as st
from datetime import datetime, time

# 1. Configuração de Luxo
st.set_page_config(page_title="Pangeia Nazaré - Gestão de Sala", layout="wide")

st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%);
        color: #D4AF37; font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }
    .main-title {
        color: #D4AF37; text-align: center; font-size: 2.2em; font-weight: 800;
        letter-spacing: 7px; margin-bottom: 25px; text-transform: uppercase;
    }
    .mesa-container {
        border: 1px solid rgba(212, 175, 55, 0.25);
        padding: 12px; border-radius: 10px; text-align: center; margin-bottom: 8px;
        background: rgba(255, 255, 255, 0.02); transition: 0.3s;
    }
    .mesa-ocupada { 
        background: linear-gradient(145deg, #D4AF37, #B8860B) !important;
        color: #000 !important; border: none; font-weight: bold;
    }
    .label-zona { opacity: 0.4; letter-spacing: 2px; font-size: 0.7em; text-align: center; margin-top: 10px; margin-bottom: 10px; color: #D4AF37; }
    .stButton>button { border-radius: 4px; font-weight: bold; height: 2.2em; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# 2. Definição das Mesas e Capacidades
MESAS_CAP = {
    1: "2pax", 2: "4-7pax", 3: "3pax", 4: "4-7pax", 6: "2pax", 7: "4-6pax",
    8: "4-6pax", 9: "4-6pax", 10: "2pax", 11: "2pax", 12: "2pax", 14: "2pax",
    16: "4-7pax", 17: "4-7pax", 18: "2-3pax", 19: "2pax", 20: "2pax"
}

if 'sala' not in st.session_state:
    st.session_state.sala = {m: {"ocupada": False, "detalhes": ""} for m in MESAS_CAP}

# --- SIDEBAR: REGRAS PANGEIA ---
with st.sidebar:
    st.markdown("### ✍️ RESERVA")
    data_sel = st.date_input("Data", datetime.now())
    bloqueio = data_sel.weekday() == 0 # Segunda-feira
    
    if bloqueio:
        st.error("FECHADO À SEGUNDA")
    else:
        turno = st.selectbox("Turno", ["Almoço (12h-15h)", "Jantar (19h-22h)"])
        lim = (time(12,0), time(15,0)) if "Almoço" in turno else (time(19,0), time(22,0))
        hora_sel = st.slider("Hora", lim[0], lim[1], lim[0])
        pax_sel = st.number_input("Pessoas", 1, 20, 2)
        nome_sel = st.text_input("Nome Cliente")

# --- CONTEÚDO PRINCIPAL ---
st.markdown("<div class='main-title'>PANGEIA NAZARÉ</div>", unsafe_allow_html=True)

if not bloqueio:
    def render_mesa(m_id, coluna):
        info = st.session_state.sala[m_id]
        classe = "mesa-ocupada" if info["ocupada"] else ""
        cor_txt = "#000" if info["ocupada"] else "#D4AF37"
        
        coluna.markdown(f"""
            <div class="mesa-container {classe}">
                <div style="font-size: 1em; font-weight: bold;">MESA {m_id}</div>
                <div style="font-size: 0.7em; opacity: 0.6;">{MESAS_CAP[m_id]}</div>
                <div style="font-size: 0.8em; margin-top:4px; color: {cor_txt}; min-height: 20px;">
                    {info['detalhes'] if info['ocupada'] else "LIVRE"}
