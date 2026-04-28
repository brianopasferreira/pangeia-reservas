import streamlit as st
from datetime import date


st.set_page_config(page_title="Pangeia Nazare", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #050505 0%, #111111 100%);
        color: #D4AF37;
    }

    [data-testid="stSidebar"] {
        background-color: #0c0c0c;
        border-right: 1px solid #D4AF37;
    }

    .titulo-sala {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #D4AF37;
        margin-bottom: 0.35rem;
    }

    .subtitulo-sala {
        text-align: center;
        font-size: 0.95rem;
        color: #d9c77e;
        margin-bottom: 1rem;
    }

    .planta-wrap {
        border: 2px solid rgba(212, 175, 55, 0.45);
        border-radius: 12px;
        padding: 18px 18px 12px 18px;
        background: rgba(212, 175, 55, 0.03);
    }

    .zona-label {
        text-align: center;
        font-weight: 700;
        color: #d9c77e;
        margin-bottom: 0.4rem;
        letter-spacing: 0.5px;
        font-size: 0.95rem;
    }

    .mesa {
        border: 1px solid #D4AF37;
        padding: 10px 8px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 8px;
        background: rgba(212, 175, 55, 0.06);
        min-height: 88px;
        box-shadow: inset 0 0 0 1px rgba(212, 175, 55, 0.08);
        font-size: 0.95rem;
    }

    .mesa-mini {
        border: 1px solid #D4AF37;
        padding: 8px 6px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 6px;
        background: rgba(212, 175, 55, 0.06);
        min-height: 74px;
        font-size: 0.82rem;
    }

    .ocupada {
        background: #D4AF37 !important;
        color: #000 !important;
        font-weight: bold;
    }

    .nota-display {
        font-size: 0.75em;
        color: #2e2e2e;
        font-style: italic;
    }

    .escadas {
        text-align: center;
        border: 1px dashed #8b7630;
        border-radius: 6px;
        margin: 10px 0;
        padding: 8px 0;
        font-size: 0.72rem;
        color: #d9c77e;
        background: rgba(212, 175, 55, 0.03);
    }

    .janela-vertical {
        writing-mode: vertical-rl;
        transform: rotate(180deg);
        text-align: center;
        font-weight: 700;
        color: #d9c77e;
        min-height: 540px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-left: 2px solid rgba(212, 175, 55, 0.45);
        margin-left: 6px;
        padding-left: 8px;
        letter-spacing: 1px;
    }

    .entrada {
        margin: 16px auto 0 auto;
        width: 42%;
        text-align: center;
        border-top: 2px solid rgba(212, 175, 55, 0.45);
        padding-top: 10px;
        color: #bda55d;
        font-size: 0.82rem;
    }

    .entrada-mobile {
        margin-top: 10px;
        text-align: center;
        border-top: 2px solid rgba(212, 175, 55, 0.45);
        padding-top: 8px;
        color: #bda55d;
        font-size: 0.76rem;
    }

    .parede-topo {
        height: 2px;
        background: rgba(212, 175, 55, 0.40);
        margin-bottom: 12px;
    }

    .passagem {
        height: 24px;
    }

    .linha-apoio {
        border-top: 2px solid rgba(212, 175, 55, 0.32);
        margin-top: 6px;
        padding-top: 8px;
    }

    .bloco-info {
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 8px;
        padding: 8px 10px;
        text-align: center;
        color: #d9c77e;
        margin-bottom: 8px;
        background: rgba(212, 175, 55, 0.03);
        font-size: 0.82rem;
    }

    div[data-testid="stButton"] > button {
        width: 100%;
        border-radius: 6px;
        border: 1px solid #D4AF37;
        background: #111111;
        color: #D4AF37;
        min-height: 40px;
        font-size: 0.92rem;
    }

    div[data-testid="stButton"] > button:hover {
        border-color: #f1d57a;
        color: #f1d57a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


MESAS_INFO = {
    1: "2p",
    2: "4-7p",
    3: "2p",
    4: "4-7p",
    6: "2p",
    7: "2p",
    8: "4-6p",
    9: "4-6p",
    10: "2p",
    11: "2p",
    12: "2p",
    14: "2p",
    16: "4-7p",
    17: "4-7p",
    18: "2-3p",
    19: "2p",
    20: "2p",
}


def gerar_horas(hora_inicio: int, minuto_inicio: int, hora_fim: int) -> list[str]:
    horas = []
    for hora in range(hora_inicio, hora_fim + 1):
        for minuto in (0, 15, 30, 45):
            if hora == hora_inicio and minuto < minuto_inicio:
                continue
            if hora == hora_fim and minuto > 0:
                continue
            horas.append(f"{hora:02d}:{minuto:02d}")
    return horas


def estado_vazio() -> dict[int, dict[str, str | bool]]:
    return {mesa: {"ocupada": False, "info": "", "nota": ""} for mesa in MESAS_INFO}


def obter_sala_por_data(data_reserva: date) -> dict[str, dict[int, dict[str, str | bool]]]:
    chave = data_reserva.isoformat()
    if "reservas" not in st.session_state:
        st.session_state.reservas = {}
    if chave not in st.session_state.reservas:
        st.session_state.reservas[chave] = {
            "Almoco": estado_vazio(),
            "Jantar": estado_vazio(),
        }
    return st.session_state.reservas[chave]


def sala_encerrada(dia_semana: int, turno: str) -> tuple[bool, str]:
    if dia_semana == 0:
        return True, "ENCERRADO A SEGUNDA"
    if turno == "Jantar" and dia_semana == 6:
        return True, "DOMINGO AO JANTAR: ENCERRADO"
    return False, ""


def limpar_turno(sala: dict[str, dict[int, dict[str, str | bool]]], turno: str) -> None:
    sala[turno] = estado_vazio()


def render_mesa(
    mesa_id: int,
    coluna,
    turno: str,
    hora_texto: str,
    sala: dict[str, dict[int, dict[str, str | bool]]],
    bloqueado: bool,
    nome_reserva: str,
    pax_reserva: int,
    nota_reserva: str,
    compacta: bool = False,
) -> None:
    mesa = sala[turno][mesa_id]
    base_class = "mesa-mini" if compacta else "mesa"
    classe = f"{base_class} ocupada" if mesa["ocupada"] else base_class
    texto = f"<b>M{mesa_id}</b><br><small>{MESAS_INFO[mesa_id]}</small>"

    if mesa["ocupada"]:
        texto += f"<br>{mesa['info']}"
        if mesa["nota"]:
            texto += f"<br><span class='nota-display'>{mesa['nota']}</span>"
    else:
        texto += "<br>LIVRE"

    coluna.markdown(f"<div class='{classe}'>{texto}</div>", unsafe_allow_html=True)

    if mesa["ocupada"]:
        if coluna.button(f"LIBERTAR {mesa_id}", key=f"libertar_{turno}_{mesa_id}_{compacta}"):
            sala[turno][mesa_id] = {"ocupada": False, "info": "", "nota": ""}
            st.rerun()
        return

    if coluna.button(
        f"SENTAR {mesa_id}",
        key=f"sentar_{turno}_{mesa_id}_{compacta}",
        disabled=bloqueado,
    ):
        if not nome_reserva.strip():
            st.warning("Indica o nome do cliente antes de sentar a mesa.")
            return

        sala[turno][mesa_id] = {
            "ocupada": True,
            "info": f"{nome_reserva.strip()} ({pax_reserva}p) @ {hora_texto}",
            "nota": nota_reserva.strip(),
        }
        st.rerun()


def render_espaco(coluna, altura: int) -> None:
    coluna.markdown(f"<div style='height:{altura}px;'></div>", unsafe_allow_html=True)


def render_escadas(coluna) -> None:
    coluna.markdown("<div class='escadas'>ESCADAS</div>", unsafe_allow_html=True)


def render_planta_pc(
    turno: str,
    hora_texto: str,
    sala: dict[str, dict[int, dict[str, str | bool]]],
    bloqueado: bool,
    nome_reserva: str,
    pax_reserva: int,
    nota_reserva: str,
) -> None:
    st.markdown("<div class='subtitulo-sala'>Modo PC</div>", unsafe_allow_html=True)

    corpo, lateral = st.columns([20, 1.4])

    with corpo:
        st.markdown("<div class='planta-wrap'>", unsafe_allow_html=True)
        st.markdown("<div class='parede-topo'></div>", unsafe_allow_html=True)

        topo_esq, topo_ctr, topo_dir = st.columns([1.15, 1.2, 1.15])

        topo_esq.markdown("<div class='zona-label'>ALA MAR</div>", unsafe_allow_html=True)
        for mesa_id in [11, 10, 9, 8]:
            render_mesa(mesa_id, topo_esq, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)

        topo_ctr.markdown("<div class='zona-label'>CENTRO</div>", unsafe_allow_html=True)
        render_espaco(topo_ctr, 14)
        for mesa_id in [12, 19, 20]:
            render_mesa(mesa_id, topo_ctr, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)

        topo_dir.markdown("<div class='zona-label'>LADO JANELA</div>", unsafe_allow_html=True)
        for mesa_id in [14, 16, 17, 18]:
            render_mesa(mesa_id, topo_dir, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)

        render_espaco(topo_esq, 8)
        render_espaco(topo_ctr, 26)
        render_escadas(topo_dir)

        meio = st.columns([1.15, 0.22, 1.05, 0.22, 1.15])
        render_mesa(7, meio[0], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)
        meio[2].markdown("<div class='passagem'></div>", unsafe_allow_html=True)
        render_mesa(6, meio[2], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)
        render_mesa(1, meio[4], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)

        baixo = st.columns([1.15, 0.22, 1.05, 0.22, 1.15])
        baixo[0].markdown("<div class='passagem'></div>", unsafe_allow_html=True)
        render_mesa(4, baixo[2], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)

        baixo[4].markdown("<div class='linha-apoio'></div>", unsafe_allow_html=True)
        render_mesa(2, baixo[4], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)
        render_mesa(3, baixo[4], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)

        st.markdown("<div class='entrada'>ENTRADA / ZONA INFERIOR</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with lateral:
        st.markdown("<div class='janela-vertical'>JANELA</div>", unsafe_allow_html=True)


def render_planta_tablet(
    turno: str,
    hora_texto: str,
    sala: dict[str, dict[int, dict[str, str | bool]]],
    bloqueado: bool,
    nome_reserva: str,
    pax_reserva: int,
    nota_reserva: str,
) -> None:
    st.markdown("<div class='subtitulo-sala'>Modo Tablet</div>", unsafe_allow_html=True)
    st.markdown("<div class='planta-wrap'>", unsafe_allow_html=True)

    linha1 = st.columns(3)
    linha1[0].markdown("<div class='zona-label'>ALA MAR</div>", unsafe_allow_html=True)
    linha1[1].markdown("<div class='zona-label'>CENTRO</div>", unsafe_allow_html=True)
    linha1[2].markdown("<div class='zona-label'>JANELA</div>", unsafe_allow_html=True)

    for mesa_id in [11, 10, 9, 8]:
        render_mesa(mesa_id, linha1[0], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    for mesa_id in [12, 19, 20]:
        render_mesa(mesa_id, linha1[1], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    for mesa_id in [14, 16, 17, 18]:
        render_mesa(mesa_id, linha1[2], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)

    render_escadas(linha1[2])

    st.markdown("<div class='bloco-info'>LINHA MEIO</div>", unsafe_allow_html=True)
    linha2 = st.columns(3)
    render_mesa(7, linha2[0], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(6, linha2[1], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(1, linha2[2], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)

    st.markdown("<div class='bloco-info'>LINHA BAIXO</div>", unsafe_allow_html=True)
    linha3 = st.columns(3)
    linha3[0].markdown("&nbsp;", unsafe_allow_html=True)
    render_mesa(4, linha3[1], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(2, linha3[2], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(3, linha3[2], turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)

    st.markdown("<div class='entrada-mobile'>ENTRADA / ZONA INFERIOR</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_planta_telemovel(
    turno: str,
    hora_texto: str,
    sala: dict[str, dict[int, dict[str, str | bool]]],
    bloqueado: bool,
    nome_reserva: str,
    pax_reserva: int,
    nota_reserva: str,
) -> None:
    st.markdown("<div class='subtitulo-sala'>Modo Telemovel</div>", unsafe_allow_html=True)
    st.markdown("<div class='planta-wrap'>", unsafe_allow_html=True)

    st.markdown("<div class='bloco-info'>ALA MAR</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    for mesa_id in [11, 10]:
        render_mesa(mesa_id, c1, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    for mesa_id in [9, 8]:
        render_mesa(mesa_id, c2, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)

    st.markdown("<div class='bloco-info'>CENTRO</div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    render_mesa(12, c3, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(19, c4, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(20, c3, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)

    st.markdown("<div class='bloco-info'>LADO JANELA</div>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    for mesa_id in [14, 16]:
        render_mesa(mesa_id, c5, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    for mesa_id in [17, 18]:
        render_mesa(mesa_id, c6, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)

    render_escadas(st)

    st.markdown("<div class='bloco-info'>LINHA DO MEIO</div>", unsafe_allow_html=True)
    c7, c8, c9 = st.columns(3)
    render_mesa(7, c7, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(6, c8, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(1, c9, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)

    st.markdown("<div class='bloco-info'>LINHA DE BAIXO</div>", unsafe_allow_html=True)
    c10, c11, c12 = st.columns(3)
    render_mesa(4, c10, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(2, c11, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)
    render_mesa(3, c12, turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva, compacta=True)

    st.markdown("<div class='entrada-mobile'>JANELA / ENTRADA</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_planta(
    modo_visual: str,
    turno: str,
    hora_texto: str,
    sala: dict[str, dict[int, dict[str, str | bool]]],
    bloqueado: bool,
    nome_reserva: str,
    pax_reserva: int,
    nota_reserva: str,
) -> None:
    if modo_visual == "PC":
        render_planta_pc(turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)
    elif modo_visual == "Tablet":
        render_planta_tablet(turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)
    else:
        render_planta_telemovel(turno, hora_texto, sala, bloqueado, nome_reserva, pax_reserva, nota_reserva)


with st.sidebar:
    st.title("RESERVA")
    data_sel = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
    dia_semana = data_sel.weekday()

    encerrado_segunda, aviso_segunda = sala_encerrada(dia_semana, "Almoco")
    if encerrado_segunda:
        st.error(aviso_segunda)

    modo_visual = st.radio("Vista", ["PC", "Tablet", "Telemovel"], index=0)

    nome_res = st.text_input("Nome Cliente")
    pax_res = st.number_input("Pessoas", min_value=1, max_value=20, value=2, step=1)
    nota_res = st.text_area("Observacoes")


sala_atual = obter_sala_por_data(data_sel)
horas_almoco = gerar_horas(12, 30, 15)
horas_jantar = gerar_horas(19, 0, 22)

st.markdown("<div class='titulo-sala'>PANGEIA NAZARE</div>", unsafe_allow_html=True)

tab_almoco, tab_jantar = st.tabs(["ALMOCO", "JANTAR"])


with tab_almoco:
    almoco_bloqueado, aviso_almoco = sala_encerrada(dia_semana, "Almoco")
    if almoco_bloqueado:
        st.error(aviso_almoco)

    h_almoco = st.selectbox("Hora Almoco", horas_almoco, key="sel_almoco")
    render_planta(
        modo_visual,
        "Almoco",
        h_almoco,
        sala_atual,
        almoco_bloqueado,
        nome_res,
        pax_res,
        nota_res,
    )

    if st.button("LIMPAR TUDO (ALMOCO)", key="clear_almoco"):
        limpar_turno(sala_atual, "Almoco")
        st.rerun()


with tab_jantar:
    jantar_bloqueado, aviso_jantar = sala_encerrada(dia_semana, "Jantar")
    if jantar_bloqueado:
        st.error(aviso_jantar)

    h_jantar = st.selectbox("Hora Jantar", horas_jantar, key="sel_jantar")
    render_planta(
        modo_visual,
        "Jantar",
        h_jantar,
        sala_atual,
        jantar_bloqueado,
        nome_res,
        pax_res,
        nota_res,
    )

    if st.button("LIMPAR TUDO (JANTAR)", key="clear_jantar"):
        limpar_turno(sala_atual, "Jantar")
        st.rerun()
