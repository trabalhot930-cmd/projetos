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

# 2. CABEÇALHO
st.markdown("# Dra. Lethicia Fernanda 🦋")
st.markdown("### ADVOCACIA ESPECIALIZADA EM DIREITO DA SAÚDE")
st.divider()

# 3. FUNÇÃO DE ENVIO DE E-MAIL
def enviar_email_gmail(dados):
    remetente = "lethiciafernanda14@gmail.com"
    senha_app = "ozmj zrks dnkk ymks" 
    destinatario = "lethiciafernanda.adv@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"NOVA TRIAGEM: {dados['Nome']}"

    corpo_html = f"""
    <div style="font-family: sans-serif; color: #333;">
        <h2>Nova Consulta Recebida</h2>
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

# 4. FORMULÁRIO DE TRIAGEM
with st.form("form_triagem_estavel"):
    st.subheader("👤 Seus Dados")
    
    nome = st.text_input("Nome completo", placeholder="Digite seu nome")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        idade = st.number_input("Idade", min_value=0, max_value=110, value=30)
    with c2:
        sexo = st.selectbox("Sexo:", ["Feminino", "Masculino", "Outro"], index=None, placeholder="Selecione")
    
    tel_raw = st.text_input("WhatsApp (com DDD)", max_chars=11, placeholder="Ex: 91988887777")
    localidade = st.text_input("Cidade e Estado", placeholder="Ex: Belém/PA")
    
    nums = re.sub(r'\D', '', tel_raw)
    whatsapp_formatado = f"({nums[:2]}) {nums[2:7]}-{nums[7:]}" if len(nums) >= 10 else nums

    st.divider()
    st.subheader("🏥 Sobre o Atendimento")
    origem = st.radio("Seu atendimento médico é via:", ["Plano de Saúde", "SUS"], index=None, horizontal=True)
    
    situacao = st.radio("O que aconteceu?", [
        "Negativa de tratamento/cirurgia", 
        "Demora excessiva na fila", 
        "Já tenho tudo pronto", 
        "Outro"
    ], index=None)

    st.divider()
    st.subheader("📄 Documentação e Urgência")
    
    tem_relatorio = st.selectbox("Possui Relatório Médico?", ["Sim", "Não", "Em emissão"], index=None)
    tem_exames = st.selectbox("Possui exames atualizados?", ["Sim", "Não"], index=None)
    urgencia = st.select_slider("Qual a urgência?", options=["Não é urgente", "Pode aguardar", "Imediata"], value="Pode aguardar")
    
    detalhes = st.text_area("Explique seu caso resumidamente (opcional):", height=150)

    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE ESPECIALIZADA 🦋")

# 5. LÓGICA DE PROCESSAMENTO (IDENTAÇÃO CORRIGIDA)
if btn_enviar:
    if nome and len(nums) >= 10 and origem and sexo:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        dados_finais = {
            "Data": agora, "Nome": nome, "Idade": idade, "Sexo": sexo, 
            "WhatsApp": whatsapp_formatado, "Localidade": localidade, 
            "Origem": origem, "Situacao": situacao, "Relatorio": tem_relatorio, 
            "Exames": tem_exames, "Urgencia": urgencia, "Detalhes": detalhes
        }

        with st.spinner('Enviando...'):
            arquivo = "leads_completos.csv"
            df_novo = pd.DataFrame([dados_finais])
            
            # Bloco corrigido para evitar o erro de identação
            if not os.path.isfile(arquivo):
                df_novo.to_csv(arquivo, index=False, sep=';', encoding='utf-8-sig')
            else:
                df_novo.to_csv(arquivo, mode='a', index=False, sep=';', encoding='utf-8-sig', header=False)
            
            sucesso, erro = enviar_email_gmail(dados_finais)

        if sucesso:
            st.balloons()
            st.success("✅ Recebido! Dra. Lethicia entrará em contato em breve.")
            time.sleep(2)
        else:
            st.error(f"Erro no e-mail: {erro}")
    else:
        st.warning("⚠️ Preencha Nome, Idade, Sexo, WhatsApp e Atendimento.")
