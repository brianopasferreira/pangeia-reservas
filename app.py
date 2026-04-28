import streamlit as st
from datetime import datetime, time

# Configurações iniciais
st.set_page_config(page_title="Pangeia Nazaré", layout="wide")

# Estilos CSS simplificados para evitar erros de sintaxe
st.markdown("<style>.stApp{background-color:#050505;color:#D4AF37;}.mesa{border:1px solid #D4AF37;padding:10px;border-radius:5px;text-align:center;margin-bottom:5px;background:rgba(212,175,55,0.05);}.ocupada{background:#D4AF37 !important;color:#000 !important;font-weight:bold;}</style>", unsafe_allow_html=True)

# Dados das Mesas
MESAS = {1:"2p", 2:"4-7p", 3:"2p", 4:"4-7p", 6:"2p", 7:"2p", 8:"4-6p", 9:"4-6p", 10:"2p", 11:"2p", 12:"2p", 14:"2p", 16:"4-7p", 17:"4-7p", 18:"2-3p", 19:"2p", 20:"2p"}

if 'sala' not in st.session_state:
    st.session_state.sala = {m: {"ocupada": False, "nome": ""} for m in MESAS}

# Sidebar
with st.sidebar:
    st.title("RESERVA")
    data = st.date_input("Data", datetime.now())
    if data.weekday() == 0: st.error("FECHADO À SEGUNDA")
    nome = st.text_input("Nome")
    pax = st.number_input("Pax", 1, 20, 2)

# Função para desenhar mesa
def desenhar(m_id, col):
    m = st.session_state.sala[m_id]
    classe = "mesa ocupada" if m["ocupada"] else "mesa"
    info = m["nome"] if m["ocupada"] else "LIVRE"
    col.markdown(f"<div class='{classe}'>M{m_id}<br><small>{MESAS[m_id]}</small><br>{info}</div>", unsafe_allow_html=True)
    if not m["ocupada"]:
        if col.button(f"SENTAR M{m_id}", key=f"s{m_id}"):
            if nome:
                st.session_state.sala[m_id] = {"ocupada": True, "nome": f"{nome} ({pax}p)"}
                st.rerun()
            else: st.error("Falta nome")
    else:
        if col.button(f"LIMPAR M{m_id}", key=f"l{m_id}"):
            st.session_state.sala[m_id] = {"ocupada": False, "nome": ""}
            st.rerun()

st.markdown("<h2 style='text-align:center;'>PANGEIA NAZARÉ</h2>", unsafe_allow_html=True)

# Layout da Sala baseado no teu desenho
c1, c2, c3 = st.columns(3)

with c1: # ALA MAR
    st.caption("ALA MAR")
    for m in [11, 10, 9, 8]: desenhar(m, c1)
    st.markdown("<div style='height:35px'></div>", unsafe_allow_html=True) # Espaço para alinhar 7 com 6
    desenhar(7, c1)

with c2: # CENTRO
    st.caption("CENTRO")
    for m in [12, 19, 20]: desenhar(m, c2)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    desenhar(6, c2) # Alinhada com a 7
    st.markdown("<div style='height:105px'></div>", unsafe_allow_html=True) # Espaço para alinhar 4 com 2
    desenhar(4, c2) # Alinhada com a 2

with c3: # JANELA
    st.caption("JANELA")
    for m in [14, 16, 17, 18]: desenhar(m, c3)
    st.markdown("<div style='text-align:center;border:1px dashed #444;margin:10px 0;'>ESCADAS</div>", unsafe_allow_html=True)
    desenhar(1, c3)
    desenhar(2, c3) # Alinhada com a 4
    desenhar(3, c3)
