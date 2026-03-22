import streamlit as st
import smtplib
import re
import pandas as pd
import os
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. CONFIGURAÇÃO DA PÁGINA E FORÇAR TEMA CLARO
st.set_page_config(
    page_title="Triagem Jurídica - Dra. Lethicia Fernanda",
    page_icon="🦋",
    layout="centered"
)

# 2. CSS PARA FORÇAR FUNDO CLARO, AJUSTAR FONTES E ANIMAÇÃO
st.markdown("""
    <style>
    /* Forçar fundo claro e cor do texto */
    .stApp {
        background-color: #fdfafb !important;
        color: #333333 !important;
    }
    
    /* Ajustar Título (Dra. Lethicia Fernanda) para não ficar gigante */
    .titulo-premium {
        color: #70161e;
        font-family: 'Serif', 'Times New Roman';
        font-size: 28px !important;
        font-weight: bold;
        text-align: center;
        margin-top: -20px;
    }
    
    .subtitulo-premium {
        color: #8c1c24;
        font-size: 12px !important;
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }

    /* Estilo dos campos de entrada */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: white !important;
        color: #333 !important;
    }

    /* Animação das Borboletas */
    @keyframes flyUp {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-120vh) rotate(360deg); opacity: 0; }
    }
    .butterfly-anim {
        position: fixed;
        font-size: 40px;
        z-index: 9999;
        animation: flyUp 4s linear forwards;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO PERSONALIZADO
st.markdown('<p class="titulo-premium">Dra. Lethicia Fernanda 🦋</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo-premium">ADVOCACIA ESPECIALIZADA EM DIREITO DA SAÚDE</p>', unsafe_allow_html=True)
st.divider()

# 4. FUNÇÃO DE ENVIO DE E-MAIL
def enviar_email_gmail(dados):
    remetente = "lethiciafernanda14@gmail.com"
    senha_app = "ozmj zrks dnkk ymks" 
    destinatario = "lethiciafernanda.adv@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"NOVA TRIAGEM: {dados['Nome']}"

    corpo_html = f"""
    <div style="font-family: sans-serif; color: #333; background-color: #fff; padding: 20px;">
        <h2 style="color: #70161e;">Nova Consulta Recebida</h2>
        <p><b>Data:</b> {dados['Data']}</p>
        <p><b>Cliente:</b> {dados['Nome']} | <b>Idade:</b> {dados['Idade']}</p>
        <p><b>WhatsApp:</b> {dados['WhatsApp']}</p>
        <hr>
        <p><b>Situação:</b> {dados['Situacao']}</p>
        <p><b>Urgência:</b> {dados['Urgencia']}</p>
        <p><b>Resumo:</b><br>{dados['Detalhes']}</p>
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
with st.form("form_triagem_final"):
    st.subheader("👤 Seus Dados")
    nome = st.text_input("Nome completo")
    
    col1, col2 = st.columns(2)
    with col1:
        idade = st.number_input("Idade", min_value=0, value=30)
    with col2:
        sexo = st.selectbox("Sexo:", ["Feminino", "Masculino", "Outro"], index=None)
    
    tel_raw = st.text_input("WhatsApp (com DDD)", placeholder="91988887777")
    localidade = st.text_input("Cidade e Estado")
    
    nums = re.sub(r'\D', '', tel_raw)
    whatsapp_formatado = f"({nums[:2]}) {nums[2:7]}-{nums[7:]}" if len(nums) >= 10 else nums

    st.divider()
    st.subheader("🏥 Sobre o Atendimento")
    origem = st.radio("Atendimento via:", ["Plano de Saúde", "SUS"], horizontal=True)
    situacao = st.radio("O que aconteceu?", ["Negativa de tratamento", "Demora na fila", "Já tenho documentos", "Outro"])

    st.divider()
    urgencia = st.select_slider("Qual a urgência?", options=["Baixa", "Média", "Imediata"], value="Média")
    detalhes = st.text_area("Resumo do caso:")

    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE 🦋")

# 6. PROCESSAMENTO E EFEITO DE BORBOLETAS
if btn_enviar:
    if nome and len(nums) >= 10:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        dados_finais = {"Data": agora, "Nome": nome, "Idade": idade, "Sexo": sexo, "WhatsApp": whatsapp_formatado, "Localidade": localidade, "Origem": origem, "Situacao": situacao, "Urgencia": urgencia, "Detalhes": detalhes}

        with st.spinner('Enviando...'):
            # Salvar CSV
            arquivo = "leads_completos.csv"
            df_novo = pd.DataFrame([dados_finais])
            if not os.path.isfile(arquivo):
                df_novo.to_csv(arquivo, index=False, sep=';', encoding='utf-8-sig')
            else:
                df_novo.to_csv(arquivo, mode='a', index=False, sep=';', encoding='utf-8-sig', header=False)
            
            sucesso, erro = enviar_email_gmail(dados_finais)

        if sucesso:
            # CRIAR BORBOLETAS NA TELA 🦋
            for i in range(10, 100, 20):
                st.markdown(f'<div class="butterfly-anim" style="left:{i}%; bottom:-10%;">🦋</div>', unsafe_allow_html=True)
            
            st.success("✅ Recebido! Dra. Lethicia entrará em contato em breve.")
            time.sleep(3)
        else:
            st.error(f"Erro: {erro}")
    else:
        st.warning("⚠️ Preencha os campos obrigatórios.")
