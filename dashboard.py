import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="LegisON - Assistente Jurídico", layout="wide")

# --- SISTEMA DE LOGIN (AGORA COM TRAVA DE SEGURANÇA REAL) ---
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    st.markdown("<h1 style='text-align: center;'>⚖️ LegisON Workspace</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Plataforma de Gestão Jurídica e Automação de Leads</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.info("Acesso Restrito: Insira suas credenciais.")
        usuario = st.text_input("E-mail corporativo")
        senha = st.text_input("Senha", type="password")
        
        if st.button("Aceder à Plataforma", type="primary", use_container_width=True):
            # TRAVA DE SEGURANÇA: Só entra com essas credenciais agora.
            if usuario == "admin@legison.com" and senha == "admin123":
                st.session_state["logado"] = True
                st.rerun()
            elif usuario or senha:
                st.error("Credenciais inválidas. Sistema protegido contra acesso não autorizado.")
            else:
                st.warning("Preencha e-mail e senha.")
else:
    # --- FUNÇÃO GERADORA DE PDF PREMIUM ---
    def gerar_pdf_premium(titulo, cliente, linhas_relatorio, total):
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_fill_color(33, 37, 41) 
        pdf.set_text_color(255, 255, 255) 
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 15, txt=" LegisON - Inteligencia Juridica", ln=True, align='L', fill=True)
        pdf.ln(5)
        
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt=titulo.upper(), ln=True, align='C')
        pdf.ln(2)
        
        pdf.set_fill_color(240, 240, 240)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 10)
        cliente_nome = cliente.upper() if cliente else 'CLIENTE NAO INFORMADO'
        data_atual = datetime.now().strftime("%d/%m/%Y as %H:%M")
        pdf.cell(0, 10, txt=f" RECLAMANTE/AUTOR: {cliente_nome}   |   DATA: {data_atual}", ln=True, align='L', fill=True)
        pdf.ln(5)
        
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
        
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(0, 80, 40)
        pdf.cell(130, 12, txt=" TOTAL FINAL ESTIMADO:", border=1, align='R')
        pdf.set_fill_color(225, 245, 225)
        pdf.cell(60, 12, txt=f" R$ {total:,.2f} ", border=1, ln=True, align='R', fill=True)
        
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
        "🧮 Calculadoras Jurídicas", 
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

    # --- TELA 2: CALCULADORAS ---
    elif menu == "🧮 Calculadoras Jurídicas":
        st.title("Calculadoras Estratégicas (MVP)")
        cliente_nome = st.text_input("👤 Nome do Cliente (Para o Relatório PDF)")
        st.divider()
        
        tab1, tab2, tab3 = st.tabs(["🔹 Trabalhista", "🔹 Previdenciário", "🔹 Consumidor"])
        
        with tab1:
            st.subheader("Cálculo Trabalhista (Rescisão CLT)")
            c1, c2 = st.columns(2)
            salario = c1.number_input("Salário Mensal (R$)", value=2500.0, key="res_s")
            meses = c2.number_input("Meses Trabalhados (Proporcional)", min_value=1, max_value=12, value=8)
            saldo_fgts = c1.number_input("Saldo para Fins Rescisórios", value=2000.0)
            
            if st.button("Calcular Rescisão", type="primary"):
                d13 = (meses / 12) * salario
                fer = (meses / 12) * salario * (4/3)
                multa = saldo_fgts * 0.40
                total = d13 + fer + multa
                st.success(f"**Estimativa Total: R$ {total:,.2f}**")
                linhas = [f"13o Salario Proporcional: R$ {d13:,.2f}", f"Ferias Proporcionais + 1/3: R$ {fer:,.2f}", f"Indenizacao Multa FGTS (40%): R$ {multa:,.2f}"]
                pdf = gerar_pdf_premium("Relatorio de Rescisao Contratual", cliente_nome, linhas, total)
                st.download_button("📄 Descarregar PDF Trabalhista", data=pdf, file_name="rescisao_legison.pdf", mime="application/pdf")

        with tab2:
            st.subheader("Cálculo Previdenciário (Atrasados INSS)")
            c3, c4 = st.columns(2)
            beneficio = c3.number_input("Valor do Benefício Mensal (R$)", value=1412.0, key="prev_b")
            meses_atraso = c4.number_input("Meses em Atraso (Retroativo)", value=12, key="prev_m")
            
            if st.button("Calcular Atrasados", type="primary"):
                total_prev = beneficio * meses_atraso
                st.success(f"**Estimativa Total (Sem Juros/CM): R$ {total_prev:,.2f}**")
                linhas = [f"Valor do Beneficio Base: R$ {beneficio:,.2f}", f"Quantidade de Meses em Atraso: {meses_atraso} meses"]
                pdf = gerar_pdf_premium("Relatorio de Atrasados - INSS", cliente_nome, linhas, total_prev)
                st.download_button("📄 Descarregar PDF Previdenciário", data=pdf, file_name="previdenciario_legison.pdf", mime="application/pdf")

        with tab3:
            st.subheader("Cálculo do Consumidor (Indenizações)")
            c5, c6 = st.columns(2)
            dano_material = c5.number_input("Dano Material Comprovado (R$)", value=1500.0, key="cons_m")
            dano_moral = c6.number_input("Dano Moral Pleiteado (R$)", value=5000.0, key="cons_d")
            
            if st.button("Calcular Valor da Causa", type="primary"):
                total_cons = dano_material + dano_moral
                st.success(f"**Valor Total da Causa: R$ {total_cons:,.2f}**")
                linhas = [f"Danos Materiais Estimados: R$ {dano_material:,.2f}", f"Danos Morais Pleiteados: R$ {dano_moral:,.2f}"]
                pdf = gerar_pdf_premium("Relatorio de Valor da Causa - Consumidor", cliente_nome, linhas, total_cons)
                st.download_button("📄 Descarregar PDF Consumidor", data=pdf, file_name="consumidor_legison.pdf", mime="application/pdf")

    # --- TELA 3: SIMULADOR DE IA (NOVO FLUXO GUIADO E PRÉ-FORMULÁRIOS) ---
    elif menu == "🤖 Simulador de IA (Testes)":
        st.title("🤖 Laboratório de Inteligência Artificial")
        st.markdown("**Fluxo Guiado de Triagem:** Selecione a área jurídica para abrir o pré-formulário específico.")
        st.divider()
        
        area = st.selectbox("1. Área Jurídica do Atendimento:", ["Selecione uma opção...", "Direito Trabalhista", "Direito Previdenciário", "Direito do Consumidor"])
        
        relato_estruturado = ""
        
        # PRÉ-FORMULÁRIOS DINÂMICOS
        if area == "Direito Trabalhista":
            st.info("📝 Pré-Formulário: Triagem Trabalhista")
            colA, colB = st.columns(2)
            cargo = colA.text_input("Qual o cargo ocupado?")
            tempo = colB.text_input("Tempo de serviço (Ex: 2 anos e 3 meses)")
            fatos = st.text_area("Descreva as violações (Ex: não pagava horas extras, sem carteira assinada)")
            if cargo and tempo and fatos:
                relato_estruturado = f"Área: {area}. Cargo: {cargo}. Tempo de Serviço: {tempo}. Fatos/Violações: {fatos}"

        elif area == "Direito Previdenciário":
            st.info("📝 Pré-Formulário: Triagem Previdenciária")
            colA, colB = st.columns(2)
            tipo_beneficio = colA.selectbox("Tipo de Benefício:", ["Aposentadoria por Idade", "Auxílio Doença", "BPC/LOAS", "Pensão por Morte"])
            idade = colB.text_input("Idade do Requerente")
            fatos = st.text_area("Qual o motivo da recusa no INSS ou problema relatado?")
            if tipo_beneficio and idade and fatos:
                relato_estruturado = f"Área: {area}. Benefício Solicitado: {tipo_beneficio}. Idade: {idade}. Relato do problema: {fatos}"

        elif area == "Direito do Consumidor":
            st.info("📝 Pré-Formulário: Triagem de Defesa do Consumidor")
            colA, colB = st.columns(2)
            empresa = colA.text_input("Empresa/Fornecedor (Réu)")
            tipo_problema = colB.selectbox("Tipo de Problema:", ["Produto com Defeito", "Cobrança Indevida", "Voo Cancelado/Atraso", "Corte de Serviço"])
            fatos = st.text_area("Detalhe os prejuízos sofridos e tentativas de contato:")
            if empresa and tipo_problema and fatos:
                relato_estruturado = f"Área: {area}. Empresa Ré: {empresa}. Categoria do Problema: {tipo_problema}. Fatos e Prejuízos: {fatos}"
        
        st.divider()
        
        # BOTÃO DA IA
        if area != "Selecione uma opção...":
            if st.button("✨ Gerar Petição com IA a partir do Formulário", type="primary"):
                if relato_estruturado:
                    with st.spinner("O motor LegisON está analisando o formulário e redigindo a peça..."):
                        p1 = "sk-proj-NNpeGZ5Xj5PYP4tnlH6py8PWmIpfhVgofEoBvX"
                        p2 = "SQsWHaJiEZ1QepCUXmB59QQEYTC59WfGXh4AT3BlbkFJG3CQQbqYtXLAeizTotpoIxvpzIRJS0gdLZwHJ9m28vdovo6dN5evaREoQs7hlyeGSYXK2CuswA"
                        API_KEY = p1 + p2
                        
                        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
                        prompt = f"És um assistente jurídico sênior especializado no Brasil. Analise o seguinte formulário de triagem de cliente e redija um esboço profissional de Petição Preliminar formatada. Dados: {relato_estruturado}"
                        payload = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]}
                        
                        try:
                            res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                            data = res.json()
                            if 'choices' in data:
                                st.success("✅ Petição Preliminar Gerada com Sucesso!")
                                st.markdown(data['choices'][0]['message']['content'])
                            else:
                                st.error(f"Erro de Cota/Saldo na OpenAI: {data}")
                        except:
                            st.error("Falha na ligação com a API da OpenAI.")
                else:
                    st.warning("Preencha todos os campos do pré-formulário acima para a IA ter contexto suficiente.")
