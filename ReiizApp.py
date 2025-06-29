import streamlit as st
import random
import pandas as pd
from fpdf import FPDF
import base64

# ---------- Funções de lógica ---------- #

def simular_dados_do_time(time):
    return {
        "nome": time,
        "ultimos_5_jogos": [random.choice(["V", "E", "D"]) for _ in range(5)],
        "media_gols": round(random.uniform(0.5, 2.5), 2),
        "media_escanteios": round(random.uniform(3, 8), 1),
        "media_cartoes": round(random.uniform(1, 4), 1),
        "desfalques": random.randint(0, 3)
    }

def gerar_palpite(time_a, time_b):
    score_a = (
        time_a["media_gols"] * 2 +
        time_a["media_escanteios"] * 0.3 -
        time_a["media_cartoes"] * 0.2 -
        time_a["desfalques"] * 0.5
    )
    score_b = (
        time_b["media_gols"] * 2 +
        time_b["media_escanteios"] * 0.3 -
        time_b["media_cartoes"] * 0.2 -
        time_b["desfalques"] * 0.5
    )

    if score_a > score_b:
        vencedor = time_a["nome"]
        placar = f"{random.randint(2, 3)}x{random.randint(0, 1)}"
    elif score_b > score_a:
        vencedor = time_b["nome"]
        placar = f"{random.randint(0, 1)}x{random.randint(2, 3)}"
    else:
        vencedor = "Empate"
        placar = f"{random.randint(1, 2)}x{random.randint(1, 2)}"

    justificativa = f"""
Análise Inteligente:
- {time_a['nome']} → Gols: {time_a['media_gols']}, Escanteios: {time_a['media_escanteios']}, Cartões: {time_a['media_cartoes']}, Desfalques: {time_a['desfalques']}, Score: {round(score_a, 2)}
- {time_b['nome']} → Gols: {time_b['media_gols']}, Escanteios: {time_b['media_escanteios']}, Cartões: {time_b['media_cartoes']}, Desfalques: {time_b['desfalques']}, Score: {round(score_b, 2)}

Resultado provável com base nas estatísticas: {vencedor}
"""
    return vencedor, placar, justificativa

# ---------- Geração de PDF ---------- #

def gerar_pdf(time1, time2, vencedor, placar, justificativa):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(220, 50, 50)
    pdf.cell(200, 10, "Palpite Gerado por ReiizApp", ln=True, align="C")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)

    texto_limpo = justificativa.encode("ascii", "ignore").decode("ascii")  # remove emojis/acentos

    pdf.multi_cell(0, 10, f"Jogo: {time1} vs {time2}")
    pdf.multi_cell(0, 10, f"Placar provável: {placar}")
    pdf.multi_cell(0, 10, f"Vencedor provável: {vencedor}")
    pdf.multi_cell(0, 10, texto_limpo)

    return pdf.output(dest='S').encode('latin1')

def gerar_download_pdf(pdf_data):
    b64 = base64.b64encode(pdf_data).decode()
    link = f'<a href="data:application/pdf;base64,{b64}" download="palpite_reiizapp.pdf">📄 Baixar Palpite em PDF</a>'
    return link

# ---------- Interface com Streamlit ---------- #

st.set_page_config(page_title="ReiizApp", layout="centered")

# CSS para fundo branco e letras cinza escuro
st.markdown("""
    <style>
        body, .stApp {
            background-color: white !important;
            color: #333333 !important;
        }
        /* Botão vermelho com texto branco */
        div.stButton > button {
            background-color: #e50914;
            color: white;
            border-radius: 4px;
            padding: 0.5em 1em;
        }
    </style>
""", unsafe_allow_html=True)

st.title("ReiizApp – Palpites Esportivos com IA")
st.markdown("Gere palpites com análise lógica baseada em estatísticas simuladas.")

# Entrada dos times
time1 = st.text_input("Digite o nome do Time 1")
time2 = st.text_input("Digite o nome do Time 2")

# Botão
if st.button("Gerar Palpite"):
    if not time1 or not time2:
        st.warning("⚠️ Por favor, digite o nome dos dois times.")
    else:
        dados1 = simular_dados_do_time(time1)
        dados2 = simular_dado_
