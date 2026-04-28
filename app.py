import streamlit as st
from datetime import datetime

# 1. Configuração e Estética
st.set_page_config(page_title="Pangeia Nazaré", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; }
    [data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #D4AF37; }
    .mesa { border: 1px solid #D4AF37; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 5px; background: rgba(212,175,55,0.05); min-height: 80px; }
    .ocupada { background: #D4AF37 !important; color: #000 !important; font-weight: bold; }
    .nota-display { font-size: 0.75em; color: #888; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# 2. Definição das Mesas
MESAS_INFO = {1:"2p", 2:"4-7p", 3:"2p", 4:"4-7p", 6:"2p", 7:"2p", 8:"4-6p", 9:"4-6p", 10:"2p", 11:"2p", 12:"2p", 14:"2p", 16:"4-7p", 17:"4-7p", 18:"2-3p", 19:"2p", 20:"2p"}

# 3. Inicialização de Memória (Proteção total contra KeyError)
if 'sala' not in st.session_state:
    st.session_state.sala = {
        "Almoço": {m: {"ocupada": False, "info": "", "nota": ""} for m in MESAS_INFO},
        "Jantar": {m: {"ocupada": False, "info": "", "nota": ""} for m in MESAS_INFO}
    }

# --- SIDEBAR ---
with st.sidebar:
    st.title("RESERVA")
    data_sel = st.date_input("Data", datetime.now())
    dia_semana = data_sel.weekday() 
    
    bloqueio = False
    if dia_semana == 0:
        st.error("Restaurante Encerrado à Segunda")
        bloqueio = True
    else:
        turno_sel = st.selectbox("Turno", ["Almoço", "Jantar"])
        
        if dia_semana == 6 and turno_sel == "Jantar":
            st.error("Encerrado Domingo ao Jantar")
            bloqueio = True
        else:
            if turno_sel == "Almoço":
                horas = [f"{h:02d}:{m:02d}" for h in range(12, 16) for m in [0, 15, 30, 45] if (h == 12 and m >= 30) or (h == 13) or (h == 14) or (h == 15 and m == 0)]
            else:
                horas = [f"{h:02d}:{m:02d}" for h in range(19, 23) for m in [0, 15, 30, 45] if (h >= 19 and h <= 22)]

            hora_sel = st.selectbox("Hora", horas)
            nome_res = st.text_input("Nome Cliente")
            pax_res = st.number_input("Pessoas", 1, 20, 2)
            nota_res = st.text_area("Notas / Observações")

# --- FUNÇÃO DE RENDERIZAÇÃO CORRIGIDA ---
def render_mesa(m_id, col, turno):
    # Verificação de segurança para garantir que os dados existem
    if turno in st.session_state.sala and m_id in st.session_state.sala[turno]:
        m = st.session_state.sala[turno][m_id]
        classe = "mesa ocupada" if m["ocupada"] else "mesa"
        txt = f"<b>M{m_id}</b><br><small>{MESAS_INFO[m_id]}</small>"
        
        if m["ocupada"]:
            txt += f"<br>{m['info']}<br><span class='nota-display'>{m['nota']}</span>"
        else:
            txt += "<br>LIVRE"
        
        col.markdown(f"<div class='{classe}'>{txt}</div>", unsafe_allow_html=True)
        
        # Lógica de botões protegida
        if not m["ocupada"]:
            if not bloqueio:
                if col.button(f"SENTAR {m_id}", key=f"s{m_id}_{turno}"):
                    if nome_res:
                        info_txt = f"{nome_res} ({pax_res}p) @ {hora_sel}"
                        st.session_state.sala[turno][m_id] = {"ocupada": True, "info": info_txt, "nota": nota_res}
                        st.rerun()
                    else:
                        st.error("Nome obrigatório")
        else:
            if col.button(f"LIBERTAR {m_id}", key=f"l{m_id}_{turno}"):
                st.session_state.sala[turno][m_id] = {"ocupada": False, "info": "", "nota": ""}
                st.rerun()

# --- MAPA DA SALA ---
st.markdown(f"<h2 style='text-align:center; color:#D4AF37;'>PANGEIA NAZARÉ - {turno_sel.upper() if not bloqueio else ''}</h2>", unsafe_allow_html=True)

if not bloqueio:
    c1, c2, c3 = st.columns(3)

    with c1: # ALA MAR
        st.markdown("<h4 style='text-align:center;'>ALA MAR</h4>", unsafe_allow_html=True)
        for mid in [11, 10, 9, 8]:
            render_mesa(mid, c1, turno_sel)
        st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True) 
        render_mesa(7, c1, turno_sel) 

    with c2: # CENTRO
        st.markdown("<h4 style='text-align:center;'>CENTRO</h4>", unsafe_allow_html=True)
        for mid in [12, 19, 20]:
            render_mesa(mid, c2, turno_sel)
        st.markdown("<div style='height:200px;'></div>", unsafe_allow_html=True) 
        render_mesa(6, c2, turno_sel) 
        render_mesa(4, c2, turno_sel) 

    with c3: # JANELA
        st.markdown("<h4 style='text-align:center;'>JANELA</h4>", unsafe_allow_html=True)
        for mid in [14, 16, 17, 18]:
            render_mesa(mid, c3, turno_sel)
        st.markdown("<div style='text-align:center; border:1px dashed #444; margin:10px 0; color:#888;'>ESCADAS</div>", unsafe_allow_html=True)
        render_mesa(1, c3, turno_sel)
        render_mesa(2, c3, turno_sel) 
        render_mesa(3, c3, turno_sel)

st.write("---")
if not bloqueio:
    if st.button("LIMPAR TURNO ATUAL"):
        st.session_state.sala[turno_sel] = {m: {"ocupada": False, "info": "", "nota": ""} for m in MESAS_INFO}
        st.rerun()
