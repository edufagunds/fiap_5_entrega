import io
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="PEDE | Radar de Risco",
    page_icon="🎓",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "modelo_risco_defasagem.joblib"

FEATURES = ["IAN", "IDA", "IEG", "IAA", "IPS", "IPV", "pedra_cat"]
PEDRAS = ["Quartzo", "Ágata", "Ametista", "Topázio"]

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

st.title("🎓 PEDE — Radar de Risco de Defasagem")
st.caption("Modelo preditivo baseado nos indicadores IAN, IDA, IEG, IAA, IPS, IPV e Pedra.")

with st.sidebar:
    st.header("Sobre o modelo")
    st.write(
        "A aplicação estima a probabilidade de o aluno apresentar defasagem "
        "no próximo ciclo. O modelo foi treinado com as transições históricas "
        "2022→2023 e 2023→2024."
    )
    st.info(
        "O resultado é um alerta de priorização e não um diagnóstico pedagógico. "
        "A decisão final deve considerar avaliação humana e contexto do aluno."
    )

# -----------------------------------------------------------------------------
# Entrada individual
# -----------------------------------------------------------------------------
st.header("1. Avaliação individual")

col1, col2, col3 = st.columns(3)
with col1:
    ian = st.number_input("IAN", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    ida = st.number_input("IDA", min_value=0.0, max_value=10.0, value=6.5, step=0.1)
    ieg = st.number_input("IEG", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
with col2:
    iaa = st.number_input("IAA", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    ips = st.number_input("IPS", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    ipv = st.number_input("IPV", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
with col3:
    pedra = st.selectbox("Pedra", PEDRAS, index=1)

if st.button("Calcular risco", type="primary", use_container_width=True):
    row = pd.DataFrame([{
        "IAN": ian,
        "IDA": ida,
        "IEG": ieg,
        "IAA": iaa,
        "IPS": ips,
        "IPV": ipv,
        "pedra_cat": pedra,
    }])

    probability = float(model.predict_proba(row[FEATURES])[:, 1][0])
    probability_pct = probability * 100

    if probability < 0.30:
        band = "Baixo risco"
        action = "Acompanhamento regular"
    elif probability < 0.70:
        band = "Risco intermediário"
        action = "Investigar indicadores e acompanhar mais de perto"
    else:
        band = "Alto risco"
        action = "Priorizar avaliação e possível intervenção"

    st.subheader("Resultado")
    r1, r2, r3 = st.columns(3)
    r1.metric("Probabilidade estimada", f"{probability_pct:.1f}%")
    r2.metric("Faixa", band)
    r3.metric("Ação sugerida", action)

    st.progress(min(probability, 1.0), text=f"Probabilidade de risco: {probability_pct:.1f}%")

# -----------------------------------------------------------------------------
# Entrada em lote
# -----------------------------------------------------------------------------
st.divider()
st.header("2. Avaliação em lote")
st.write(
    "Envie um CSV com as colunas **IAN, IDA, IEG, IAA, IPS, IPV e pedra_cat** "
    "para classificar vários alunos de uma vez."
)

example = pd.DataFrame([{
    "IAN": 7.5, "IDA": 6.8, "IEG": 8.0, "IAA": 7.2,
    "IPS": 7.0, "IPV": 7.5, "pedra_cat": "Ágata"
}])

with st.expander("Ver formato esperado do CSV"):
    st.dataframe(example, use_container_width=True)

uploaded = st.file_uploader("CSV dos alunos", type=["csv"])

if uploaded is not None:
    try:
        batch = pd.read_csv(uploaded)
        missing = [c for c in FEATURES if c not in batch.columns]

        if missing:
            st.error("Colunas ausentes: " + ", ".join(missing))
        else:
            probs = model.predict_proba(batch[FEATURES])[:, 1]
            result = batch.copy()
            result["probabilidade_risco"] = probs
            result["probabilidade_risco_%"] = (probs * 100).round(1)
            result["faixa_risco"] = pd.cut(
                probs,
                bins=[-np.inf, 0.30, 0.70, np.inf],
                labels=["Baixo", "Médio", "Alto"]
            )

            st.subheader("Resultados")
            st.dataframe(result, use_container_width=True)

            csv_bytes = result.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Baixar resultados em CSV",
                data=csv_bytes,
                file_name="resultado_risco_defasagem.csv",
                mime="text/csv",
            )
    except Exception as exc:
        st.error(f"Não foi possível processar o arquivo: {exc}")

st.divider()
st.caption(
    "Projeto Datathon PEDE 2022–2024 | Modelo: Regressão Logística | "
    "Uso recomendado: apoio à priorização pedagógica."
)
