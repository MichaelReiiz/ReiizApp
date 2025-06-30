import streamlit as st
import random
import pandas as pd
from fpdf import FPDF
import base64

# Função para simular dados do time
def simular_dados_do_time(time):
    return {
        "nome": time,
        "ultimos_5_jogos": [random.choice(["V", "E", "D"]) for _ in range(5)],
        "media_gols": round(random.uniform(0.5, 2.5), 2),
        "media_escanteios": round(random.uniform(3, 8), 1),
        "media_cartoes": round(random.uniform(1, 4), 1),
        "desfalques": random.randint(0, 3)
    }

# Função que gera o palpite e a justificativa
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

    justificativa = f"""Análise Inteligente:
- {time_a['nome']} → Gols: {time_a['media_gols']}, Escanteios: {time_a['media_escanteios']}, Cartões: {time_a['media_cartoes']}, Desfalques: {time_a['desfalques']}, Score: {round(score_a, 2)}
- {time_b['nome']} → Gols: {time_b['media_gols']}, Escanteios: {time_b['media_escanteios']}, Cartões: {time_b['media_cartoes']}, Desfalques: {time_b['desfalques']}, Score: {round(score_b, 2)}

Resultado provável com base nas estatísticas: {vencedor}
"""
    return vencedor, placar, justificativa

# Função para gerar PDF
def gerar_pdf(time1, time2, vencedor, placar, justificativa):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(220, 50, 50)
    pdf.cell(0, 10, "Palpite Gerado por ReiizApp", ln=True, align="C")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)

    texto_limpo = justificativa.encode("ascii", "ignore").decode("ascii")  # remove emojis e caracteres especiais

    pdf.multi_cell(0, 10, f"Jogo: {time1} vs {time2}")
    pdf.multi_cell(0, 10, f"Placar provável: {placar}")
    pdf.multi_cell(0, 10, f"Vencedor provável: {vencedor}")
    pdf.multi_cell(0, 10, texto_limpo)

    return pdf.output(dest='S').encode('latin1')

# Função para criar link de download do PDF
def gerar_download_pdf(pdf_data):
    b64 = base64.b64encode(pdf_data).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="palpite_reiizapp.pdf">📄 Baixar Palpite em PDF</a>'

# Configurações da página
st.set_page_config(page_title="ReiizApp", layout="centered")

# Estilo básico com fundo branco e texto cinza escuro
st.markdown("""
    <style>
        body, .stApp {
            background-color: white !important;
            color: #333333 !important;
        }
        div.stButton > button {
            background-color: #e50914;
            color: white;
            border-radius: 5px;
            padding: 0.5em 1em;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho
st.title("ReiizApp – Palpites Esportivos com IA")
st.markdown("Gere palpites baseados em análise lógica de estatísticas simuladas.")

# Inputs para nomes dos times
time1 = st.text_input("Digite o nome do Time 1", "")
time2 = st.text_input("Digite o nome do Time 2", "")

# Botão para gerar palpite
if st.button("Gerar Palpite"):
    if not time1.strip() or not time2.strip():
        st.warning("⚠️ Por favor, preencha os nomes dos dois times para gerar o palpite.")
    else:
        dados1 = simular_dados_do_time(time1.strip())
        dados2 = simular_dados_do_time(time2.strip())

        vencedor, placar, justificativa = gerar_palpite(dados1, dados2)

        ult1 = " ".join(dados1["ultimos_5_jogos"])
        ult2 = " ".join(dados2["ultimos_5_jogos"])

        st.subheader("Comparativo dos Times")
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

        st.subheader("Palpite Gerado")

        resultado_md = f"""
**Vitória provável:** {vencedor}  
**Placar provável:** {placar}  

**Justificativa do Palpite:**  
{justificativa}
"""
        st.write(resultado_md)

        pdf_data = gerar_pdf(time1, time2, vencedor, placar, justificativa)
        st.markdown(gerar_download_pdf(pdf_data), unsafe_allow_html=True)

