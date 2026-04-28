import streamlit as st
from datetime import datetime

# 1. Configuração e Estética
st.set_page_config(page_title="Pangeia Nazaré", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; }
    [data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #D4AF37; }
    .mesa { border: 1px solid #D4AF37; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 5px; background: rgba(212,175,55,0.05); min-height: 85px; }
    .ocupada { background: #D4AF37 !important; color: #000 !important; font-weight: bold; }
    .nota-display { font-size: 0.75em; color: #888; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# 2. Definição das Mesas
MESAS_INFO = {1:"2p", 2:"4-7p", 3:"2p", 4:"4-7p", 6:"2p", 7:"2p", 8:"4-6p", 9:"4-6p", 10:"2p", 11:"2p", 12:"2p", 14:"2p", 16:"4-7p", 17:"4-7p", 18:"2-3p", 19:"2p", 20:"2p"}

# 3. Inicialização de Memória Independente
if 'sala' not in st.session_state:
    st.session_state.sala = {
        "Almoço": {m: {"ocupada": False, "info": "", "nota": ""} for m in MESAS_INFO},
        "Jantar": {m: {"ocupada": False, "info": "", "nota": ""} for m in MESAS_INFO}
    }

# --- SIDEBAR (Dados da Reserva) ---
with st.sidebar:
    st.title("NOVA RESERVA")
    data_sel = st.date_input("Data", datetime.now())
    
    if data_sel.weekday() == 0: # Segunda-feira
        st.error("Restaurante Encerrado")
        bloqueio_geral = True
    else:
        bloqueio_geral = False
        nome_res = st.text_input("Nome Cliente")
        pax_res = st.number_input("Pessoas", 1, 20, 2)
        nota_res = st.text_area("Notas")

# --- FUNÇÃO DE RENDERIZAÇÃO ---
def render_mesa(m_id, col, turno, h_sel):
    m = st.session_state.sala[turno][m_id]
    classe = "mesa ocupada" if m["ocupada"] else "mesa"
    txt = f"<b>M{m_id}</b><br><small>{MESAS_INFO[m_id]}</small>"
    
    if m["ocupada"]:
        txt += f"<br>{m['info']}<br><span class='nota-display'>{m['nota']}</span>"
    else:
        txt += "<br>LIVRE"
    
    col.markdown(f"<div class='{classe}'>{txt}</div>", unsafe_allow_html=True)
    
    if not m["ocupada"] and not bloqueio_geral:
        if col.button(f"SENTAR M{m_id}", key=f"s{m_id}_{turno}"):
            if nome_res:
                st.session_state.sala[turno][m_id] = {
                    "ocupada": True, 
                    "info": f"{nome_res} ({pax_res}p) @ {h_sel}", 
                    "nota": nota_res
                }
                st.rerun()
            else:
                st.error("Insira o nome")
    elif m["ocupada"]:
        if col.button(f"LIBERTAR M{m_id}", key=f"l{m_id}_{turno}"):
            st.session_state.sala[turno][m_id] = {"ocupada": False, "info": "", "nota": ""}
            st.rerun()

# --- INTERFACE PRINCIPAL COM SEPARADORES ---
st.title("PANGEIA NAZARÉ")

tab_almoco, tab_jantar = st.tabs(["🍽️ ALMOÇO", "🌙 JANTAR"])

# --- CONTEÚDO ALMOÇO ---
with tab_almoco:
    h_almoco = st.selectbox("Hora Almoço", [f"{h:02d}:{m:02d}" for h in range(12, 16) for m in [0, 15, 30, 45] if (h==12 and m>=30) or (h<15) or (h==15 and m==0)], key="h_alm")
    
    c1, c2, c3 = st.columns(3)
    with c1: # ALA MAR
        for mid in [11, 10, 9, 8]: render_mesa(mid, c1, "Almoço", h_almoco)
        st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)
        render_mesa(7, c1,
