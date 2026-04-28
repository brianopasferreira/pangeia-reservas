import streamlit as st
from datetime import datetime, time

# 1. Configuração e Estética de Luxo
st.set_page_config(page_title="Pangeia Nazaré - Gestão VIP", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    /* Fundo 'Vivo' com textura e gradiente */
    .stApp { 
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #050505 100%);
        color: #D4AF37; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Estilizada */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 2px solid #D4AF37;
    }

    /* Cartões das Mesas */
    .mesa-container {
        border: 1px solid rgba(212, 175, 55, 0.4);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 10px;
        background: rgba(20, 20, 20, 0.8);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    .mesa-ocupada { 
        background: linear-gradient(145deg, #D4AF37, #8B6914) !important;
        color: #000 !important;
        border: none;
    }

    /* Alertas de Fechado */
    .closed-alert {
        background-color: #8B0000;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
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

# --- SIDEBAR: CONTROLO DE HORÁRIO ---
with st.sidebar:
    st.image("https://pangeiarestaurante.com/wp-content/themes/pangeia/images/logo.png", width=200) # Placeholder logo
    st.markdown("### 📅 Agendamento")
    
    data_sel = st.date_input("Data da Reserva", datetime.now())
    
    # Validação de Segunda-feira
    e_segunda = data_sel.weekday() == 0 # 0 é Segunda
    
    if e_segunda:
        st.error("⚠️ RESTAURANTE FECHADO À SEGUNDA")
        bloqueio = True
    else:
        bloqueio = False
        turno = st.radio("Turno", ["Almoço (12h-15h)", "Jantar (19h-22h)"])
        
        if "Almoço" in turno:
            hora_sel = st.slider("Hora", time(12, 0), time(15, 0), time(13, 0))
        else:
            hora_sel = st.slider("Hora", time(19, 0), time(22, 0), time(20, 0))
            
        pax_sel = st.number_input("Pessoas", min_value=1, max_value=20, value=2)
        nome_sel = st.text_input("Nome do Cliente")

st.markdown("<h1>🔱 PANGEIA NAZARÉ</h1>", unsafe_allow_html=True)

if bloqueio:
    st.markdown("<div class='closed-alert'>O Pangeia encontra-se encerrado às Segundas-feiras para descanso do pessoal.</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='text-align:center;'>{data_sel.strftime('%d/%m/%Y')} | {hora_sel.strftime('%H:%M')} | {pax_sel} Pessoas</p>", unsafe_allow_html=True)

    # 3. Layout de Sala
    col1, col2, col3 = st.columns(3)

    def render_mesa(m_id, coluna):
        info = st.session_state.sala[m_id]
        classe = "mesa-ocupada" if info["ocupada"] else ""
        txt_cor = "#000" if info["ocupada"] else "#D4AF37"
        
        coluna.markdown(f"""
            <div class="mesa-container {classe}">
                <div style="font-size: 1.2em; font-weight: bold;">Mesa {m_id}</div>
                <div style="font-size: 0.7em; opacity: 0.8;">{MESAS[m_id]}</div>
                <div style="margin-top: 8px; font-size: 0.9em; font-weight: bold; color: {txt_cor};">
                    {info['detalhes'] if info['ocupada'] else "DISPONÍVEL"}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if not info["ocupada"]:
            if coluna.button(f"OCUPAR M{m_id}", key=f"btn{m_id}"):
                if nome_sel:
                    detalhe = f"{nome_sel} ({pax_sel}p) - {hora_sel.strftime('%H:%M')}"
                    st.session_state.sala[m_id] = {"ocupada": True, "detalhes": detalhe}
                    st.rerun()
                else:
                    st.error("Insira o nome!")
        else:
            if coluna.button(f"LIBERTAR", key=f"btn{m_id}"):
                st.session_state.sala[m_id] = {"ocupada": False, "detalhes": ""}
                st.rerun()

    # --- Distribuição ---
    with col1:
        st.markdown("### Ala Mar")
        for m in [12, 11, 10, 9, 8]: render_mesa(m, col1)
        st.markdown("<div style='border:1px dashed #444; padding:10px; text-align:center; color:#555;'>🎹 PIANO</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Centro")
        for m in [19, 20, 6, 7, 4]: render_mesa(m, col2)

    with col3:
        st.markdown("### Ala Entrada")
        for m in [14, 16, 17, 18]: render_mesa(m, col3)
        st.markdown("<div style='border:1px dashed #444; padding:10px; text-align:center; color:#555;'>🪜 ESCADAS</div>", unsafe_allow_html=True)
        for m in [1, 2, 3]: render_mesa(m, col3)

st.write("---")
if st.button("LIMPAR MAPA DE HOJE"):
    st.session_state.sala = {m: {"ocupada": False, "detalhes": ""} for m in MESAS}
    st.rerun()
