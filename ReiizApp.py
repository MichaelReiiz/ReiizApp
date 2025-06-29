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
    pdf.cell(200, 10, f"Palpite Gerado por ReiizApp", ln=True, align="C")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    
    # Remover emojis e acentos do PDF
    texto_justo = justificativa.encode("ascii", "ignore").decode("ascii")

    pdf.multi_cell(0, 10, f"Jogo: {time1} vs {time2}")
    pdf.multi_cell(0, 10, f"Placar provável: {placar}")
    pdf.multi_cell(0, 10, f"Vencedor provável: {vencedor}")
    pdf.multi_cell(0, 10, texto_justo)
    
    return pdf.output(dest='S').encode('latin1')

def gerar_download_pdf(pdf_data):
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="palpite_reiizapp.pdf">📄 Baixar Palpite em PDF</a>'
    return href

# ---------- Interface com Streamlit ---------- #

st.set_page_config(page_title="ReiizApp", layout="centered")

# Estilo visual: fundo branco e botão vermelho
st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
        }
        .stButton>button {
            color: white;
            background-color: #e50914;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔴⚫ ReiizApp – Palpites Esportivos com IA")

st.markdown("🎯 Gere palpites com análise lógica baseada em estatísticas simuladas.")

time1 = st.text_input("Digite o nome do Time 1")
time2 = st.text_input("Digite o nome do Time 2")

if st.button("Gerar Palpite"):
    if not time1 or not time2:
        st.warning("⚠️ Por favor, digite o nome dos dois times.")
    else:
        dados1 = simular_dados_do_time(time1)
        dados2 = simular_dados_do_time(time2)

        vencedor, placar, justificativa = gerar_palpite(dados1, dados2)
        justificativa = justificativa.encode("ascii", "ignore").decode("ascii")  # remove emojis para celular fraco

        # Últimos 5 jogos (sem emojis para Android fraco)
        ult1 = " ".join(dados1["ultimos_5_jogos"])
        ult2 = " ".join(dados2["ultimos_5_jogos"])

        st.subheader("📊 Comparativo dos Times")
        df = pd.DataFrame({
            "Estatística": ["Gols", "Escanteios", "Cartões", "Desfalques", "Últimos 5 Jogos"],
            time1: [
                dados1["media_gols"], dados1["media_escanteios"],
                dados1["media_cartoes"], dados1["desfalques"], ult1
            ],
            time2: [
                dados2["media_gols"], dados2["media_escanteios"],
                dados2["media_cartoes"], dados2["desfalques"], ult2
            ]
        })
        st.table(df)

        st.subheader("📝 Palpite Gerado")
        st.success(f"✅ Vitória provável: {vencedor}")
        st.info(f"🔢 Placar provável: {placar}")
        st.markdown("📋 **Justificativa do Palpite**")
        st.markdown(justificativa)

        # Geração do PDF
        pdf_data = gerar_pdf(time1, time2, vencedor, placar, justificativa)
        st.markdown(gerar_download_pdf(pdf_data), unsafe_allow_html=True)
