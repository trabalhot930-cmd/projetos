import streamlit as st
import smtplib
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

# 4. FUNÇÃO DE ENVIO DE E-MAIL (SMTP)
def enviar_email_lead(dados):
    remetente = "lethiciafernanda.adv@outlook.com"
    # Sua senha de 16 dígitos gerada após o 2FA
    senha_app = "cjvuqgsztjbgmxek" 
    destinatario = "lethiciafernanda.adv@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"NOVA TRIAGEM: {dados['nome']} ({dados['origem']})"

    corpo_html = f"""
    <div style="font-family: sans-serif; color: #333;">
        <h2 style="color: #70161e;">Nova Consulta Recebida</h2>
        <p><b>Nome do Cliente:</b> {dados['nome']}</p>
        <p><b>WhatsApp:</b> {dados['whatsapp']}</p>
        <p><b>Localidade:</b> {dados['localidade']}</p>
        <hr>
        <p><b>Canal:</b> {dados['origem']}</p>
        <p><b>Situação:</b> {dados['situacao']}</p>
        <p><b>Relatório Médico:</b> {dados['relatorio']}</p>
        <p><b>Status dos Exames:</b> {dados['exames_status']}</p>
        <p><b>Exames Citados:</b> {dados['exames_lista']}</p>
        <p><b>Urgência:</b> {dados['urgencia']}</p>
        <hr>
        <p><b>Resumo do Caso:</b><br>{dados['detalhes']}</p>
    </div>
    """
    msg.attach(MIMEText(corpo_html, 'html'))

    try:
        # Servidor SMTP mais compatível com Outlook/Office 365
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(remetente, senha_app)
        server.send_message(msg)
        server.quit()
        return True, "Enviado"
    except Exception as e:
        return False, str(e)

# 5. FORMULÁRIO
with st.form("form_triagem_juridica"):
    st.markdown("### 📌 Seus Dados")
    nome = st.text_input("Nome completo")
    whatsapp_cliente = st.text_input("WhatsApp com DDD")
    localidade = st.text_input("Cidade e Estado")
    
    st.divider()

    st.markdown("### 🏥 Sobre o Atendimento")
    origem = st.radio("Seu atendimento é via:", ["Plano de Saúde", "SUS"], index=None)
    situacao = st.radio("O que aconteceu?", [
        "Meu plano de saúde negou um tratamento/cirurgia", 
        "Estou aguardando pelo SUS e está demorando muito",
        "Já tenho tudo pronto e preciso entrar com o processo",
        "Já entrei com processo, mas não estou satisfeito(a)",
        "Outro"
    ], index=None)

    st.divider()

    st.markdown("### 📄 Documentação e Exames")
    tem_relatorio = st.radio("Possui Relatório Médico ou Pedido de Urgência?", ["Sim", "Não", "Em emissão"])
    tem_exames = st.radio("Possui exames que comprovam a necessidade?", ["Sim, atualizados", "Sim, mas antigos", "Não possuo"])
    quais_exames = st.text_input("Quais exames você já tem?")

    st.divider()

    st.markdown("### 🚨 Gravidade")
    urgencia = st.selectbox("Seu caso é?", ["Sim, preciso resolver o mais rápido possível", "Pode aguardar um pouco", "Não é urgente"])
    detalhes = st.text_area("Explique seu caso resumidamente:")

    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE ESPECIALIZADA 🦋")

# 6. FEEDBACK FINAL
if btn_enviar:
    if nome and whatsapp_cliente and origem:
        dados_finais = {
            "nome": nome, "whatsapp": whatsapp_cliente, "localidade": localidade,
            "origem": origem, "situacao": situacao, "relatorio": tem_relatorio,
            "exames_status": tem_exames, "exames_lista": quais_exames,
            "urgencia": urgencia, "detalhes": detalhes
        }

        with st.spinner('Enviando dados...'):
            sucesso, erro_detalhado = enviar_email_lead(dados_finais)

        if sucesso:
            st.success(f"✅ Sucesso, {nome}! Seus dados foram enviados. A Dra. Lethicia entrará em contato.")
            st.balloons()
        else:
            st.error(f"Erro no envio: {erro_detalhado}")
            st.info("Dica técnica: Verifique se o e-mail dela recebeu um aviso de 'Login Incomum' da Microsoft e clique em 'Fui eu'.")
    else:
        st.warning("Preencha o Nome, WhatsApp e o Tipo de Atendimento (Plano ou SUS).")
