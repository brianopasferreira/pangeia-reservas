import streamlit as st
from datetime import datetime

# 1. Configuração e Estética Premium Pangeia
st.set_page_config(page_title="Pangeia Nazaré - Gestão VIP", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    /* Fundo com Gradiente para dar "Vida" */
    .stApp { 
        background: radial-gradient(circle, #1a1a1a 0%, #050505 100%);
        color: #D4AF37; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Títulos com brilho suave */
    h1, h2, h3 { 
        color: #D4AF37 !important; 
        text-align: center; 
        text-transform: uppercase; 
        letter-spacing: 3px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Cartões das Mesas - Mais modernos */
    .mesa-container {
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 15px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        transition: transform 0.2s, border 0.2s;
    }
    .mesa-container:hover {
        border: 1px solid #D4AF37;
        transform: translateY(-2px);
    }
    
    /* Estados da Mesa */
    .mesa-ocupada { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important; 
        color: #000 !important; 
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    
    /* Botões Premium */
    .stButton>button { 
        background-color: #D4AF37; 
        color: black; 
        font-weight: bold; 
        width: 100%; 
        border-radius: 8px; 
        border: none; 
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #fff; 
        box-shadow: 0 0 15px #D4AF37;
    }

    /* Estilo Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0c0c0c;
        border-right: 1px solid #D4AF37;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Dados das Mesas
MESAS = {
    1: "2pax", 2: "4-7pax", 3: "3pax", 4: "4-7pax", 6: "2pax", 7: "4-6pax",
    8: "4-6pax", 9: "4-6pax", 10: "2pax", 11: "2pax", 12: "2pax", 14: "2pax",
    16: "4-7pax", 17: "4-7pax", 18: "2-3pax", 19: "2pax", 20: "2pax"
}

if 'sala' not in st.session_state:
    st.session_state.sala = {m: {"ocupada": False, "detalhes": ""} for m in MESAS}

# --- SIDEBAR: REGISTO DE RESERVA ---
with st.sidebar:
    st.markdown("### 📅 Nova Reserva")
    nome_reserva = st.text_input("Nome do Cliente")
    pax_reserva = st.number_input("Nº de Pessoas", min_value=1, value=2)
    data_reserva = st.date_input("Data", datetime.now())
    hora_reserva = st.time_input("Horário", datetime.now())
    
    info_formatada = f"{nome_reserva} | {pax_reserva}pax | {hora_reserva.strftime('%H:%M')}"

st.markdown("<h1>🔱 PANGEIA NAZARÉ</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Gestão de Sala - {data_reserva.strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)

# 3. Layout de Sala
col1, col2, col3 = st.columns([1, 1, 1])

def render_mesa(m_id, coluna):
    info = st.session_state.sala[m_id]
    classe = "mesa-ocupada" if info["ocupada"] else ""
    txt_cor = "#000" if info["ocupada"] else "#D4AF37"
    
    coluna.markdown(f"""
        <div class="mesa-container {classe}">
            <div style="font-size: 1.3em; font-weight: bold;">Mesa {m_id}</div>
            <div style="font-size: 0.8em; opacity: 0.7;">Capacidade: {MESAS[m_id]}</div>
            <div style="margin-top: 10px; font-weight: bold; color: {txt_cor};">
                {info['detalhes'] if info['ocupada'] else "Disponível"}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if not info["ocupada"]:
        if coluna.button(f"OCUPAR M{m_id}", key=f"btn{m_id}"):
            if nome_reserva:
                st.session_state.sala[m_id] = {"ocupada": True, "detalhes": info_formatada}
                st.rerun()
            else:
                st.error("Preencha o nome na lateral!")
    else:
        if coluna.button(f"LIBERTAR M{m_id}", key=f"btn{m_id}"):
            st.session_state.sala[m_id] = {"ocupada": False, "detalhes": ""}
            st.rerun()

# --- Distribuição das Colunas (Igual ao teu desenho) ---
with col1:
    st.markdown("### Ala Mar")
    for m in [12, 11, 10, 9, 8]: render_mesa(m, col1)
    st.markdown("<div style='border:1px dashed #444; padding:15px; text-align:center; color:#666;'>🎹 PIANO</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### Centro")
    for m in [19, 20, 6, 7, 4]: render_mesa(m, col2)

with col3:
    st.markdown("### Ala Entrada")
    for m in [14, 16, 17, 18]: render_mesa(m, col3)
    st.markdown("<div style='border:1px dashed #444; padding:15px; text-align:center; color:#666;'>🪜 ESCADAS</div>", unsafe_allow_html=True)
    for m in [1, 2, 3]: render_mesa(m, col3)

st.write("---")
if st.button("LIMPAR TURNO"):
    st.session_state.sala = {m: {"ocupada": False, "detalhes": ""} for m in MESAS}
    st.rerun()
