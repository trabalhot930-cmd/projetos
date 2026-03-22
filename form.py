import streamlit as st
import smtplib
import re
import pandas as pd
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Triagem Jurídica - Dra. Lethicia Fernanda", page_icon="🦋")

# 2. ESTILO PREMIUM BORDÔ
st.markdown("""
    <style>
    .stApp { background-color: #fdfafb; }
    .header-bordo {
        background: linear-gradient(90deg, #70161e, #8c1c24);
        padding: 40px; text-align: center; border-radius: 15px; margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%; background-color: #70161e; color: white; 
        font-weight: bold; padding: 18px; border-radius: 10px; border: none;
    }
    .stButton>button:hover { background-color: #5a1218; border: 1px solid white; }
    h3 { color: #70161e !important; padding-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO
st.markdown("""
    <div class="header-bordo">
        <h1 style='color: white; margin:0; font-family: serif;'>Dra. Lethicia Fernanda 🦋</h1>
        <p style='color: #f3dede; font-size: 14px; letter-spacing: 1px;'>ADVOCACIA ESPECIALIZADA EM DIREITO DA SAÚDE</p>
    </div>
    """, unsafe_allow_html=True)

# 4. FUNÇÃO DE ENVIO DE E-MAIL (GMAIL)
def enviar_email_gmail(dados):
    remetente = "lethiciafernanda14@gmail.com"
    # IMPORTANTE: Use a senha de 16 letras gerada no Google (Senhas de App)
    senha_app = "SUA_SENHA_DE_16_LETRAS_AQUI" 
    destinatario = "lethiciafernanda.adv@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"NOVA TRIAGEM: {dados['Nome']} ({dados['Idade']} anos)"

    corpo_html = f"""
    <div style="font-family: sans-serif; color: #333;">
        <h2 style="color: #70161e;">Nova Consulta Recebida</h2>
        <p><b>Data:</b> {dados['Data']}</p>
        <p><b>Nome:</b> {dados['Nome']}</p>
        <p><b>Idade:</b> {dados['Idade']} anos | <b>Sexo:</b> {dados['Sexo']}</p>
        <p><b>WhatsApp:</b> {dados['WhatsApp']}</p>
        <p><b>Localidade:</b> {dados['Localidade']}</p>
        <hr>
        <p><b>Atendimento:</b> {dados['Origem']}</p>
        <p><b>Situação:</b> {dados['Situacao']}</p>
        <p><b>Relatório Médico:</b> {dados['Relatorio']}</p>
        <p><b>Exames:</b> {dados['Status_Exames']}</p>
        <p><b>Urgência:</b> {dados['Urgencia']}</p>
        <hr>
        <p><b>Resumo:</b><br>{dados['Detalhes']}</p>
    </div>
    """
    msg.attach(MIMEText(corpo_html, 'html'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(remetente, senha_app)
        server.send_message(msg)
        server.quit()
        return True, "Enviado"
    except Exception as e:
        return False, str(e)

# 5. FORMULÁRIO DE TRIAGEM COMPLETO
with st.form("form_triagem"):
    st.markdown("### 👤 Perfil do Cliente")
    c1, c2 = st.columns([3, 1])
    with c1:
        nome = st.text_input("Nome completo")
    with c2:
        idade = st.number_input("Idade", min_value=0, max_value=110, value=30)
    
    sexo = st.radio("Sexo:", ["Feminino", "Masculino", "Outro"], index=None, horizontal=True)
    
    c3, c4 = st.columns(2)
    with c3:
        tel_raw = st.text_input("WhatsApp (com DDD)", max_chars=11, help="Apenas números")
    with c4:
        localidade = st.text_input("Cidade e Estado")
    
    # Lógica de formatação do WhatsApp (XX) XXXXX-XXXX
    nums = re.sub(r'\D', '', tel_raw)
    whatsapp_formatado = f"({nums[:2]}) {nums[2:7]}-{nums[7:]}" if len(nums) >= 10 else nums

    st.divider()

    st.markdown("### 🏥 Sobre o Atendimento")
    origem = st.radio("Seu atendimento é via:", ["Plano de Saúde", "SUS"], index=None)
    situacao = st.selectbox("O que aconteceu?", [
        "Meu plano de saúde negou um tratamento/cirurgia", 
        "Estou aguardando pelo SUS e está demorando muito",
        "Já tenho tudo pronto e preciso entrar com o processo",
        "Já entrei com processo, mas não estou satisfeito(a)",
        "Outro"
    ], index=None)

    st.divider()

    st.markdown("### 📄 Documentação e Urgência")
    tem_relatorio = st.radio("Possui Relatório Médico ou Pedido de Urgência?", ["Sim", "Não", "Em emissão"], horizontal=True)
    tem_exames = st.radio("Possui exames atualizados?", ["Sim", "Não"], horizontal=True)
    urgencia = st.selectbox("Qual a urgência?", ["Imediata", "Pode aguardar", "Não é urgente"])
    
    detalhes = st.text_area("Explique seu caso resumidamente:")
