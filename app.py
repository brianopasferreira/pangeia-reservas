import streamlit as st

# 1. Configuração e Branding
st.set_page_config(page_title="Pangeia Nazaré", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #D4AF37; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
    .mesa-box {
        border: 1px solid #D4AF37;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
        background-color: #111111;
    }
    .stButton>button { background-color: #D4AF37; color: black; font-weight: bold; width: 100%; border: none; }
    input { background-color: #111111 !important; color: #D4AF37 !important; border: 1px solid #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Dados das Mesas (conforme a tua foto)
MESAS = {
    1: "2pax", 2: "4-7pax", 3: "3pax", 4: "4-7pax", 6: "2pax", 7: "4-6pax",
    8: "4-6pax", 9: "4-6pax", 10: "2pax", 11: "2pax", 12: "2pax", 14: "2pax",
    16: "4-7pax", 17: "4-7pax", 18: "2-3pax", 19: "2pax", 20: "2pax"
}

if 'status' not in st.session_state:
    st.session_state.status = {m: {"ocupada": False, "nome": ""} for m in MESAS}

st.markdown("<h1>🔱 PANGEIA NAZARÉ</h1>", unsafe_allow_html=True)
st.write("---")

# 3. Disposição baseada no teu desenho (3 colunas de zona)
col_esq, col_meio, col_dir = st.columns(3)

def desenhar_mesa(m_id, local):
    info = st.session_state.status[m_id]
    cor_fundo = "#D4AF37" if info["ocupada"] else "#111111"
    cor_texto = "black" if info["ocupada"] else "#D4AF37"
    
    local.markdown(f"""
        <div class="mesa-box" style="background-color: {cor_fundo}; color: {cor_texto};">
            <strong>Mesa {m_id}</strong><br><small>{MESAS[m_id]}</small><br>
            {"<br>"+info['nome'] if info['ocupada'] else "LIVRE"}
        </div>
    """, unsafe_allow_html=True)
    
    if not info["ocupada"]:
        nome = local.text_input(f"Nome", key=f"txt{m_id}", label_visibility="collapsed", placeholder="Nome...")
        if local.button(f"Sentar M{m_id}", key=f"btn{m_id}"):
            st.session_state.status[m_id] = {"ocupada": True, "nome": nome}
            st.rerun()
    else:
        if local.button(f"Libertar M{m_id}", key=f"btn{m_id}"):
            st.session_state.status[m_id] = {"ocupada": False, "nome": ""}
            st.rerun()

# Coluna 1: Lado Esquerdo (Mesas 12, 11, 10, 9, 8, Piano...)
with col_esq:
    st.subheader("Parede Esq.")
    for m in [12, 11, 10, 9, 8]: desenhar_mesa(m, col_esq)
    st.markdown("<div style='text-align:center; padding:20px; border:1px dashed #D4AF37;'>🎹 PIANO</div>", unsafe_allow_html=True)

# Coluna 2: Centro (Mesas 19, 20, 6, 4, 7...)
with col_meio:
    st.subheader("Centro")
    for m in [19, 20, 6, 7, 4]: desenhar_mesa(m, col_meio)

# Coluna 3: Lado Direito (Mesas 14, 16, 17, 18, Escadas, 1, 2, 3)
with col_dir:
    st.subheader("Parede Dir.")
    for m in [14, 16, 17, 18, 1, 2, 3]: desenhar_mesa(m, col_dir)

st.write("---")
if st.button("Limpar Sala"):
    st.session_state.status = {m: {"ocupada": False, "nome": ""} for m in MESAS}
    st.rerun()
