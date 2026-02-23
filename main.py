import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import random

# --- (Aqui ficariam suas listas de disciplinas_base_parte1, 2, 3 e estagio) ---
# [MANTENHA AS MESMAS LISTAS QUE VOCÊ JÁ TEM NO SEU CÓDIGO ORIGINAL AQUI]

def gerar_pdf_buffer(dados_aluno, partes_disciplinas, dados_estagio):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=cm, leftMargin=cm, topMargin=cm, bottomMargin=cm)
    story = []
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenteredTitle', alignment=TA_CENTER, fontSize=12, fontName='Helvetica-Bold'))
    
    story.append(Paragraph("HISTÓRICO ESCOLAR", styles['CenteredTitle']))
    story.append(Spacer(1, 0.1*cm))

    # Tabela de dados do aluno
    aluno_data = [
        [f"Aluna(o): {dados_aluno['nome']}", f"CPF: {dados_aluno['cpf']}"],
        [f"Curso: {dados_aluno['curso']}", f"Turma: {dados_aluno['turma']}", f"Situação: {dados_aluno['situacao']}"]
    ]
    aluno_table = Table(aluno_data, colWidths=[11*cm, 7*cm])
    aluno_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
    ]))
    story.append(aluno_table)
    story.append(Spacer(1, 0.5*cm))

    # Adicionando as tabelas de disciplinas (usando suas funções create_styled_table)
    for parte in partes_disciplinas:
        # Nota: Você deve incluir as funções create_styled_table e create_internship_table aqui
        story.append(create_styled_table(parte)) 
        story.append(Spacer(1, 0.2*cm))

    story.append(create_internship_table(dados_estagio))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- Interface Web com Streamlit ---
st.set_page_config(page_title="Gerador de Histórico")
st.title("📄 Gerador de Histórico Escolar")

with st.form("dados_aluno"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome do Aluno")
        cpf = st.text_input("CPF")
        curso = st.text_input("Curso", value="Técnico em Enfermagem")
    with col2:
        turma = st.text_input("Turma")
        situacao = st.selectbox("Situação", ["APROVADO", "CURSANDO", "CONCLUÍDO"])
    
    submetido = st.form_submit_button("Gerar PDF")

if submetido:
    if not nome:
        st.error("Por favor, preencha o nome do aluno.")
    else:
        dados = {'nome': nome, 'cpf': cpf, 'curso': curso, 'turma': turma, 'situacao': situacao}
        
        # Lógica de notas aleatórias (sua função original)
        d1 = generate_random_grades(disciplinas_base_parte1.copy())
        d2 = generate_random_grades(disciplinas_base_parte2.copy())
        d3 = generate_random_grades(disciplinas_base_parte3.copy())
        
        pdf_resultado = gerar_pdf_buffer(dados, [d1, d2, d3], dados_estagio_base)
        
        st.success("PDF Gerado com sucesso!")
        st.download_button(
            label="⬇️ Baixar Histórico Escolar",
            data=pdf_resultado,
            file_name=f"Historico_{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
