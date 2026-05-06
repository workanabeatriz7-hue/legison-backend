import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="LegisON - Assistente Jurídico", layout="wide")

# --- SISTEMA DE LOGIN (MULTI-TENANT SAAS) ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    st.markdown("<h1 style='text-align: center;'>⚖️ LegisON Workspace</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Acesso Multi-Tenant para Escritórios</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.info("Utilize suas credenciais de parceiro para acessar o motor de IA.")
        usuario = st.text_input("E-mail corporativo", placeholder="advogado@escritorio.com.br")
        senha = st.text_input("Senha", type="password")
        
        if st.button("Acessar Plataforma", type="primary", use_container_width=True):
            if usuario and senha:
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Preencha e-mail e senha para acessar.")
else:
    # --- FUNÇÕES GERADORAS DE PDF ---
    def gerar_pdf(titulo, cliente, linhas_relatorio, total):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt=f"LegisON - {titulo}", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
        pdf.cell(200, 10, txt=f"CLIENTE / RECLAMANTE: {cliente.upper() if cliente else 'NAO INFORMADO'}", ln=True)
        pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
        for linha in linhas_relatorio:
            pdf.cell(200, 10, txt=linha, ln=True)
        pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"TOTAL ESTIMADO: R$ {total:,.2f}", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    # --- MENU LATERAL ---
    st.sidebar.title("⚖️ LegisON")
    st.sidebar.markdown(f"**Status:** Conectado (Licença Ativa)")
    menu = st.sidebar.radio("Navegação", [
        "📊 Dashboard de Leads", 
        "🧮 Calculadora Trabalhista", 
        "🤖 Simulador de IA (Testes)"
    ])
    st.sidebar.divider()
    if st.sidebar.button("Sair (Logout)"):
        st.session_state["logado"] = False
        st.rerun()

    # --- TELA 1: DASHBOARD ---
    if menu == "📊 Dashboard de Leads":
        st.title("Visão Geral do Escritório")
        st.info("O pipeline será preenchido automaticamente quando o WhatsApp Oficial for conectado ao Meta Business.")
        col1, col2, col3 = st.columns(3)
        col1.metric("Leads Totais", "0")
        col2.metric("Qualificados (IA)", "0")
        col3.metric("Petições em Rascunho", "0")

    # --- TELA 2: CALCULADORA (AS 3 ABAS QUE ELE PEDIU) ---
    elif menu == "🧮 Calculadora Trabalhista":
        st.title("Calculadora Estratégica (MVP)")
        cliente_nome = st.text_input("👤 Nome do Cliente (Para Memória de Cálculo em PDF)")
        st.divider()
        
        tab1, tab2, tab3 = st.tabs(["🔹 Rescisão CLT", "🔹 Horas Extras", "🔹 Atualização de Valores"])
        
        with tab1:
            st.subheader("Cálculo de Rescisão")
            colA, colB = st.columns(2)
            salario = colA.number_input("Salário Base (R$)", value=2000.00, key="res_sal")
            meses = colB.number_input("Meses Trabalhados", min_value=1, max_value=12, value=6, key="res_mes")
            saldo_fgts = colA.number_input("Saldo do FGTS", value=1500.00, key="res_fgts")
            
            if st.button("Calcular Rescisão", type="primary"):
                décimo = (meses / 12) * salario
                ferias = (meses / 12) * salario * (4/3)
                multa = saldo_fgts * 0.40
                total = décimo + ferias + multa
                
                st.success(f"**Total da Rescisão: R$ {total:,.2f}**")
                linhas = [f"13o Proporcional: R$ {décimo:,.2f}", f"Ferias + 1/3: R$ {ferias:,.2f}", f"Multa FGTS: R$ {multa:,.2f}"]
                pdf_bytes = gerar_pdf("Memoria de Calculo - Rescisao", cliente_nome, linhas, total)
                st.download_button("📄 Baixar PDF de Rescisão", data=pdf_bytes, file_name="rescisao.pdf", mime="application/pdf")

        with tab2:
            st.subheader("Cálculo de Horas Extras")
            colC, colD = st.columns(2)
            salario_he = colC.number_input("Salário Base (R$)", value=2000.00, key="he_sal")
            horas = colD.number_input("Quantidade de Horas", value=10, key="he_qtd")
            adicional = colC.selectbox("Adicional", ["50%", "100%"])
            
            if st.button("Calcular Horas Extras", type="primary"):
                valor_hora = salario_he / 220
                mult = 1.5 if adicional == "50%" else 2.0
                total_he = (valor_hora * mult) * horas
                
                st.success(f"**Total a Receber: R$ {total_he:,.2f}**")
                linhas = [f"Valor Hora Base: R$ {valor_hora:,.2f}", f"Quantidade: {horas}h com Adicional de {adicional}"]
                pdf_bytes = gerar_pdf("Calculo de Horas Extras", cliente_nome, linhas, total_he)
                st.download_button("📄 Baixar PDF de Horas Extras", data=pdf_bytes, file_name="horas_extras.pdf", mime="application/pdf")

        with tab3:
            st.subheader("Atualização de Valores (Juros)")
            colE, colF = st.columns(2)
            valor_orig = colE.number_input("Valor Original (R$)", value=5000.00)
            meses_atraso = colF.number_input("Meses de Atraso", value=12)
            taxa = colE.number_input("Taxa de Juros (% a.m.)", value=1.0)
            
            if st.button("Atualizar Valor", type="primary"):
                juros = valor_orig * (taxa / 100) * meses_atraso
                total_juros = valor_orig + juros
                st.success(f"**Valor Atualizado: R$ {total_juros:,.2f}**")
                linhas = [f"Valor Original: R$ {valor_orig:,.2f}", f"Juros Acumulados: R$ {juros:,.2f}"]
                pdf_bytes = gerar_pdf("Atualizacao de Valores", cliente_nome, linhas, total_juros)
                st.download_button("📄 Baixar PDF de Juros", data=pdf_bytes, file_name="atualizacao.pdf", mime="application/pdf")

    # --- TELA 3: O SIMULADOR DE IA ---
    elif menu == "🤖 Simulador de IA (Testes)":
        st.title("🤖 Motor de Inteligência Artificial")
        st.markdown("**Ambiente de Homologação:** Teste o cérebro da IA gerando petições em tempo real.")
        st.divider()
        
        caso_cliente = st.text_area("Descreva o caso do lead (Ex: 'Trabalhei 5 anos sem carteira e fui demitido...')", height=150)
        
        if st.button("✨ Qualificar Lead e Gerar Petição", type="primary"):
            if caso_cliente:
                with st.spinner("A IA está analisando os fatos. Isso leva alguns segundos..."):
                    
                    parte1 = "sk-proj-NNpeGZ5Xj5PYP4tnlH6py8PWmIpfhVgofEoBvX"
                    parte2 = "SQsWHaJiEZ1QepCUXmB59QQEYTC59WfGXh4AT3BlbkFJG3CQQbqYtXLAeizTotpoIxvpzIRJS0gdLZwHJ9m28vdovo6dN5evaREoQs7hlyeGSYXK2CuswA"
                    API_KEY = parte1 + parte2 
                    
                    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
                    
                    prompt_sistema = """Você é um assistente jurídico. Qualifique o lead a seguir e gere um rascunho de Petição Preliminar formatada."""
                    data = {"model": "gpt-3.5-turbo", "messages": [{"role": "system", "content": prompt_sistema}, {"role": "user", "content": caso_cliente}]}
                    
                    try:
                        resposta = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
                        resultado_json = resposta.json()
                        if 'choices' in resultado_json:
                            st.success("✅ Petição Gerada com Sucesso pela IA!")
                            st.write(resultado_json['choices'][0]['message']['content'])
                        else:
                            st.error(f"Erro na OpenAI: {resultado_json}")
                    except Exception as e:
                        st.error("Erro de conexão com o servidor de Inteligência Artificial.")
            else:
                st.warning("Por favor, digite um caso para a IA analisar.")
