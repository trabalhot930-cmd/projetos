import streamlit as st
import smtplib
import re
import pandas as pd
import os
import time
import base64
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Triagem Jurídica - Dra. Lethicia Fernanda",
    page_icon="🦋",
    layout="centered"
)

# 2. CARREGAR LOGO EM BASE64 PARA FUNDO
def get_logo_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64("logo_lethicia_png.jpeg")
bg_style = ""
if logo_b64:
    bg_style = f"""
    [data-testid="stForm"] {{
        position: relative;
        overflow: hidden;
    }}
    [data-testid="stForm"]::before {{
        content: '';
        position: absolute;
        inset: 0;
        background-image: url("data:image/jpeg;base64,{logo_b64}");
        background-size: 55%;
        background-repeat: no-repeat;
        background-position: center bottom 20px;
        opacity: 0.50;
        pointer-events: none;
        z-index: 0;
        border-radius: 12px;
    }}
    """

# 3. CSS PARA DESIGN CLEAR E ANIMAÇÃO
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Lato:wght@300;400;700&display=swap');

    .stApp, [data-testid="stAppViewContainer"] {{ background-color: #f9f5f4 !important; }}
    h1, h2, h3, p, span, label, .stSubheader {{ color: #1a1a1a !important; font-family: 'Lato', sans-serif !important; }}

    .titulo-premium {{
        color: #70161e !important;
        font-size: 28px !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2px;
        font-family: 'Cormorant Garamond', serif !important;
        letter-spacing: 1px;
    }}
    .subtitulo-premium {{
        color: #8c1c24 !important;
        font-size: 11px !important;
        text-align: center;
        letter-spacing: 2.5px;
        margin-bottom: 20px;
        font-family: 'Lato', sans-serif !important;
        font-weight: 300;
        text-transform: uppercase;
    }}

    [data-testid="stForm"] {{
        background: #ffffff !important;
        border: 1px solid #e8ddd9 !important;
        border-radius: 12px !important;
        padding: 28px 32px !important;
        box-shadow: 0 4px 24px rgba(112,22,30,0.07) !important;
    }}

    .stTextInput>div>div>input,
    .stSelectbox>div>div>div,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {{
        background-color: #fdfafa !important;
        color: #1a1a1a !important;
        border: 1px solid #ddd0cc !important;
        border-radius: 8px !important;
        font-family: 'Lato', sans-serif !important;
    }}

    div.stButton > button {{
        background-color: #ffffff !important;
        color: #70161e !important;
        border: 2px solid #70161e !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-weight: 700 !important;
        width: 100% !important;
        font-family: 'Lato', sans-serif !important;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }}
    div.stButton > button:hover {{
        background-color: #70161e !important;
        color: #ffffff !important;
    }}

    /* Caixa de destaque para pergunta de contratação */
    .interesse-box {{
        background: linear-gradient(135deg, #70161e08, #70161e14);
        border: 1.5px solid #70161e55;
        border-radius: 10px;
        padding: 18px 22px;
        margin: 10px 0 6px 0;
    }}
    .interesse-label {{
        color: #70161e !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        margin-bottom: 6px;
        font-family: 'Lato', sans-serif !important;
    }}

    @keyframes flyUp {{
        0%   {{ transform: translateY(0) rotate(0deg);   opacity: 1; }}
        100% {{ transform: translateY(-120vh) rotate(360deg); opacity: 0; }}
    }}
    .butterfly-anim {{
        position: fixed;
        font-size: 40px;
        z-index: 9999;
        animation: flyUp 4s linear forwards;
    }}

    {bg_style}
    </style>
    """, unsafe_allow_html=True)

# 4. CABEÇALHO
st.markdown('<p class="titulo-premium">Dra. Lethicia Fernanda 🦋</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo-premium">Advocacia Especializada em Direito da Saúde</p>', unsafe_allow_html=True)
st.divider()

# 5. FUNÇÃO DE ENVIO DE E-MAIL
def enviar_email_gmail(dados):
    remetente = "lethiciafernanda14@gmail.com"
    senha_app = "ozmj zrks dnkk ymks"
    destinatario = "lethiciafernanda.adv@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"NOVA TRIAGEM: {dados['Nome']}"

    interesse_cor = "#2e7d32" if "Sim" in dados.get('Interesse', '') else "#c62828"

    corpo_html = f"""
    <div style="font-family: sans-serif; color: #333; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
        <h2 style="color: #70161e; border-bottom: 2px solid #70161e; padding-bottom: 10px;">Nova Consulta Recebida</h2>
        <p><b>📅 Data:</b> {dados['Data']}</p>
        <p><b>👤 Cliente:</b> {dados['Nome']} | <b>Idade:</b> {dados['Idade']} | <b>Sexo:</b> {dados['Sexo']}</p>
        <p><b>📍 Localidade:</b> {dados['Localidade']}</p>
        <p><b>📱 WhatsApp:</b> {dados['WhatsApp']}</p>
        <hr>
        <h3 style="color: #8c1c24;">Detalhes do Atendimento:</h3>
        <p><b>🏥 Via de Atendimento:</b> {dados['Origem']}</p>
        <p><b>⚖️ Situação Relatada:</b> {dados['Situacao']}</p>
        <p><b>📄 Relatório Médico:</b> {dados['Relatorio']}</p>
        <p><b>🧪 Possui Exames:</b> {dados['Exames']}</p>
        <p><b>🚨 Urgência:</b> {dados['Urgencia']}</p>
        <hr>
        <p style="background:{interesse_cor}18; border-left: 4px solid {interesse_cor}; padding: 10px 14px; border-radius: 6px;">
            <b>💼 Interesse em Contratar:</b> <span style="color:{interesse_cor}; font-weight:bold;">{dados.get('Interesse', 'Não informado')}</span>
        </p>
        <hr>
        <p><b>📝 Resumo do Caso:</b><br>{dados['Detalhes']}</p>
    </div>
    """
    msg.attach(MIMEText(corpo_html, 'html'))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(remetente, senha_app)
        server.send_message(msg)
        server.quit()
        return True, "Ok"
    except Exception as e:
        return False, str(e)

# 6. FORMULÁRIO
with st.form("form_triagem_completo"):
    st.subheader("👤 Seus Dados")
    nome = st.text_input("Nome completo")

    c1, c2 = st.columns(2)
    with c1:
        idade = st.number_input("Idade", min_value=0, value=30)
    with c2:
        sexo = st.selectbox("Sexo:", ["Feminino", "Masculino", "Outro"], index=None)

    tel_raw = st.text_input("WhatsApp (com DDD)", placeholder="Ex: 91988887777")
    localidade = st.text_input("Cidade e Estado")

    nums = re.sub(r'\D', '', tel_raw)
    whatsapp_formatado = f"({nums[:2]}) {nums[2:7]}-{nums[7:]}" if len(nums) >= 10 else nums

    st.divider()
    st.subheader("🏥 Atendimento")
    origem = st.radio("Seu atendimento médico é via:", ["Plano de Saúde", "SUS"], horizontal=True, index=None)
    situacao = st.radio("O que aconteceu?", ["Negativa de tratamento/cirurgia", "Demora excessiva na fila", "Já tenho tudo pronto", "Outro"], index=None)

    st.divider()
    st.subheader("📄 Documentação")
    c3, c4 = st.columns(2)
    with c3:
        tem_relatorio = st.selectbox("Possui Relatório Médico?", ["Sim", "Não", "Em emissão"], index=None)
    with c4:
        tem_exames = st.selectbox("Possui exames?", ["Sim", "Não"], index=None)

    urgencia = st.select_slider("Qual a urgência?", options=["Baixa", "Média", "Alta"], value="Média")
    detalhes = st.text_area("Explique brevemente o caso:")

    # ── NOVA PERGUNTA DE INTERESSE ──────────────────────────────────────────
    st.divider()
    st.markdown('<div class="interesse-box">', unsafe_allow_html=True)
    st.markdown('<p class="interesse-label">💼 Interesse em Contratar os Serviços Jurídicos</p>', unsafe_allow_html=True)
    interesse = st.radio(
        "Após a análise do seu caso, você tem interesse e disponibilidade em contratar os serviços da Dra. Lethicia Fernanda?",
        options=[
            "✅ Sim, tenho interesse e disponibilidade",
            "⏳ Talvez, preciso avaliar melhor",
            "❌ No momento não, apenas quero informações",
        ],
        index=None,
        key="interesse_contratar"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    # ────────────────────────────────────────────────────────────────────────

    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE 🦋")

# 7. PROCESSAMENTO
if btn_enviar:
    if nome and len(nums) >= 10 and origem and situacao and interesse:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")

        dados_finais = {
            "Data": agora, "Nome": nome, "Idade": idade, "Sexo": sexo,
            "WhatsApp": whatsapp_formatado, "Localidade": localidade,
            "Origem": origem, "Situacao": situacao,
            "Relatorio": tem_relatorio, "Exames": tem_exames,
            "Urgencia": urgencia, "Detalhes": detalhes,
            "Interesse": interesse if interesse else "Não informado",
        }

        with st.spinner('Enviando...'):
            arquivo = "leads_completos.csv"
            df_novo = pd.DataFrame([dados_finais])
            if not os.path.isfile(arquivo):
                df_novo.to_csv(arquivo, index=False, sep=';', encoding='utf-8-sig')
            else:
                df_novo.to_csv(arquivo, mode='a', index=False, sep=';', encoding='utf-8-sig', header=False)

            sucesso, erro = enviar_email_gmail(dados_finais)

        if sucesso:
            for i in range(10, 100, 20):
                st.markdown(f'<div class="butterfly-anim" style="left:{i}%; bottom:-10%;">🦋</div>', unsafe_allow_html=True)
            st.success("✅ Recebido! Dra. Lethicia entrará em contato em breve.")
            time.sleep(3)
        else:
            st.error(f"Erro no envio: {erro}")
    else:
        st.warning("⚠️ Preencha os campos obrigatórios (Nome, WhatsApp, Atendimento, Situação e Interesse em Contratar).")
