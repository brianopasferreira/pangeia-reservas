import streamlit as st
from datetime import date


st.set_page_config(page_title="Pangeia Nazare", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #050505; color: #D4AF37; }
    [data-testid="stSidebar"] {
        background-color: #0c0c0c;
        border-right: 1px solid #D4AF37;
    }
    .mesa {
        border: 1px solid #D4AF37;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 5px;
        background: rgba(212, 175, 55, 0.05);
        min-height: 85px;
    }
    .ocupada {
        background: #D4AF37 !important;
        color: #000 !important;
        font-weight: bold;
    }
    .nota-display {
        font-size: 0.75em;
        color: #444;
        font-style: italic;
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
) -> None:
    mesa = sala[turno][mesa_id]
    classe = "mesa ocupada" if mesa["ocupada"] else "mesa"
    texto = f"<b>M{mesa_id}</b><br><small>{MESAS_INFO[mesa_id]}</small>"

    if mesa["ocupada"]:
        texto += f"<br>{mesa['info']}"
        if mesa["nota"]:
            texto += f"<br><span class='nota-display'>{mesa['nota']}</span>"
    else:
        texto += "<br>LIVRE"

    coluna.markdown(f"<div class='{classe}'>{texto}</div>", unsafe_allow_html=True)

    if mesa["ocupada"]:
        if coluna.button(f"LIBERTAR {mesa_id}", key=f"libertar_{turno}_{mesa_id}"):
            sala[turno][mesa_id] = {"ocupada": False, "info": "", "nota": ""}
            st.rerun()
        return

    if coluna.button(
        f"SENTAR {mesa_id}",
        key=f"sentar_{turno}_{mesa_id}",
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
    coluna.markdown(
        "<div style='text-align:center; border:1px dashed #444; margin:10px 0; font-size:0.7em;'>ESCADAS</div>",
        unsafe_allow_html=True,
    )


def render_planta(
    turno: str,
    hora_texto: str,
    sala: dict[str, dict[int, dict[str, str | bool]]],
    bloqueado: bool,
    nome_reserva: str,
    pax_reserva: int,
    nota_reserva: str,
) -> None:
    esquerda, centro, direita = st.columns([1.1, 1.2, 1.1])

    esquerda.caption("ALA MAR")
    for mesa_id in [11, 10, 9, 8]:
        render_mesa(
            mesa_id,
            esquerda,
            turno,
            hora_texto,
            sala,
            bloqueado,
            nome_reserva,
            pax_reserva,
            nota_reserva,
        )

    centro.caption("CENTRO")
    render_espaco(centro, 12)
    for mesa_id in [12, 19, 20]:
        render_mesa(
            mesa_id,
            centro,
            turno,
            hora_texto,
            sala,
            bloqueado,
            nome_reserva,
            pax_reserva,
            nota_reserva,
        )

    direita.caption("JANELA")
    for mesa_id in [14, 16, 17, 18]:
        render_mesa(
            mesa_id,
            direita,
            turno,
            hora_texto,
            sala,
            bloqueado,
            nome_reserva,
            pax_reserva,
            nota_reserva,
        )

    render_espaco(esquerda, 18)
    render_espaco(centro, 36)
    render_escadas(direita)

    linha_meio = st.columns([1.1, 0.25, 1.1, 0.25, 1.1])
    render_mesa(
        7,
        linha_meio[0],
        turno,
        hora_texto,
        sala,
        bloqueado,
        nome_reserva,
        pax_reserva,
        nota_reserva,
    )
    render_mesa(
        6,
        linha_meio[2],
        turno,
        hora_texto,
        sala,
        bloqueado,
        nome_reserva,
        pax_reserva,
        nota_reserva,
    )
    render_mesa(
        1,
        linha_meio[4],
        turno,
        hora_texto,
        sala,
        bloqueado,
        nome_reserva,
        pax_reserva,
        nota_reserva,
    )

    linha_baixo = st.columns([1.1, 0.25, 1.1, 0.25, 1.1])
    linha_baixo[0].markdown("&nbsp;", unsafe_allow_html=True)
    render_mesa(
        4,
        linha_baixo[2],
        turno,
        hora_texto,
        sala,
        bloqueado,
        nome_reserva,
        pax_reserva,
        nota_reserva,
    )

    coluna_direita_baixo = linha_baixo[4]
    render_mesa(
        2,
        coluna_direita_baixo,
        turno,
        hora_texto,
        sala,
        bloqueado,
        nome_reserva,
        pax_reserva,
        nota_reserva,
    )
    render_mesa(
        3,
        coluna_direita_baixo,
        turno,
        hora_texto,
        sala,
        bloqueado,
        nome_reserva,
        pax_reserva,
        nota_reserva,
    )


with st.sidebar:
    st.title("RESERVA")
    data_sel = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
    dia_semana = data_sel.weekday()

    encerrado_segunda, aviso_segunda = sala_encerrada(dia_semana, "Almoco")
    if encerrado_segunda:
        st.error(aviso_segunda)

    nome_res = st.text_input("Nome Cliente")
    pax_res = st.number_input("Pessoas", min_value=1, max_value=20, value=2, step=1)
    nota_res = st.text_area("Observacoes")


sala_atual = obter_sala_por_data(data_sel)
horas_almoco = gerar_horas(12, 30, 15)
horas_jantar = gerar_horas(19, 0, 22)

st.markdown("<h1 style='text-align:center;'>PANGEIA NAZARE</h1>", unsafe_allow_html=True)

tab_almoco, tab_jantar = st.tabs(["ALMOCO", "JANTAR"])


with tab_almoco:
    almoco_bloqueado, aviso_almoco = sala_encerrada(dia_semana, "Almoco")
    if almoco_bloqueado:
        st.error(aviso_almoco)

    h_almoco = st.selectbox("Hora Almoco", horas_almoco, key="sel_almoco")
    render_planta(
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
