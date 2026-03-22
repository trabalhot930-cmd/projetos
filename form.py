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
st.set_page_config(page_title="Triagem Jurídica - Dra. Lethicia Fernanda", page_icon="🦋")

# 2. ESTILO E ANIMAÇÃO DE BORBOLETAS
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
    @keyframes fly {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-120vh) rotate(360deg); opacity: 0; }
    }
    .butterfly {
        position: fixed; font-size: 40px; pointer-events: none; z-index: 9999;
        animation: fly 4s linear forwards;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO
st.markdown("""
    <div class="header-bordo">
        <h1 style='color: white; margin:0; font-family: serif;'>Dra. Lethicia Fernanda 🦋</h1>
        <p style='color: #f3dede; font-size: 14px; letter-spacing: 1px;'>ADVOCACIA ESPECIALIZADA EM DIREITO DA SAÚDE</p>
    </div>
    """, unsafe_allow_html=True)

# 4. FUNÇÃO DE ENVIO DE E-MAIL
def enviar_email_gmail(dados):
    remetente = "lethiciafernanda14@gmail.com"
    # COLOQUE SUA SENHA DE 16 LETRAS ABAIXO
    senha_app = "COLOQUE_AQUI_SUA_SENHA" 
    destinatario = "lethiciafernanda.adv@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"NOVA TRIAGEM: {dados['Nome']}"

    corpo_html = f"""
    <div style="font-family: sans-serif; color: #333;">
        <h2 style="color: #70161e;">Nova Consulta Recebida</h2>
        <p><b>Data:</b> {dados['Data']}</p>
        <p><b>Cliente:</b> {dados['Nome']} | <b>Idade:</b> {dados['Idade']} | <b>Sexo:</b> {dados['Sexo']}</p>
        <p><b>WhatsApp:</b> {dados['WhatsApp']}</p>
        <p><b>Localidade:</b> {dados['Localidade']}</p>
        <hr>
        <p><b>Atendimento:</b> {dados['Origem']}</p>
        <p><b>Situação:</b> {dados['Situacao']}</p>
        <p><b>Relatório:</b> {dados['Relatorio']} | <b>Exames:</b> {dados['Exames']}</p>
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
        return True, "Ok"
    except Exception as e:
        return False, str(e)

# 5. FORMULÁRIO
with st.form("form_triagem"):
    st.markdown("### 👤 Seus Dados")
    c1, c2 = st.columns([3, 1])
    with c1: 
        nome = st.text_input("Nome completo")
    with c2: 
        idade = st.number_input("Idade", min_value=0, max_value=110, value=30)
    
    sexo = st.radio("Sexo:", ["Feminino", "Masculino", "Outro"], index=None, horizontal=True)
    
    c3, c4 = st.columns(2)
    with c3: 
        tel_raw = st.text_input("WhatsApp (com DDD)", max_chars=11)
    with c4: 
        localidade = st.text_input("Cidade e Estado")
    
    nums = re.sub(r'\D', '', tel_raw)
    whatsapp_formatado = f"({nums[:2]}) {nums[2:7]}-{nums[7:]}" if len(nums) >= 10 else nums

    st.divider()
    st.markdown("### 🏥 Sobre o Atendimento")
    origem = st.radio("Seu atendimento é via:", ["Plano de Saúde", "SUS"], index=None)
    situacao = st.radio("O que aconteceu?", ["Negativa de tratamento/cirurgia", "Demora excessiva na fila", "Já tenho tudo pronto", "Outro"], index=None)

    st.divider()
    st.markdown("### 📄 Documentação")
    tem_relatorio = st.radio("Possui Relatório Médico?", ["Sim", "Não", "Em emissão"], horizontal=True)
    tem_exames = st.radio("Possui exames atualizados?", ["Sim", "Não"], horizontal=True)
    urgencia = st.selectbox("Qual a urgência?", ["Imediata", "Pode aguardar", "Não é urgente"])
    detalhes = st.text_area("Explique seu caso resumidamente:")

    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE 🦋")

# 6. PROCESSAMENTO
if btn_enviar:
    if nome and len(nums) >= 10 and origem and sexo:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Dicionário de dados sem quebras de linha internas para evitar erros
        dados_finais = {"Data": agora, "Nome": nome, "Idade": idade, "Sexo": sexo, "WhatsApp": whatsapp_formatado, "Localidade": localidade, "Origem": origem, "Situacao": situacao, "Relatorio": tem_relatorio, "Exames": tem_exames, "Urgencia": urgencia, "Detalhes": detalhes}

        with st.spinner('Enviando...'):
            arquivo = "leads_completos.csv"
            df_novo = pd.DataFrame([dados_finais])
            
            # Bloco de salvamento corrigido
            if not os.path.isfile(arquivo):
                df_novo.to_csv(arquivo, index=False, sep=';', encoding='utf-8-sig')
            else:
                df_novo.to_csv(arquivo, mode='a', index=False, sep=';', encoding='utf-8-sig', header=False)
            
            sucesso, erro = enviar_email_gmail(dados_finais)

        if sucesso:
            # Efeito Borboleta 🦋
            for pos in range(10, 100, 20):
                st.markdown(f'<div class="butterfly" style="left:{pos}%; bottom:-10%;">🦋</div>', unsafe_allow_html=True)
            st.success("✅ Recebido! Dra. Lethicia entrará em contato em breve.")
            time.sleep(2)
        else:
            st.error(f"Erro no e-mail: {erro}")
    else:
        st.warning("⚠️ Preencha Nome, Idade, Sexo, WhatsApp e Atendimento.")

# 7. ÁREA ADMINISTRATIVA PRIVADA
st.write("---")
with st.expander("🔐 Área Administrativa"):
    senha_acesso = st.text_input("Senha:", type="password")
    if senha_acesso == "admin123":
        if os.path.exists("leads_completos.csv"):
            df_adm = pd.read_csv("leads_completos.csv", sep=';')
            st.write(f"Total de Leads: {len(df_adm)}")
            st.download_button("📥 Baixar Planilha", df_adm.to_csv(index=False, sep=';',
