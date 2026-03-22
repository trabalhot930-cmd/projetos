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
    # INSIRA A SENHA DE 16 LETRAS GERADA NO GOOGLE (SENHAS DE APP)
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
        <p><b>Idade:</b> {dados['Idade']} | <b>Sexo:</b> {dados['Sexo']}</p>
        <p><b>WhatsApp:</b> {dados['WhatsApp']}</p>
        <p><b>Localidade:</b> {dados['Localidade']}</p>
        <hr>
        <p><b>Atendimento:</b> {dados['Origem']}</p>
        <p><b>Situação:</b> {dados['Situacao']}</p>
        <p><b>Relatório Médico:</b> {dados['Relatorio']}</p>
        <p><b>Status dos Exames:</b> {dados['Status_Exames']}</p>
        <p><b>Quais Exames:</b> {dados['Lista_Exames']}</p>
        <p><b>Urgência:</b> {dados['Urgencia']}</p>
        <hr>
        <p><b>Resumo do Caso:</b><br>{dados['Detalhes']}</p>
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
with st.form("form_triagem_completo"):
    st.markdown("### 👤 Perfil do Cliente")
    c1, c2 = st.columns([3, 1])
    with c1:
        nome = st.text_input("Nome completo")
    with c2:
        idade = st.number_input("Idade", min_value=0, max_value=110, value=30)
    
    sexo = st.radio("Sexo:", ["Feminino", "Masculino", "Outro"], index=None, horizontal=True)
    
    c3, c4 = st.columns(2)
    with c3:
        tel_raw = st.text_input("WhatsApp (com DDD)", max_chars=11, help="Digite apenas números")
    with c4:
        localidade = st.text_input("Cidade e Estado")
    
    # Formatação automática do WhatsApp
    nums = re.sub(r'\D', '', tel_raw)
    whatsapp_formatado = f"({nums[:2]}) {nums[2:7]}-{nums[7:]}" if len(nums) >= 10 else nums

    st.divider()

    st.markdown("### 🏥 Sobre o Atendimento")
    origem = st.radio("Seu atendimento é via:", ["Plano de Saúde", "SUS"], index=None)
    situacao = st.selectbox("Qual dessas situações mais se parece com a sua?", [
        "Meu plano de saúde negou um tratamento/cirurgia", 
        "Estou aguardando pelo SUS e está demorando muito",
        "Já tenho tudo pronto e preciso entrar com o processo",
        "Já entrei com processo, mas não estou satisfeito(a)",
        "Outro"
    ], index=None)

    st.divider()

    st.markdown("### 📄 Documentação e Exames")
    tem_relatorio = st.radio("Possui Relatório Médico ou Pedido de Urgência?", ["Sim", "Não", "Em emissão"], horizontal=True)
    tem_exames = st.radio("Possui exames que comprovam a necessidade?", ["Sim, atualizados", "Sim, mas antigos", "Não possuo"], horizontal=True)
    quais_exames = st.text_input("Quais exames você já tem? (Ex: Ressonância, Laudo, Biópsia...)")

    st.divider()

    st.markdown("### 🚨 Gravidade")
    urgencia = st.selectbox("Seu caso é?", ["Sim, preciso resolver o mais rápido possível", "Pode aguardar alguns dias", "Não é urgente"])
    detalhes = st.text_area("Explique seu caso resumidamente:")

    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE ESPECIALIZADA 🦋")

# 6. PROCESSAMENTO (PLANILHA + E-MAIL)
if btn_enviar:
    # Validação dos campos essenciais
    if nome and len(nums) >= 10 and origem and sexo:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        dados_finais = {
            "Data": agora,
            "Nome": nome,
            "Idade": idade,
            "Sexo": sexo,
            "WhatsApp": whatsapp_formatado,
            "Localidade": localidade,
            "Origem": origem,
            "Situacao": situacao,
            "Relatorio": tem_relatorio,
            "Status_Exames": tem_exames,
            "Lista_Exames": quais_exames,
            "Urgencia": urgencia,
            "Detalhes": detalhes
        }

        with st.spinner('Enviando dados...'):
            # SALVAR NA PLANILHA CSV
            arquivo = "leads_completos.csv"
            df_novo = pd.DataFrame([dados_finais])
            if not os.path.isfile(arquivo):
                df_novo.to_csv(arquivo, index=False, sep=';', encoding='utf-8-sig')
            else:
                df_novo.to_csv(arquivo, mode='a', index=False, sep=';', encoding='utf-8-sig', header=False)

            # ENVIAR E-MAIL
            sucesso, erro = enviar_email_gmail(dados_finais)

        if sucesso:
            st.success(f"✅ Sucesso! Dra. Lethicia recebeu seus dados e entrará em contato em breve.")
            st.balloons()
        else:
            st.error(f"Erro no envio: {erro}")
    else:
        st.warning("⚠️ Por favor, preencha todos os campos do Perfil (Nome, Idade, Sexo e WhatsApp) e o Atendimento.")

# 7. ÁREA ADMINISTRATIVA
with st.expander("📊 Relatório de Público (Uso Interno)"):
    if os.path.exists("leads_completos.csv"):
        df_view = pd.read_csv("leads_completos.csv", sep=';')
        st.write(f"Total de Leads: {len(df_view)}")
        
        c1, c2 = st.columns(2)
        c1.metric("Média de Idade", f"{int(df_view['Idade'].mean())} anos")
        c2.write(df_view['Sexo'].value_counts())
        
        csv_data = df_view.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 Baixar Planilha Completa", csv_data, "relatorio_leads.csv", "text/csv")
