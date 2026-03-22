import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Triagem Jurídica - Dra. Lethicia Fernanda", page_icon="🦋")

# 2. ESTILO PREMIUM BORDÔ (Visual Profissional)
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

# 3. CABEÇALHO COM LOGO/NOME
st.markdown("""
    <div class="header-bordo">
        <h1 style='color: white; margin:0; font-family: serif;'>Dra. Lethicia Fernanda 🦋</h1>
        <p style='color: #f3dede; font-size: 14px; letter-spacing: 1px;'>ADVOCACIA ESPECIALIZADA EM DIREITO DA SAÚDE</p>
    </div>
    """, unsafe_allow_html=True)

# 4. FUNÇÃO DE ENVIO DE E-MAIL (SMTP OUTLOOK)
def enviar_email_lead(dados):
    remetente = "lethiciafernanda.adv@outlook.com"
    # Sua senha de 16 dígitos configurada após o 2FA
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
        <p><b>Tipo de Atendimento:</b> {dados['origem']}</p>
        <p><b>Situação Relatada:</b> {dados['situacao']}</p>
        <p><b>Possui Relatório Médico:</b> {dados['relatorio']}</p>
        <p><b>Status dos Exames:</b> {dados['exames_status']}</p>
        <p><b>Exames Citados:</b> {dados['exames_lista']}</p>
        <p><b>Urgência do Caso:</b> {dados['urgencia']}</p>
        <hr>
        <p><b>Resumo do Caso:</b><br>{dados['detalhes']}</p>
    </div>
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
        print(f"Erro técnico no envio: {e}")
        return False

# 5. ESTRUTURA DO FORMULÁRIO (CONFORME SOLICITADO)
with st.form("form_triagem_juridica"):
    st.markdown("### 📌 Seus Dados de Contato")
    nome = st.text_input("Nome completo")
    whatsapp_cliente = st.text_input("WhatsApp com DDD")
    localidade = st.text_input("Cidade e Estado")
    
    st.divider()

    st.markdown("### 🏥 Entendendo sua situação")
    origem = st.radio("Seu atendimento médico é via:", ["Plano de Saúde (Particular ou Empresarial)", "SUS (Público)"], index=None)
    situacao = st.radio("Qual dessas situações mais se parece com a sua?", [
        "Meu plano de saúde negou um tratamento/cirurgia", 
        "Aguardo estou fazendo pelo SUS e estou demorando muito",
        "Já tenho tudo pronto e preciso entrar com o processo",
        "Já entrei com processo, mas não estou satisfeito(a)",
        "Outro"
    ], index=None)

    st.divider()

    st.markdown("### 📄 Documentação e Exames")
    tem_relatorio = st.radio("Possui Relatório Médico ou Pedido de Urgência?", ["Sim", "Não", "Em emissão"])
    tem_exames = st.radio("Possui exames que comprovam a necessidade?", ["Sim, atualizados", "Sim, mas antigos", "Não possuo"])
    quais_exames = st.text_input("Quais exames você já tem? (Ex: Ressonância, Laudo...)")

    st.divider()

    st.markdown("### 🚨 Gravidade e Resumo")
    urgencia = st.selectbox("Seu caso é?", ["Sim, preciso resolver o mais rápido possível", "Pode aguardar alguns dias", "Não é urgente"])
    detalhes = st.text_area("Explique seu caso resumidamente:")

    # BOTÃO DE ENVIO
    btn_enviar = st.form_submit_button("ENVIAR PARA ANÁLISE ESPECIALIZADA 🦋")

# 6. LÓGICA DE EXECUÇÃO E FEEDBACK DE SUCESSO
if btn_enviar:
    # Validação simples de campos obrigatórios
    if nome and whatsapp_cliente and origem:
        dados_coletados = {
            "nome": nome, "whatsapp": whatsapp_cliente, "localidade": localidade,
            "origem": origem, "situacao": situacao, "relatorio": tem_relatorio,
            "exames_status": tem_exames, "exames_lista": quais_exames,
            "urgencia": urgencia, "detalhes": detalhes
        }

        # Spinner de carregamento para o cliente esperar o envio
        with st.spinner('Processando sua solicitação...'):
            foi_enviado = enviar_email_lead(dados_coletados)

        if foi_enviado:
            # MENSAGEM DE SUCESSO NA TELA DO CLIENTE
            st.success(f"✅ Sucesso, {nome}! Seus dados foram enviados com segurança para a Dra. Lethicia Fernanda. Em breve entraremos em contato.")
            st.balloons() # Efeito visual opcional de celebração
        else:
            st.error("Houve um erro técnico ao processar o envio por e-mail. Por favor, tente novamente.")
    else:
        st.warning("⚠️ Por favor, preencha os campos obrigatórios (Nome, WhatsApp e Tipo de Atendimento).")
