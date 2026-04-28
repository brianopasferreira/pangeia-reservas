import streamlit as st
from datetime import datetime, time

# 1. Configuração Premium
st.set_page_config(page_title="Pangeia Nazaré", layout="wide")

# CSS: Fundo Gradiente Carbono e Design de Cartões
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle, #1e1e1e 0%, #000000 100%);
        color: #D4AF37; 
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }
    
    .main-title {
        color: #D4AF37; text-align: center; font-size: 2.8em; font-weight: 800;
        letter-spacing: 8px; margin-bottom: 20px; text-transform: uppercase;
    }
    
    .mesa-container {
        border: 1px solid rgba(212, 175, 55, 0.4);
        padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;
        background: rgba(255, 255, 255, 0.03); transition: 0.3s;
    }
    .mesa-ocupada { 
        background: linear-gradient(145deg, #D4AF37, #B8860B) !important;
        color: #000 !important; border: none; font-weight: bold;
    }
    
    .stButton>button { border-radius: 4px; font-weight: bold; }
    .label-zona { opacity: 0.5; letter-spacing: 3px; font-size: 0.8em; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Definição das Mesas
MESAS = {
    1: "2pax", 2: "4-7pax", 3: "3pax", 4: "4-7pax", 6: "2pax", 7: "4-6pax",
    8: "4-6pax", 9: "4-6pax", 10: "2pax", 11: "2pax", 12: "2pax", 14: "2pax",
    16: "4-7pax", 17: "4-7pax", 18: "2-3pax", 19: "2pax", 20: "2pax"
}

if 'sala' not in st.session_state:
    st.session_state.sala = {m: {"ocupada": False, "detalhes": ""} for m in MESAS}

# --- SIDEBAR: REGRAS DE NEGÓCIO ---
with st.sidebar:
    st.markdown("### GESTÃO DE RESERVA")
    data_sel = st.date_input("Data", datetime.now())
    
    # Validação Segunda-feira
    if data_sel.weekday() == 0:
        st.error("RESTAURANTE FECHADO")
        bloqueio = True
    else:
        bloqueio = False
        turno = st.selectbox("Turno", ["Almoço (12h-15h)", "Jantar (19h-22h)"])
        limites = (time(12, 0), time(15, 0)) if "Almoço" in turno else (time(19, 0), time(22, 0))
        hora_sel = st.slider("Hora", limites[0], limites[1], limites[0])
        pax_sel = st.number_input("Pessoas", 1, 20, 2)
        nome_sel = st.text_input("Nome Cliente")

# --- INTERFACE PRINCIPAL ---
st.markdown("<div class='main-title'>PANGEIA NAZARÉ</div>", unsafe_allow_html=True)

if bloqueio:
    st.warning("O restaurante encerra às segundas-feiras para descanso semanal.")
else:
    st.markdown(f"<p style='text-align:center; opacity:0.6;'>{data_sel.strftime('%d/%m/%Y')} | {hora_sel.strftime('%H:%M')}</p>", unsafe_allow_html=True)

    # Disposição exata da imagem enviada
    col1, col2, col3 = st.columns(3)

    def render_mesa(m_id, coluna):
        info = st.session_state.sala[m_id]
        classe = "mesa-ocupada" if info["ocupada"] else ""
        cor_txt = "#000" if info["ocupada"] else "#D4AF37"
        
        coluna.markdown(f"""
            <div class="mesa-container {classe}">
                <div style="font-size: 1.1em; font-weight: bold;">Mesa {m_id}</div>
                <div style="font-size: 0.7em; opacity: 0.7;">{MESAS[m_id]}</div>
                <div style="font-size: 0.85em; margin-top:5px; color: {cor_txt};">
                    {info['detalhes'] if info['ocupada'] else "DISPONÍVEL"}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if not info["ocupada"]:
            if coluna.button(f"OCUPAR M{m_id}", key=f"b{m_id}"):
                if nome_sel:
                    st.session_state.sala[m_id] = {"ocupada": True, "detalhes": f"{nome_sel} ({pax_sel}p)"}
                    st.rerun()
                else: st.error("Nome?")
        else:
            if coluna.button(f"LIBERTAR M{m_id}", key=f"b{m_id}"):
                st.session_state.sala[m_id] = {"ocupada": False, "detalhes": ""}
                st.rerun()

    with col1:
        st.markdown("<div class='label-zona'>ALA MAR</div>", unsafe_allow_html=True)
        # Ordem da foto (cima para baixo)
        for m in [12, 11, 10, 9, 8]: render_mesa(m, col1)
        st.markdown("<div style='border:1px solid #333; padding:10px; text-align:center; font-size:0.7em;'>🎹 PIANO</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='label-zona'>CENTRO</div>", unsafe_allow_html=True)
        # Ordem da foto (cima para baixo)
        for m in [19, 20, 6, 7, 4]: render_mesa(m, col2)

    with col3:
        st.markdown("<div class='label-zona'>ALA ENTRADA</div>", unsafe_allow_html=True)
        # Ordem da foto (cima para baixo)
        for m in [14, 16, 17, 18]: render_mesa(m, col3)
        st.markdown("<div style='border:1px solid #333; padding:10px; text-align:center; font-size:0.7em;'>🪜 ESCADAS</div>", unsafe_allow_html=True)
        for m in [1, 2, 3]: render_mesa(m, col3)

st.write("---")
if st.button("RESET SALA"):
    st.session_state.sala = {m: {"ocupada": False, "detalhes": ""} for m in MESAS}
    st.rerun()
