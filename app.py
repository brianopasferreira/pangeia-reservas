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

# 2. Definição das Mesas
MESAS_CAP = {
    1: "2pax", 2: "4-7pax", 3: "3pax", 4: "4-7pax", 6: "2pax", 7: "4-6pax",
    8: "4-6pax", 9: "4-6pax", 10: "2pax", 11: "2pax", 12: "2pax", 14: "2pax",
    16: "4-7pax", 17: "4-7pax", 18: "2-3pax", 19: "2pax", 20: "2pax"
}

if 'sala' not in st.session_state:
    st.session_state.sala = {m: {"ocupada": False, "detalhes": ""} for m in MESAS_CAP}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ✍️ RESERVA")
    data_sel = st.date_input("Data", datetime.now())
    bloqueio = data_sel.weekday() == 0
    if bloqueio:
        st.error("FECHADO À SEGUNDA")
    else:
        turno = st.selectbox("Turno", ["Almoço (12h-15h)", "Jantar (19h-22h)"])
        lim = (time(12,0), time(15,0)) if "Almoço" in turno else (time(19,0), time(22,0))
        hora_sel = st.slider("Hora", lim[0], lim[1], lim[0])
        pax_sel = st.number_input("Pessoas", 1, 20, 2)
        nome_sel = st.text_input("Nome Cliente")

# --- CONTEÚDO ---
st.markdown("<div class='main-title'>PANGEIA NAZARÉ</div>", unsafe_allow_html=True)

if not bloqueio:
    def render_mesa(m_id, coluna):
        info = st.session_state.sala[m_id]
        classe = "mesa-ocupada" if info["ocupada"] else ""
        cor_txt = "#000" if info["ocupada"] else "#D4AF37"
        coluna.markdown(f"""<div class="mesa-container {classe}">
            <div style="font-size: 1em; font-weight: bold;">MESA {m_id}</div>
            <div style="font-size: 0.7em; opacity: 0.6;">{MESAS_CAP[m_id]}</div>
            <div style="font-size: 0.8em; margin-top:4px; color: {cor_txt};">{info['detalhes'] if info['ocupada'] else "LIVRE"}</div>
            </div>""", unsafe_allow_html=True)
        if not info["ocupada"]:
            if coluna.button(f"SENTAR M{m_id}", key=f"b{m_id}"):
                if nome_sel:
                    st.session_state.sala[m_id] = {"ocupada": True, "detalhes": f"{nome_sel} ({pax_sel}p)"}
                    st.rerun()
                else: st.error("Nome?")
        else:
            if coluna.button(f"LIBERTAR M{m_id}", key=f"b{m_id}"):
                st.session_state.sala[m_id] = {"ocupada": False, "detalhes": ""}
                st.rerun()

    # Layout de 3 Colunas com as novas regras de paralelismo
    c1, c2, c3 = st.columns(3)

    # COLUNA 1: ALA MAR (Reordenada: 12 no topo, depois 11 a 7 descendo)
    with c1:
        st.markdown("<div class='label-zona'>ALA MAR / JANELA</div>", unsafe_allow_html=True)
        render_mesa(12, c1)
        for m in [11, 10, 9, 8, 7]: render_mesa(m, c1)

    # COLUNA 2: CENTRO (Mesa 19 e 20 nos lugares da 6 e 7 + Piano paralelo à 4)
    with c2:
        st.markdown("<div class='label-zona'>CENTRO</div>", unsafe_allow_html=True)
        render_mesa(19, c2) # Ocupa lugar da antiga 6
        render_mesa(20, c2) # Ocupa lugar da antiga 7
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div style='border:1px solid #444; padding:10px; text-align:center; font-size:0.7em;'>🎹 PIANO</div>", unsafe_allow_html=True)
        render_mesa(4, c2)  # Paralela ao Piano

    # COLUNA 3: ALA ENTRADA (Mesa 14 topo, 6 paralela à 1, 4 paralela à 2)
    with c3:
        st.markdown("<div class='label-zona'>ALA ENTRADA</div>", unsafe_allow_html=True)
        render_mesa(14, c3)
        render_mesa(16, c3)
        render_mesa(17, c3)
        render_mesa(18, c3)
        st.markdown("<div style='text-align:center; font-size:0.7
