import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- FUNÇÕES GERADORAS DE PDF ---
# Nota: Textos sem acento no FPDF para evitar erros de encoding de última hora no servidor
def gerar_pdf_rescisao(cliente, salario, dias_trabalhados, meses, aviso, decimo_terceiro, ferias, multa_fgts, saldo_salario, valor_aviso, total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="LegisON - Memoria de Calculo Trabalhista", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Data do Calculo: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"CLIENTE / RECLAMANTE: {cliente.upper() if cliente else 'NAO INFORMADO'}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Salario Base: R$ {salario:,.2f}", ln=True)
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    
    pdf.cell(200, 10, txt="VERBAS RESCISORIAS:", ln=True)
    pdf.cell(200, 10, txt=f"- Saldo de Salario ({dias_trabalhados} dias): R$ {saldo_salario:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"- Aviso Previo ({aviso}): R$ {valor_aviso:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"- 13 Proporcional ({meses}/12): R$ {decimo_terceiro:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"- Ferias Proporcionais + 1/3: R$ {ferias:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"- Multa FGTS (40% sobre saldo): R$ {multa_fgts:,.2f}", ln=True)
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"TOTAL ESTIMADO: R$ {total:,.2f}", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

def gerar_pdf_he(cliente, salario_he, horas_trab, adicional, valor_hora, valor_he, total_he):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="LegisON - Calculo de Horas Extras", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"CLIENTE / RECLAMANTE: {cliente.upper() if cliente else 'NAO INFORMADO'}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Salario Base (Divisor 220): R$ {salario_he:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Quantidade de Horas: {horas_trab}h | Adicional: {adicional}", ln=True)
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Valor da Hora Base: R$ {valor_hora:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Valor da Hora Extra: R$ {valor_he:,.2f}", ln=True)
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"TOTAL A RECEBER: R$ {total_he:,.2f}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

def gerar_pdf_juros(cliente, valor_original, meses_atraso, taxa_juros, valor_juros, total_atualizado):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="LegisON - Atualizacao de Valores", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"CLIENTE / RECLAMANTE: {cliente.upper() if cliente else 'NAO INFORMADO'}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Valor Original: R$ {valor_original:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Tempo de Atraso: {meses_atraso} meses | Taxa: {taxa_juros}% a.m.", ln=True)
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Juros Acumulados: R$ {valor_juros:,.2f}", ln=True)
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"TOTAL ATUALIZADO: R$ {total_atualizado:,.2f}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="LegisON - Painel", layout="wide")

# --- MENU LATERAL ---
st.sidebar.title("⚖️ LegisON")
st.sidebar.markdown("Ferramenta de Produtividade Jurídica")
menu = st.sidebar.radio("Navegação", ["📊 Dashboard de Leads", "🧮 Calculadora Trabalhista"])

# --- TELA 1: DASHBOARD ---
if menu == "📊 Dashboard de Leads":
    st.title("Visão Geral do Escritório")
    col1, col2, col3 = st.columns(3)
    col1.metric("Leads Totais", "2", "+1 novo")
    col2.metric("Qualificados (IA)", "1", "Score: 85%")
    col3.metric("Petições em Rascunho", "0")
    st.divider()
    st.subheader("Leads Recentes (Pipeline)")
    dados = {
        "Nome": ["João Ricardo", "Maria Antonieta"],
        "Caso Relatado": ["Quero informações para aposentadoria", "Fui demitida sem justa causa."],
        "Área": ["Previdenciário", "Trabalhista"],
        "Status": ["Em Nutrição", "Novo Lead"]
    }
    st.dataframe(pd.DataFrame(dados), use_container_width=True, hide_index=True)

# --- TELA 2: CALCULADORA COMPLETA (MVP PRD) ---
elif menu == "🧮 Calculadora Trabalhista":
    st.title("Calculadora Trabalhista (MVP)")
    st.markdown("Cálculos essenciais automatizados com geração de relatório em PDF.")
    
    # Adicionando o campo de Nome do Cliente no topo
    cliente_nome = st.text_input("👤 Nome do Cliente / Reclamante (Para o Relatório PDF)", placeholder="Ex: João da Silva")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["🔹 Rescisão CLT", "🔹 Horas Extras", "🔹 Atualização de Valores"])
    
    # ABA 1: RESCISÃO COMPLETA
    with tab1:
        st.subheader("Cálculo de Rescisão")
        col1, col2 = st.columns(2)
        salario = col1.number_input("Salário Base (R$)", value=2000.00, step=100.0)
        dias_trabalhados = col2.number_input("Dias Trabalhados (No mês da rescisão)", min_value=0, max_value=31, value=15)
        
        col3, col4 = st.columns(2)
        meses = col3.number_input("Meses Trabalhados (Ano atual para 13º/Férias)", min_value=1, max_value=12, value=6)
        saldo_fgts = col4.number_input("Saldo atual do FGTS (R$)", value=1500.00, step=100.0)
        
        aviso = st.selectbox("Aviso Prévio", ["Indenizado (Recebe +1 mês)", "Trabalhado / Não se aplica"])
        
        if st.button("Calcular Rescisão", type="primary"):
            saldo_salario = (salario / 30) * dias_trabalhados
            valor_aviso = salario if aviso == "Indenizado (Recebe +1 mês)" else 0.0
            decimo_terceiro = (meses / 12) * salario
            ferias = (meses / 12) * salario * (4/3) 
            multa_fgts = saldo_fgts * 0.40
            total = saldo_salario + valor_aviso + decimo_terceiro + ferias + multa_fgts
            
            st.success(f"**Total da Rescisão: R$ {total:,.2f}**")
            st.write("### 📄 Memória de Cálculo")
            st.write(f"- **Saldo de Salário:** R$ {saldo_salario:,.2f}")
            st.write(f"- **Aviso Prévio:** R$ {valor_aviso:,.2f}")
            st.write(f"- **13º Proporcional:** R$ {decimo_terceiro:,.2f}")
            st.write(f"- **Férias + 1/3:** R$ {ferias:,.2f}")
            st.write(f"- **Multa FGTS:** R$ {multa_fgts:,.2f}")
            
            pdf_bytes = gerar_pdf_rescisao(cliente_nome, salario, dias_trabalhados, meses, aviso, decimo_terceiro, ferias, multa_fgts, saldo_salario, valor_aviso, total)
            st.download_button("📄 Baixar Relatório PDF", data=pdf_bytes, file_name="rescisao.pdf", mime="application/pdf")

    # ABA 2: HORAS EXTRAS
    with tab2:
        st.subheader("Cálculo de Horas Extras")
        colA, colB = st.columns(2)
        salario_he = colA.number_input("Salário Base (R$)", value=2000.00, step=100.0, key="sal_he")
        horas_trab = colB.number_input("Quantidade de Horas Extras", value=10, step=1)
        adicional = colA.selectbox("Adicional", ["50% (Dias normais)", "100% (Domingos/Feriados)"])
        
        if st.button("Calcular Horas Extras", type="primary"):
            valor_hora = salario_he / 220
            multiplicador = 1.5 if "50%" in adicional else 2.0
            valor_he = valor_hora * multiplicador
            total_he = valor_he * horas_trab
            
            st.success(f"**Total a Receber: R$ {total_he:,.2f}**")
            st.write("### 📄 Memória de Cálculo")
            st.write(f"- **Valor da Hora Base:** R$ {valor_hora:,.2f}")
            st.write(f"- **Valor da Hora Extra:** R$ {valor_he:,.2f}")
            
            pdf_bytes_he = gerar_pdf_he(cliente_nome, salario_he, horas_trab, adicional, valor_hora, valor_he, total_he)
            st.download_button("📄 Baixar Relatório PDF", data=pdf_bytes_he, file_name="horas_extras.pdf", mime="application/pdf")

    # ABA 3: ATUALIZAÇÃO DE VALORES
    with tab3:
        st.subheader("Atualização de Valores (Juros Simples)")
        colX, colY = st.columns(2)
        valor_original = colX.number_input("Valor Original do Débito (R$)", value=5000.00, step=100.0)
        meses_atraso = colY.number_input("Meses de Atraso", value=12, step=1)
        taxa_juros = colX.number_input("Taxa de Juros (% ao mês)", value=1.0, step=0.1)
        
        if st.button("Atualizar Valor", type="primary"):
            valor_juros = valor_original * (taxa_juros / 100) * meses_atraso
            total_atualizado = valor_original + valor_juros
            
            st.success(f"**Valor Total Atualizado: R$ {total_atualizado:,.2f}**")
            st.write("### 📄 Memória de Cálculo")
            st.write(f"- **Valor Inicial:** R$ {valor_original:,.2f}")
            st.write(f"- **Juros Acumulados ({meses_atraso} meses):** R$ {valor_juros:,.2f}")
            
            pdf_bytes_juros = gerar_pdf_juros(cliente_nome, valor_original, meses_atraso, taxa_juros, valor_juros, total_atualizado)
            st.download_button("📄 Baixar Relatório PDF", data=pdf_bytes_juros, file_name="atualizacao.pdf", mime="application/pdf")