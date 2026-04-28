import streamlit as st
from datetime import datetime, time

# 1. Configuração e Estética
st.set_page_config(page_title="Pangeia Nazaré", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; }
    [data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #D4AF37; }
    .mesa { border: 1px solid #D4AF37; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 5px; background: rgba(212,175,55,0.05); }
    .ocupada { background: #D4AF37 !important; color: #000 !important; font-weight: bold; }
    .nota-display { font-size: 0.75em; color: #888; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dados das Mesas
MESAS_INFO = {1:"2p", 2:"4-7p", 3:"2p", 4:"4-7p", 6:"2p", 7:"2p", 8:"4-6p", 9:"4-6p", 10:"2p", 11:"2p", 12:"2p", 14:"2p", 16:"4-7p", 17:"4-7p", 18:"2-3p", 19:"2p", 20:"2p"}

if 'sala' not in st.session_state:
    st.session_state.sala = {m: {"ocupada": False, "info": "", "nota": ""} for m in MESAS_INFO}

# --- SIDEBAR ---
with st.sidebar:
    st.title("RESERVA")
    data_sel = st.date_input("Data", datetime.now())
    dia_semana = data_sel.weekday() 
    
    bloqueio = False
    if dia_semana == 0:
        st.error("ENCERRADO À SEGUNDA")
        bloqueio = True
    else:
        turno = st.selectbox("Turno", ["Almoço", "Jantar"])
        
        if dia_semana == 6 and turno == "Jantar":
            st.error("ENCERRADO DOMINGO AO JANTAR")
            bloqueio = True
        else:
            # GERADOR DINÂMICO DE HORAS
            if turno == "Almoço":
                # Lista de 12:30 até 15:00
                horas_disponiveis = [f"{h:02d}:{m:02d}" for h in range(12, 16) for m in [0, 15, 30, 45] if (h == 12 and m >= 30) or (h == 13) or (h == 14) or (h == 15 and m == 0)]
            else:
                # Lista de 19:00 até 22:30
                horas_disponiveis = [f"{h:02d}:{m:02d}" for h in range(19, 23) for m in [0, 15, 30, 45] if (h >= 19 and h <= 22)]

            hora_sel = st.selectbox("Hora da Reserva", horas_disponiveis)
            
            nome_res = st.text_input("Nome Cliente")
            pax_res = st.number_input("Pessoas", 1, 20, 2)
            nota_res = st.text_area("Notas / Observações")

def render_mesa(m_id, col):
    m = st.session_state.sala[m_id]
    classe = "mesa ocupada" if m["ocupada"] else "mesa"
    txt = f"<b>M{m_id}</b><br><small>{MESAS_INFO[m_id]}</small>"
    if m["ocupada"]:
        txt += f"<br>{m['info']}<br><span class='nota-display'>{m['nota']}</span>"
    else:
        txt += "<br>LIVRE"
    
    col.markdown(f"<div class='{classe}'>{txt}</div>", unsafe_allow_html=True)
    
    if not m["ocupada"] and not bloqueio:
        if col.button(f"SENTAR {m_id}", key=f"s{m_id}"):
            if nome_res:
                info_pax = f"{nome_res} ({pax_res}p) @ {hora_sel}"
                st.session_state.sala[m_id] = {"ocupada": True, "info": info_pax, "nota": nota_res}
                st.rerun()
            else: st.error("Falta o nome!")
    elif m["ocupada"]:
        if col.button(f"LIBERTAR {m_id}", key=f"l{m_id}"):
            st.session_state.sala[m_id] = {"ocupada": False, "info": "", "nota": ""}
            st.rerun()

# --- LAYOUT GEOMÉTRICO (MANTIDO) ---
st.markdown("<h2 style='text-align:center;'>PANGEIA NAZARÉ</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1: # ALA MAR
    st.caption("ALA MAR")
    for m in [11, 10, 9, 8]: render_mesa(m, c1)
    st.markdown("<div style='height:55px;'></div>", unsafe_allow_html=True) 
    render_mesa(7, c1) 

with c2: # CENTRO
    st.caption("CENTRO")
    for m in [12, 19, 20]: render_mesa(m, c2)
    st.markdown("<div style='height:210px;'></div>", unsafe_allow_html=True) 
    render_mesa(6, c2) 
    render_mesa(4, c2) 

with c3: # JANELA
    st.caption("JANELA")
    for m in [14, 16, 17, 18]: render_mesa(m, c3)
    st.markdown("<div style='text-align:center;border:1px dashed #444;margin:10px 0;font-size:0.7em;'>ESCADAS</div>", unsafe_allow_html=True)
    render_mesa(1, c3)
    render_mesa(2, c3) 
    render_mesa(3, c3)

st.write("---")
if st.button("LIMPAR TUDO"):
    st.session_state.sala = {m: {"ocupada": False, "info": "", "nota": ""} for m in MESAS_INFO}
    st.rerun()
