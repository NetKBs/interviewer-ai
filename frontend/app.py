import streamlit as st
import cv2
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main_backend import CIMBackend

st.set_page_config(
    page_title="CIM AI | Enterprise Talent Analytics",
    page_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/3044f73c-0547-4b01-aeec-7ebff6555e1b/dmdg1ov-adf6091c-b91b-4c40-95f6-996dd8d5970d.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiIvZi8zMDQ0ZjczYy0wNTQ3LTRiMDEtYWVlYy03ZWJmZjY1NTVlMWIvZG1kZzFvdi1hZGY2MDkxYy1iOTFiLTRjNDAtOTVmNi05OTZkZDhkNTk3MGQucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.9Ect5kkHnRfXRQGXMaoZ47Q3dBuWOv0ubgEFrUBNL3o",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "page" not in st.session_state:
    st.session_state.page = "landing"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-main: #0a0510;
        --card-bg: rgba(22, 13, 35, 0.65);
        --border-color: rgba(184, 106, 249, 0.18);
        --border-hover: rgba(184, 106, 249, 0.5);
        --accent-purple: #b86af9;
        --accent-lilac: #e2bbfd;
        --text-muted: #9486a4;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 15px rgba(184, 106, 249, 0.2); }
        50% { box-shadow: 0 0 30px rgba(184, 106, 249, 0.45); }
        100% { box-shadow: 0 0 15px rgba(184, 106, 249, 0.2); }
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a0b2e 0%, var(--bg-main) 80%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f4effa;
    }

    /* Contenedores Responsivos y Estilo Global */
    .landing-hero {
        text-align: center;
        padding: 80px 20px 40px 20px;
        animation: fadeInUp 0.7s ease-out forwards;
        max-width: 900px;
        margin: 0 auto;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(184, 106, 249, 0.12);
        border: 1px solid var(--accent-purple);
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 2px;
        color: var(--accent-lilac);
        text-transform: uppercase;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.15;
        background: linear-gradient(135deg, #ffffff 0%, var(--accent-lilac) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 auto;
    }

    .hero-subtitle {
        color: var(--text-muted);
        font-size: 1.25rem;
        font-weight: 400;
        margin-top: 20px;
        line-height: 1.6;
    }

    .exec-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 28px;
        margin-bottom: 24px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        animation: fadeInUp 0.8s ease-out forwards;
    }

    .exec-card:hover {
        border-color: var(--border-hover);
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), 0 0 25px rgba(184, 106, 249, 0.15);
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 12px;
    }

    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--accent-lilac);
        margin: 0;
    }

    .card-description {
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Botones de Navegación del Producto */
    div.stButton > button {
        background: linear-gradient(135deg, #7928CA 0%, #B800FF 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.85rem 2.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        animation: pulseGlow 3s infinite !important;
        width: auto !important;
        margin: 0 auto !important;
        display: block !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(184, 0, 255, 0.5) !important;
        background: linear-gradient(135deg, #8a35e2 0%, #c426ff 100%) !important;
    }

    .back-link {
        color: var(--text-muted);
        cursor: pointer;
        font-size: 0.9rem;
        text-decoration: none;
        transition: color 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 20px;
    }
    .back-link:hover {
        color: var(--accent-lilac);
    }

    /* Panel de Métricas e Inputs */
    .metric-container {
        text-align: center;
        padding: 20px;
        background: rgba(15, 8, 26, 0.5);
        border-radius: 12px;
        border: 1px solid rgba(184, 106, 249, 0.12);
    }

    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--text-muted);
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(180deg, #ffffff 0%, var(--accent-lilac) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    div[data-testid="stFileUploader"] {
        background: rgba(13, 7, 22, 0.6);
        border: 1px dashed rgba(184, 106, 249, 0.3);
        border-radius: 10px;
        padding: 15px;
    }

    textarea {
        background-color: rgba(13, 7, 22, 0.8) !important;
        border: 1px solid rgba(184, 106, 249, 0.2) !important;
        color: #f4effa !important;
        border-radius: 8px !important;
    }

    .star-item {
        margin-bottom: 14px;
        padding-left: 12px;
        border-left: 2px solid var(--accent-purple);
    }
    .star-tag {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--accent-purple);
        letter-spacing: 1px;
    }
    .star-text {
        font-size: 0.95rem;
        color: #e0d8ea;
        margin-top: 3px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

ICONS = {
    "arrow-left": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>',
    "vision": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#b86af9" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
    "audio": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#b86af9" stroke-width="2"><path d="M12 1v22"/><path d="M17 5v14"/><path d="M22 9v6"/><path d="M7 5v14"/><path d="M2 9v6"/></svg>',
    "brain": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#b86af9" stroke-width="2"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.44 2.5 2.5 0 0 1 0-3.12 3 3 0 0 1 0-4.88 2.5 2.5 0 0 1 0-3.12A2.5 2.5 0 0 1 9.5 2zM14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.44 2.5 2.5 0 0 0 0-3.12 3 3 0 0 0 0-4.88 2.5 2.5 0 0 0 0-3.12A2.5 2.5 0 0 0 14.5 2z"/></svg>',
    "media": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#b86af9" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    "briefcase": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#b86af9" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
    "analytics": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#b86af9" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "transcript": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#b86af9" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    "target": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#b86af9" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
}


def extract_frames(video_path, max_frames=100):
    frames = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, total_frames // max_frames)
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % step == 0:
            frames.append(frame)
        count += 1
        if len(frames) >= max_frames:
            break
    cap.release()
    return frames


# ---------------------------------------------------------
# VISTA 1: LANDING PAGE COMERCIAL
# ---------------------------------------------------------
def render_landing_page():

    st.markdown(
        """
        <div class="landing-hero">
        <div class="">
            <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/3044f73c-0547-4b01-aeec-7ebff6555e1b/dmdg1ov-adf6091c-b91b-4c40-95f6-996dd8d5970d.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiIvZi8zMDQ0ZjczYy0wNTQ3LTRiMDEtYWVlYy03ZWJmZjY1NTVlMWIvZG1kZzFvdi1hZGY2MDkxYy1iOTFiLTRjNDAtOTVmNi05OTZkZDhkNTk3MGQucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.9Ect5kkHnRfXRQGXMaoZ47Q3dBuWOv0ubgEFrUBNL3o" width="200""/>
        </div>
            <div class="hero-badge">Alineación Tecnológica Inteligente</div>
            <h1 class="hero-title">Evaluación Avanzada de Candidatos con Inteligencia Artificial Multimodal</h1>
            <p class="hero-subtitle">
                Optimice sus procesos de reclutamiento ejecutivo. CIM Engine fusiona visión computacional, 
                análisis fonético y modelos lingüísticos avanzados para auditar competencias técnicas y habilidades de comunicación en tiempo real.
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="margin: 20px 0 50px 0;">', unsafe_allow_html=True)
    if st.button("INGRESAR AL PANEL DE ANÁLISIS"):
        st.session_state.page = "app"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<h3 style="text-align:center; margin-bottom: 30px; color:#e1b3ff;">Pilares de la Evaluación Multimodal</h3>',
        unsafe_allow_html=True,
    )

    f_col1, f_col2, f_col3 = st.columns(3, gap="medium")

    with f_col1:
        st.markdown(
            f"""
            <div class="exec-card">
                <div class="card-header">
                    {ICONS['vision']}
                    <span class="card-title">Análisis Biométrico Ocular</span>
                </div>
                <p class="card-description">
                    Procesamiento de fotogramas mediante MediaPipe Face Mesh para calcular de forma objetiva los índices de contacto visual, nivel de atención y seguridad postural del candidato.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with f_col2:
        st.markdown(
            f"""
            <div class="exec-card">
                <div class="card-header">
                    {ICONS['audio']}
                    <span class="card-title">Cadencia y Fluidez Verbal</span>
                </div>
                <p class="card-description">
                    Aislamiento y procesamiento de la pista de voz mediante redes neurales de Gemini para transcripción exacta y cálculo métrico de palabras por minuto (WPM) para medir elocuencia.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with f_col3:
        st.markdown(
            f"""
            <div class="exec-card">
                <div class="card-header">
                    {ICONS['brain']}
                    <span class="card-title">Auditoría Técnica STAR</span>
                </div>
                <p class="card-description">
                    Evaluación semántica profunda con modelos de lenguaje masivos para estructurar el discurso en Situación, Tarea, Acción y Resultado, contrastando con el perfil del puesto requerido.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# VISTA 2: PANEL DE ANÁLISIS INTERACTIVO
# ---------------------------------------------------------
def render_app_page():

    # Manejo manual del retorno por consistencia de diseño
    if st.button("← VOLVER AL INICIO", key="back_btn"):
        st.session_state.page = "landing"
        st.rerun()

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 35px;">
            <h1 class="main-title" style="font-size: 2.2rem;">CIM Analytics Executive Dashboard</h1>
            <p style="color: var(--text-muted); font-size: 1rem;">Módulo de Diagnóstico Audiovisual y Contraste de Competencias</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(
            f'<div class="exec-card"><div class="card-header">{ICONS["media"]}<span class="card-title">Carga de Paquetes Multimedia</span></div></div>',
            unsafe_allow_html=True,
        )
        uploaded_video = st.file_uploader(
            "Vídeo de Sesión (.mp4, .mov)", type=["mp4", "mov", "avi"]
        )
        uploaded_audio = st.file_uploader(
            "Registro de Audio (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"]
        )

    with col_right:
        st.markdown(
            f'<div class="exec-card" style="padding-bottom: 12px;"><div class="card-header">{ICONS["briefcase"]}<span class="card-title">Criterios de Evaluación Corporativa</span></div></div>',
            unsafe_allow_html=True,
        )
        job_description = st.text_area(
            "Especificaciones y Requerimientos Esenciales del Puesto",
            placeholder="Detalla los requerimientos técnicos y competencias esperadas para el perfil...",
            height=142,
        )

    st.markdown('<div style="margin: 25px 0;">', unsafe_allow_html=True)
    process_btn = st.button("EJECUTAR PIPELINE DE EVALUACIÓN")
    st.markdown("</div>", unsafe_allow_html=True)

    if process_btn:
        if not uploaded_video or not uploaded_audio or not job_description:
            st.error(
                "Por favor, cargue todos los recursos multimedia y defina los requerimientos del puesto."
            )
            return

        with st.status(
            "Procesando sesión multimedia con CIM Backend...", expanded=True
        ) as status:
            try:
                backend = CIMBackend()

                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=os.path.splitext(uploaded_audio.name)[1]
                ) as tmp_audio:
                    tmp_audio.write(uploaded_audio.read())
                    audio_path = tmp_audio.name

                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=os.path.splitext(uploaded_video.name)[1]
                ) as tmp_video:
                    tmp_video.write(uploaded_video.read())
                    video_path = tmp_video.name

                cap = cv2.VideoCapture(video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                duration_seconds = frame_count / fps if fps > 0 else 60.0
                cap.release()

                frames = extract_frames(video_path, max_frames=120)

                results = backend.process_interview_session(
                    audio_path=audio_path,
                    frames=frames,
                    job_description=job_description,
                    duration=duration_seconds,
                )

                os.unlink(audio_path)
                os.unlink(video_path)

                status.update(
                    label="Evaluación completada con éxito",
                    state="complete",
                    expanded=False,
                )

                st.markdown(
                    '<div style="margin: 40px 0 20px 0; border-top: 1px solid rgba(184,106,249,0.2); padding-top:30px;"></div>',
                    unsafe_allow_html=True,
                )

                feedback_data = results.get("feedback", {})
                score = feedback_data.get("puntaje_global", 0)

                m_col1, m_col2, m_col3 = st.columns(3)

                with m_col1:
                    st.markdown(
                        f'<div class="metric-container"><div class="metric-label">Índice de Competencia</div><div class="metric-value">{score}<span style="font-size:1.2rem; color:var(--text-muted);">/100</span></div></div>',
                        unsafe_allow_html=True,
                    )
                with m_col2:
                    st.markdown(
                        f'<div class="metric-container"><div class="metric-label">Foco / Contacto Visual</div><div class="metric-value">{results.get("eye_contact_percent", 0)}<span style="font-size:1.2rem; color:var(--text-muted);">%</span></div></div>',
                        unsafe_allow_html=True,
                    )
                with m_col3:
                    st.markdown(
                        f'<div class="metric-container"><div class="metric-label">Cadencia Verbal</div><div class="metric-value">{results.get("wpm", 0)} <span style="font-size:1.2rem; color:var(--text-muted);">WPM</span></div></div>',
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    '<div style="margin-bottom: 30px;"></div>', unsafe_allow_html=True
                )

                res_col1, res_col2 = st.columns([1.3, 1], gap="medium")

                with res_col1:
                    star = feedback_data.get("analisis_star", {})
                    st.markdown(
                        f"""
                        <div class="exec-card">
                            <div class="card-header">
                                {ICONS['analytics']}
                                <span class="card-title">Desglose Estructurado (Metodología STAR)</span>
                            </div>
                            <div class="star-item"><div class="star-tag">Situación</div><div class="star-text">{star.get('situation', 'No detectada')}</div></div>
                            <div class="star-item"><div class="star-tag">Tarea</div><div class="star-text">{star.get('task', 'No detectada')}</div></div>
                            <div class="star-item"><div class="star-tag">Acción</div><div class="star-text">{star.get('action', 'No detectada')}</div></div>
                            <div class="star-item" style="margin-bottom:0;"><div class="star-tag">Resultado</div><div class="star-text">{star.get('result', 'No detectada')}</div></div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f"""
                        <div class="exec-card">
                            <div class="card-header">
                                {ICONS['transcript']}
                                <span class="card-title">Registro Auditoría de Discurso</span>
                            </div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #c3b8d8; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                                {results.get("transcription", "")}
                            </div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

                with res_col2:
                    mejoras = feedback_data.get("mejoras_comunicacion", [])
                    mejoras_html = ""
                    if mejoras:
                        for mejora in mejoras:
                            mejoras_html += f'<li style="margin-bottom: 12px; color: #e0d8ea; font-size: 0.92rem; line-height: 1.5;">{mejora}</li>'
                    else:
                        mejoras_html = '<p style="color: #00f59b;">No se han detectado brechas críticas en la articulación corporativa.</p>'

                    st.markdown(
                        f"""
                        <div class="exec-card">
                            <div class="card-header">
                                {ICONS['target']}
                                <span class="card-title">Directrices de Optimización</span>
                            </div>
                            <ul style="padding-left: 20px; margin: 0;">
                                {mejoras_html}
                            </ul>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                status.update(
                    label="Interrupción en el pipeline de evaluación", state="error"
                )
                st.error(f"Fallo técnico reportado: {str(e)}")


# ---------------------------------------------------------
# ENRUTADOR PRINCIPAL (SPA)
# ---------------------------------------------------------
def main():
    if st.session_state.page == "landing":
        render_landing_page()
    elif st.session_state.page == "app":
        render_app_page()


if __name__ == "__main__":
    main()
