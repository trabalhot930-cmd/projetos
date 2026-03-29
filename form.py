import streamlit as st
import smtplib
import re
import pandas as pd
import os
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Triagem Jurídica - Dra. Lethicia Fernanda",
    page_icon="🦋",
    layout="centered"
)

# 2. CSS PARA DESIGN CLEAR E ANIMAÇÃO
st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
    h1, h2, h3, p, span, label, .stSubheader { color: #1a1a1a !important; }

    .titulo-premium {
        color: #70161e !important; font-size: 24px !important;
        font-weight: bold; text-align: center; margin-bottom: 5px;
    }
    .subtitulo-premium {
        color: #8c1c24 !important; font-size: 11px !important;
        text-align: center; letter-spacing: 1px; margin-bottom: 20px;
    }

    .stTextInput>div>div>input, .stSelectbox>div>div>div, 
    .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background-color: #ffffff !important; color: #1a1a1a !important;
        border: 1px solid #dddddd !important; border-radius: 8px !important;
    }

    div.stButton > button {
        background-color: #ffffff !important; color: #70161e !important;
        border: 2px solid #70161e !important; border-radius: 8px !important;
        padding: 12px !important; font-weight: bold !important; width: 100% !important;
    }
    div.stButton > button:hover { background-color: #70161e !important; color: #ffffff !important; }

    @keyframes flyUp {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-120vh) rotate(360deg); opacity: 0; }
    }
    .butterfly-anim {
        position: fixed; font-size: 40px; z-index: 9999;
        animation: flyUp 4s linear forwards;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO
st.markdown('<p class="titulo-premium">Dra. Lethicia Fernanda 🦋</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo-premium">ADVOCACIA ESPECIALIZADA EM DIREITO DA SAÚDE</p>', unsafe_allow_html=True)
st.divider()

# 4. FUNÇÃO DE ENVIO DE E-MAIL (AGORA COM TODOS OS CAMPOS)
def enviar_email_gmail(dados):
    remetente = "lethiciafernanda14@gmail.com"
    senha_app = "ozmj zrks dnkk ymks" 
    destinatario = "lethiciafernanda.adv@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"NOVA TRIAGEM: {dados['Nome']}"

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

# 5. FORMULÁRIO
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

    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE 🦋")

# 6. PROCESSAMENTO
if btn_enviar:
    if nome and len(nums) >= 10 and origem and situacao:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Coleta de TODOS os dados para o dicionário
        dados_finais = {
            "Data": agora, "Nome": nome, "Idade": idade, "Sexo": sexo, 
            "WhatsApp": whatsapp_formatado, "Localidade": localidade, 
            "Origem": origem, "Situacao": situacao, 
            "Relatorio": tem_relatorio, "Exames": tem_exames, 
            "Urgencia": urgencia, "Detalhes": detalhes
        }

        with st.spinner('Enviando...'):
            # Salvar no CSV
            arquivo = "leads_completos.csv"
            df_novo = pd.DataFrame([dados_finais])
            if not os.path.isfile(arquivo):
                df_novo.to_csv(arquivo, index=False, sep=';', encoding='utf-8-sig')
            else:
                df_novo.to_csv(arquivo, mode='a', index=False, sep=';', encoding='utf-8-sig', header=False)
            
            sucesso, erro = enviar_email_gmail(dados_finais)

        if sucesso:
            # Borboletas 🦋
            for i in range(10, 100, 20):
                st.markdown(f'<div class="butterfly-anim" style="left:{i}%; bottom:-10%;">🦋</div>', unsafe_allow_html=True)
            st.success("✅ Recebido! Dra. Lethicia entrará em contato em breve.")
            time.sleep(3)
        else:
            st.error(f"Erro no envio: {erro}")
    else:
        st.warning("⚠️ Preencha os campos obrigatórios (Nome, WhatsApp, Atendimento e Situação).")
