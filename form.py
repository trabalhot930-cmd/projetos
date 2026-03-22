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
    # Lembre-se de inserir a senha de 16 letras gerada no Google aqui
    senha_app = "COLOQUE_AQUI_SUA_SENHA_DE_16_LETRAS" 
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
        <p><b>Idade:</b> {dados['Idade']} anos</p>
        <p><b>Sexo:</b> {dados['Sexo']}</p>
        <p><b>WhatsApp:</b> {dados['WhatsApp']}</p>
        <p><b>Localidade:</b> {dados['Localidade']}</p>
        <hr>
        <p><b>Atendimento:</b> {dados['Origem']}</p>
        <p><b>Situação:</b> {dados['Situacao']}</p>
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

# 5. FORMULÁRIO DE TRIAGEM
with st.form("form_triagem_publico"):
    st.markdown("### 👤 Perfil do Cliente")
    col1, col2 = st.columns([2, 1])
    with col1:
        nome = st.text_input("Nome completo")
    with col2:
        idade = st.number_input("Idade", min_value=0, max_value=120, value=30)
    
    sexo = st.radio("Sexo:", ["Feminino", "Masculino", "Prefiro não informar"], index=None, horizontal=True)
    
    col3, col4 = st.columns(2)
    with col3:
        tel_raw = st.text_input("WhatsApp (com DDD)", max_chars=11, help="Apenas números")
    with col4:
        localidade = st.text_input("Cidade/Estado")
    
    # Lógica de formatação (XX) XXXXX-XXXX
    nums = re.sub(r'\D', '', tel_raw)
    whatsapp_formatado = f"({nums[:2]}) {nums[2:7]}-{nums[7:]}" if len(nums) >= 10 else nums

    st.divider()

    st.markdown("### 🏥 Sobre o Atendimento")
    origem = st.radio("Atendimento via:", ["Plano de Saúde", "SUS"], index=None)
    situacao = st.selectbox("O que aconteceu?", [
        "Negativa de tratamento/cirurgia pelo Plano", 
        "Demora excessiva na fila do SUS",
        "Home Care / Medicamentos de alto custo",
        "Reajuste abusivo de mensalidade",
        "Outro"
    ], index=None)

    detalhes = st.text_area("Descreva brevemente o seu caso:")

    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE 🦋")

# 6. PROCESSAMENTO
if btn_enviar:
    if nome and len(nums) >= 10 and origem and sexo:
        dados_finais = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Nome": nome,
            "Idade": idade,
            "Sexo": sexo,
            "WhatsApp": whatsapp_formatado,
            "Localidade": localidade,
            "Origem": origem,
            "Situacao": situacao,
            "Detalhes": detalhes
        }

        with st.spinner('Salvando dados...'):
            # SALVAR NA PLANILHA CSV
            arquivo = "leads_com_perfil.csv"
            df_novo = pd.DataFrame([dados_finais])
            if not os.path.isfile(arquivo):
                df_novo.to_csv(arquivo, index=False, sep=';', encoding='utf-8-sig')
            else:
                df_novo.to_csv(arquivo, mode='a', index=False, sep=';', encoding='utf-8-sig', header=False)

            # ENVIAR E-MAIL
            sucesso, erro = enviar_email_gmail(dados_finais)

        if sucesso:
            st.success(f"✅ Recebido! Dra. Lethicia entrará em contato com você em breve.")
            st.balloons()
        else:
            st.error(f"Erro no envio: {erro}")
    else:
        st.warning("⚠️ Preencha Nome, Idade, Sexo, WhatsApp e Atendimento.")

# 7. DASHBOARD SIMPLES (EXPANSÍVEL)
with st.expander("📊 Relatório de Público (ADM)"):
    if os.path.exists("leads_com_perfil.csv"):
        df = pd.read_csv("leads_com_perfil.csv", sep=';')
        st.write(f"Total de Leads: {len(df)}")
        
        # Mini estatística para a Dra. Lethicia
        c1, c2 = st.columns(2)
        c1.metric("Média de Idade", f"{int(df['Idade'].mean())} anos")
        c2.write(df['Sexo'].value_counts())
        
        csv = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 Baixar Planilha Completa", csv, "leads_perfil.csv", "text/csv")
