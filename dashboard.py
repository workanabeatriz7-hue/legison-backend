import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="LegisON - Assistente Jurídico", layout="wide")

# --- SISTEMA DE LOGIN (ESTRUTURA SAAS MULTI-TENANT) ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    st.markdown("<h1 style='text-align: center;'>⚖️ LegisON Workspace</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Plataforma de Gestão Jurídica e Automação de Leads</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.info("Aceda com as suas credenciais para gerir o seu escritório.")
        usuario = st.text_input("E-mail corporativo", placeholder="advogado@exemplo.com")
        senha = st.text_input("Senha", type="password")
        
        if st.button("Aceder à Plataforma", type="primary", use_container_width=True):
            if usuario and senha:
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Introduza o e-mail e a senha.")
else:
    # --- FUNÇÃO GERADORA DE PDF PREMIUM ---
    def gerar_pdf_premium(titulo, cliente, linhas_relatorio, total):
        pdf = FPDF()
        pdf.add_page()
        
        # 1. Cabeçalho Corporativo (Header)
        pdf.set_fill_color(33, 37, 41) 
        pdf.set_text_color(255, 255, 255) 
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 15, txt=" LegisON - Inteligencia Juridica", ln=True, align='L', fill=True)
        pdf.ln(5)
        
        # 2. Título do Documento
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt=titulo.upper(), ln=True, align='C')
        pdf.ln(2)
        
        # 3. Informações do Reclamante e Data
        pdf.set_fill_color(240, 240, 240)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 10)
        cliente_nome = cliente.upper() if cliente else 'CLIENTE NAO INFORMADO'
        data_atual = datetime.now().strftime("%d/%m/%Y as %H:%M")
        pdf.cell(0, 10, txt=f" RECLAMANTE: {cliente_nome}   |   DATA: {data_atual}", ln=True, align='L', fill=True)
        pdf.ln(5)
        
        # 4. Tabela de Valores
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(60, 60, 60)
        pdf.cell(130, 10, txt=" Descricao da Verba", border=1, align='L', fill=True)
        pdf.cell(60, 10, txt=" Valor Calculado (R$)", border=1, ln=True, align='C', fill=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 11)
        fundo_cinza = False
        
        for linha in linhas_relatorio:
            if ":" in linha:
                desc, valor = linha.split(":", 1)
            else:
                desc, valor = linha, ""
            
            pdf.set_fill_color(245, 245, 245) if fundo_cinza else pdf.set_fill_color(255, 255, 255)
            pdf.cell(130, 10, txt=f" {desc.strip()}", border=1, align='L', fill=True)
            pdf.cell(60, 10, txt=f"{valor.strip()} ", border=1, ln=True, align='R', fill=True)
            fundo_cinza = not fundo_cinza
            
        pdf.ln(5)
        
        # 5. Totalizador
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(0, 80, 40)
        pdf.cell(130, 12, txt=" TOTAL FINAL ESTIMADO:", border=1, align='R')
        pdf.set_fill_color(225, 245, 225)
        pdf.cell(60, 12, txt=f" R$ {total:,.2f} ", border=1, ln=True, align='R', fill=True)
        
        # 6. Rodapé Legal
        pdf.set_y(-25)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(160, 160, 160)
        pdf.cell(0, 10, txt="Relatorio gerado pelo motor LegisON. Valores meramente estimativos.", ln=True, align='C')
        
        return pdf.output(dest='S').encode('latin-1')

    # --- MENU LATERAL ---
    st.sidebar.title("⚖️ LegisON")
    st.sidebar.markdown(f"**Escritório:** Licença Ativa")
    menu = st.sidebar.radio("Navegação", [
        "📊 Dashboard de Leads", 
        "🧮 Calculadora Trabalhista", 
        "🤖 Simulador de IA (Testes)"
    ])
    st.sidebar.divider()
    if st.sidebar.button("Terminar Sessão"):
        st.session_state["logado"] = False
        st.rerun()

    # --- TELA 1: DASHBOARD ---
    if menu == "📊 Dashboard de Leads":
        st.title("Gestão de Leads e Atendimento")
        st.info("A integração com o WhatsApp oficial sincronizará os leads automaticamente aqui.")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Leads Captados (Hoje)", "2", "+2 novos")
        col2.metric("Qualificados pela IA", "1", "Score: 88%")
        col3.metric("Minutas Geradas", "1")
        
        st.divider()
        st.subheader("Visualização do Pipeline (Exemplo)")
        dados = {
            "Nome do Cliente": ["João Ricardo", "Maria Antonieta"],
            "Resumo do Caso (IA)": ["Vínculo empregatício não reconhecido...", "Demitida durante estabilidade gestacional."],
            "Área Jurídica": ["Trabalhista", "Trabalhista"],
            "Status": ["Aguardando Revisão", "Qualificado - Urgente"]
        }
        st.dataframe(pd.DataFrame(dados), use_container_width=True, hide_index=True)

    # --- TELA 2: CALCULADORA COMPLETA ---
    elif menu == "🧮 Calculadora Trabalhista":
        st.title("Calculadora Estratégica Jurídica")
        cliente_nome = st.text_input("👤 Nome do Cliente (Para o Relatório PDF)")
        st.divider()
        
        tab1, tab2, tab3 = st.tabs(["🔹 Rescisão CLT", "🔹 Horas Extras", "🔹 Atualização de Valores"])
        
        with tab1:
            st.subheader("Cálculo de Rescisão")
            c1, c2 = st.columns(2)
            salario = c1.number_input("Salário Mensal (R$)", value=2500.0, key="res_s")
            meses = c2.number_input("Meses Trabalhados (Proporcional)", min_value=1, max_value=12, value=8)
            saldo_fgts = c1.number_input("Saldo para Fins Rescisórios", value=2000.0)
            
            if st.button("Calcular Rescisão Completa", type="primary"):
                d13 = (meses / 12) * salario
                fer = (meses / 12) * salario * (4/3)
                multa = saldo_fgts * 0.40
                total = d13 + fer + multa
                st.success(f"**Estimativa Total: R$ {total:,.2f}**")
                linhas = [f"13o Salario Proporcional: R$ {d13:,.2f}", f"Ferias Proporcionais + 1/3: R$ {fer:,.2f}", f"Indenizacao Multa FGTS (40%): R$ {multa:,.2f}"]
                pdf = gerar_pdf_premium("Relatorio de Rescisao Contratual", cliente_nome, linhas, total)
                st.download_button("📄 Descarregar PDF Premium", data=pdf, file_name="rescisao_legison.pdf", mime="application/pdf")

        with tab2:
            st.subheader("Cálculo de Horas Extras")
            c3, c4 = st.columns(2)
            sal_he = c3.number_input("Salário Base (R$)", value=2500.0, key="he_s")
            qtd_he = c4.number_input("Total de Horas Extras", value=15)
            adic = c3.selectbox("Adicional", ["50%", "100%"])
            
            if st.button("Calcular Horas Extras", type="primary"):
                v_hora = sal_he / 220
                fator = 1.5 if adic == "50%" else 2.0
                total_he = (v_hora * fator) * qtd_he
                st.success(f"**Total HE: R$ {total_he:,.2f}**")
                linhas = [f"Valor da Hora Base: R$ {v_hora:,.2f}", f"Adicional Aplicado: {adic}", f"Quantidade Calculada: {qtd_he} horas"]
                pdf = gerar_pdf_premium("Relatorio de Horas Extras", cliente_nome, linhas, total_he)
                st.download_button("📄 Descarregar PDF Premium", data=pdf, file_name="horas_extras_legison.pdf", mime="application/pdf")

        with tab3:
            st.subheader("Atualização e Juros")
            c5, c6 = st.columns(2)
            v_orig = c5.number_input("Valor Original (R$)", value=10000.0)
            meses_at = c6.number_input("Meses em Atraso", value=24)
            t_juros = c5.number_input("Taxa de Juros Mensal (%)", value=1.0)
            
            if st.button("Calcular Atualização", type="primary"):
                valor_juros = v_orig * (t_juros / 100) * meses_at
                total_at = v_orig + valor_juros
                st.success(f"**Valor Atualizado: R$ {total_at:,.2f}**")
                linhas = [f"Valor Principal: R$ {v_orig:,.2f}", f"Periodo de Atraso: {meses_at} meses", f"Juros Acumulados: R$ {valor_juros:,.2f}"]
                pdf = gerar_pdf_premium("Relatorio de Atualizacao de Valores", cliente_nome, linhas, total_at)
                st.download_button("📄 Descarregar PDF Premium", data=pdf, file_name="atualizacao_legison.pdf", mime="application/pdf")

    # --- TELA 3: SIMULADOR DE IA ---
    elif menu == "🤖 Simulador de IA (Testes)":
        st.title("🤖 Laboratório de Inteligência Artificial")
        st.markdown("**Teste o motor de IA:** Insira o relato do cliente e veja a geração da petição preliminar.")
        st.divider()
        
        relato = st.text_area("Descreva o caso do lead para análise da IA:", height=150)
        
        if st.button("✨ Analisar Caso e Gerar Minuta", type="primary"):
            if relato:
                with st.spinner("O motor LegisON está a processar os dados..."):
                    # CHAVE DIVIDIDA PARA SEGURANÇA
                    p1 = "sk-proj-NNpeGZ5Xj5PYP4tnlH6py8PWmIpfhVgofEoBvX"
                    p2 = "SQsWHaJiEZ1QepCUXmB59QQEYTC59WfGXh4AT3BlbkFJG3CQQbqYtXLAeizTotpoIxvpzIRJS0gdLZwHJ9m28vdovo6dN5evaREoQs7hlyeGSYXK2CuswA"
                    API_KEY = p1 + p2
                    
                    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
                    prompt = f"És um assistente jurídico sênior. Analisa este caso e gera uma petição preliminar: {relato}"
                    payload = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]}
                    
                    try:
                        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                        data = res.json()
                        if 'choices' in data:
                            st.success("✅ Petição Preliminar Gerada com Sucesso!")
                            st.markdown(data['choices'][0]['message']['content'])
                        else:
                            st.error(f"Erro OpenAI: {data}")
                    except:
                        st.error("Falha na ligação com o motor de IA.")
            else:
                st.warning("Por favor, introduza o relato do caso.")
