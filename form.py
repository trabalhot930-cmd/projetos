import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Triagem Jurídica - Dra. Lethicia Fernanda", page_icon="🦋")

# 2. ESTILO PREMIUM BORDÔ (CSS)
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
    .stButton>button:hover { background-color: #5a1218; }
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
    # Sua Senha de App de 25 dígitos gerada na conta Microsoft
    senha_app = "WMUPP-SK3Q3-GKSC2-Z3GS6-65UYM" 
    destinatario = "lethiciafernanda.adv@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"NOVO FORMULÁRIO: {dados['nome']} ({dados['origem']})"

    corpo_html = f"""
    <h3>Dados da Triagem - Direito da Saúde</h3>
    <p><b>Nome:</b> {dados['nome']}</p>
    <p><b>WhatsApp:</b> {dados['whatsapp']}</p>
    <p><b>Localidade:</b> {dados['localidade']}</p>
    <hr>
    <p><b>Canal:</b> {dados['origem']}</p>
    <p><b>Situação:</b> {dados['situacao']}</p>
    <p><b>Relatório Médico/Urgência:</b> {dados['relatorio']}</p>
    <p><b>Status dos Exames:</b> {dados['exames_status']}</p>
    <p><b>Lista de Exames:</b> {dados['exames_lista']}</p>
    <p><b>Urgência:</b> {dados['urgencia']}</p>
    <hr>
    <p><b>Resumo do Caso:</b><br>{dados['detalhes']}</p>
    """
    msg.attach(MIMEText(corpo_html, 'html'))

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(remetente, senha_app)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Erro no envio: {e}")
        return False

# 5. FORMULÁRIO DE TRIAGEM
with st.form("form_triagem"):
    st.markdown("### 📌 Seus Dados")
    nome = st.text_input("Nome completo")
    whatsapp_cliente = st.text_input("WhatsApp com DDD")
    localidade = st.text_input("Cidade e Estado")
    
    st.divider()

    st.markdown("### 🏥 Sobre o Atendimento")
    origem = st.radio("Seu atendimento é via:", ["Plano de Saúde", "SUS"], index=None)
    situacao = st.radio("O que aconteceu?", [
        "Negativa de tratamento/cirurgia", 
        "Demora excessiva na fila",
        "Já tenho tudo pronto e preciso entrar com o processo",
        "Outro"
    ], index=None)

    st.divider()

    st.markdown("### 📄 Documentação e Exames")
    tem_relatorio = st.radio("Possui Relatório Médico ou Pedido de Urgência?", ["Sim", "Não", "Em emissão"])
    tem_exames = st.radio("Possui exames que comprovam a necessidade?", ["Sim, atualizados", "Sim, mas antigos", "Não possuo"])
    quais_exames = st.text_input("Quais exames você já tem?")

    st.divider()

    st.markdown("### 🚨 Gravidade")
    urgencia = st.selectbox("Qual a urgência do caso?", ["Imediata", "Pode aguardar alguns dias", "Não é urgente"])
    detalhes = st.text_area("Explique seu caso resumidamente:")

    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE ESPECIALIZADA 🦋")

# 6. LÓGICA DE FINALIZAÇÃO (PÓS-BOTÃO)
if btn_enviar:
    if nome and whatsapp_cliente and origem:
        dados_finais = {
            "nome": nome, "whatsapp": whatsapp_cliente, "localidade": localidade,
            "origem": origem, "situacao": situacao, "relatorio": tem_relatorio,
            "exames_status": tem_exames, "exames_lista": quais_exames,
            "urgencia": urgencia, "detalhes": detalhes
        }

        with st.spinner('Enviando para a Dra. Lethicia...'):
            sucesso = enviar_email_lead(dados_finais)

        if sucesso:
            st.success(f"✅ Sucesso, {nome}! Seus dados foram enviados. A Dra. Lethicia analisará e entrará em contato em breve.")
        else:
            st.error("Houve um erro técnico no envio. Por favor, tente novamente em alguns instantes.")
    else:
        st.error("Por favor, preencha o Nome, WhatsApp e tipo de atendimento.")
