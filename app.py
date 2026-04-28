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

# --- SIDEBAR (Dados Comuns da Reserva) ---
with st.sidebar:
    st.title("RESERVA")
    data_sel = st.date_input("Data", datetime.now())
    dia_semana = data_sel.weekday()
    
    bloqueio_segunda = (dia_semana == 0)
    if bloqueio_segunda:
        st.error("ENCERRADO À SEGUNDA")
    
    nome_res = st.text_input("Nome Cliente")
    pax_res = st.number_input("Pessoas", 1, 20, 2)
    nota_res = st.text_area("Observações")

# --- FUNÇÃO DE RENDERIZAÇÃO ---
def render_mesa(m_id, col, turno, hora_texto):
    m = st.session_state.sala[turno][m_id]
    classe = "mesa ocupada" if m["ocupada"] else "mesa"
    txt = f"<b>M{m_id}</b><br><small>{MESAS_INFO[m_id]}</small>"
    
    if m["ocupada"]:
        txt += f"<br>{m['info']}<br><span class='nota-display'>{m['nota']}</span>"
    else:
        txt += "<br>LIVRE"
    
    col.markdown(f"<div class='{classe}'>{txt}</div>", unsafe_allow_html=True)
    
    # Lógica de Botões
    if not m["ocupada"]:
        if not bloqueio_segunda:
            if col.button(f"SENTAR {m_id}", key=f"s{m_id}_{turno}"):
                if nome_res:
                    info_pax = f"{nome_res} ({pax_res}p) @ {hora_texto}"
                    st.session_state.sala[turno][m_id] = {"ocupada": True, "info": info_pax, "nota": nota_res}
                    st.rerun()
                else:
                    st.error("Falta o Nome!")
    else:
        if col.button(f"LIBERTAR {m_id}", key=f"l{m_id}_{turno}"):
            st.session_state.sala[turno][m_id] = {"ocupada": False, "info": "", "nota": ""}
            st.rerun()

# --- INTERFACE COM SEPARADORES ---
st.markdown("<h1 style='text-align:center;'>PANGEIA NAZARÉ</h1>", unsafe_allow_html=True)

# Criação dos dois separadores solicitados
tab_almoco, tab_jantar = st.tabs(["🍽️ ALMOÇO", "🌙 JANTAR"])

# --- CONTEÚDO ALMOÇO ---
with tab_almoco:
    h_alm = st.selectbox("Hora Almoço", [f"{h:02d}:{m:02d}" for h in range(12, 16) for m in [0, 15, 30, 45] if (h==12 and m>=30) or (h<15) or (h==15 and m==0)], key="sel_alm")
    
    c1, c2, c3 = st.columns(3)
    with c1: # ALA MAR
        st.caption("ALA MAR")
        for mid in [11, 10, 9, 8]: render_mesa(mid, c1, "Almoço", h_alm)
        st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)
        render_mesa(7, c1, "Almoço", h_alm)
    with c2: # CENTRO
        st.caption("CENTRO")
        for mid in [12, 19, 20]: render_mesa(mid, c2, "Almoço", h_alm)
        st.markdown("<div style='height:210px;'></div>", unsafe_allow_html=True)
        render_mesa(6, c2, "Almoço", h_alm)
        render_mesa(4, c2, "Almoço", h_alm)
    with c3: # JANELA
        st.caption("JANELA")
        for mid in [14, 16, 17, 18]: render_mesa(mid, c3, "Almoço", h_alm)
        st.markdown("<div style='text-align:center; border:1px dashed #444; margin:10px 0; font-size:0.7em;'>ESCADAS</div>", unsafe_allow_html=True)
        for mid in [1, 2, 3]: render_mesa(mid, c3, "Almoço", h_alm)

    if st.button("LIMPAR TUDO (ALMOÇO)", key="clear_alm"):
        st.session_state.sala["Almoço"] = {m: {"ocupada": False, "info": "", "nota": ""} for m in MESAS_INFO}
        st.rerun()

# --- CONTEÚDO JANTAR ---
with tab_jantar:
    if dia_semana == 6: # Domingo
        st.error("DOMINGO AO JANTAR: ENCERRADO")
    else:
        h_jan = st.selectbox("Hora Jantar", [f"{h:02d}:{m:02d}" for h in range(19, 23) for m in [0, 15, 30, 45] if h<=22], key="sel_jan")
        
        cj1, cj2, cj3 = st.columns(3)
        with cj1: # ALA MAR
            st.caption("ALA MAR")
            for mid in [11, 10, 9, 8]: render_mesa(mid, cj1, "Jantar", h_jan)
            st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)
            render_mesa(7, cj1, "Jantar", h_jan)
        with cj2: # CENTRO
            st.caption("CENTRO")
            for mid in [12, 19, 20]: render_mesa(mid, cj2, "Jantar", h_jan)
            st.markdown("<div style='height:210px;'></div>", unsafe_allow_html=True)
            render_mesa(6, cj2, "Jantar", h_jan)
            render_mesa(4, cj2, "Jantar", h_jan)
        with cj3: # JANELA
            st.caption("JANELA")
            for mid in [14, 16, 17, 18]: render_mesa(mid, cj3, "Jantar", h_jan)
            st.markdown("<div style='text-align:center; border:1px dashed #444; margin:10px 0; font-size:0.7em;'>ESCADAS</div>", unsafe_allow_html=True)
            for mid in [1, 2, 3]: render_mesa(mid, cj3, "Jantar", h_jan)

        if st.button("LIMPAR TUDO (JANTAR)", key="clear_jan"):
            st.session_state.sala["Jantar"] = {m: {"ocupada": False, "info": "", "nota": ""} for m in MESAS_INFO}
            st.rerun()
