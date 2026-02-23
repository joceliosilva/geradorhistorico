import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import random

# ----------------- 1. Dados base das disciplinas -----------------
disciplinas_base_parte1 = [
    {'bloco': 'Organização do processo de trabalho em Saúde I', 'disciplina': 'Ética, legislação, trabalho e Bioética', 'professor': 'ANTONIO PAZ ARAUJO FILHO', 'ch_teorica': '20', 'ch_pratica': '-', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Organização do processo de trabalho em Saúde I', 'disciplina': 'Relações Humanas e psicologia aplicada a saúde', 'professor': 'WISCOVINNY G. CARVALHO', 'ch_teorica': '20', 'ch_pratica': '-', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Organização do processo de trabalho em Saúde I', 'disciplina': 'Politicas Públicas de saúde SUS', 'professor': 'LUCAS RODRIGUES FEITOSA', 'ch_teorica': '20', 'ch_pratica': '-', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Educação para autocuidado', 'disciplina': 'Educação para o autocuidado', 'professor': 'ANTONIO PAZ ARAUJO FILHO', 'ch_teorica': '20', 'ch_pratica': '10', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Educação para autocuidado', 'disciplina': 'Primeiros socorros', 'professor': 'LUCAS RODRIGUES FEITOSA', 'ch_teorica': '40', 'ch_pratica': '10', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Biossegurança nas ações de enfermagem', 'disciplina': 'Microbiologia e parasitologia aplicada a saúde', 'professor': 'ALCIDES C. CHAES', 'ch_teorica': '40', 'ch_pratica': '10', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Promoção da saúde e segurança do trabalho', 'disciplina': 'Biossegurança: Saúde e segurança no trabalho', 'professor': 'WISCOVINNY G. CARVALHO', 'ch_teorica': '20', 'ch_pratica': '-', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Apoio Diagnóstico', 'disciplina': 'Anatomia e fisiologia Humana Básica', 'professor': 'LUCAS RODRIGUES FEITOSA', 'ch_teorica': '40', 'ch_pratica': '10', 'media': '', 'situacao': 'APROVADO'},
]

disciplinas_base_parte2 = [
    {'bloco': 'Organização do processo de trabalho em Saúde II', 'disciplina': 'Organização do Processo de Trabalho Aplicado à Enfermagem', 'professor': '-', 'ch_teorica': '40', 'ch_pratica': '-', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Assistência em Saúde Coletiva', 'disciplina': 'Saúde coletiva', 'professor': 'LUCAS RODRIGUES FEITOSA', 'ch_teorica': '60', 'ch_pratica': '0', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Recuperação e Reablilitação I', 'disciplina': 'Fundamentos da Enfermagem', 'professor': '-', 'ch_teorica': '60', 'ch_pratica': '30', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Recuperação e Reablilitação I', 'disciplina': 'Enfermagem em saúde mental', 'professor': '-', 'ch_teorica': '60', 'ch_pratica': '30', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Recuperação e Reablilitação I', 'disciplina': 'Enfermagem em Clínica Médica', 'professor': '-', 'ch_teorica': '60', 'ch_pratica': '30', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Recuperação e Reablilitação I', 'disciplina': 'Enfermagem em Centro Cirurgico', 'professor': '-', 'ch_teorica': '60', 'ch_pratica': '30', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Recuperação e Reablilitação I', 'disciplina': 'Enfermagem em Saúde da Mulher', 'professor': '-', 'ch_teorica': '60', 'ch_pratica': '30', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Recuperação e Reablilitação I', 'disciplina': 'Enfermagem em Saúde da Criança e do Adolescente', 'professor': '-', 'ch_teorica': '60', 'ch_pratica': '30', 'media': '', 'situacao': 'APROVADO'},
]

disciplinas_base_parte3 = [
    {'bloco': 'Organização do processo de trabalho em Saúde III', 'disciplina': 'Principio do Planejamento e Organização da Assistência', 'professor': '-', 'ch_teorica': '40', 'ch_pratica': '-', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Recuperação e Reablilitação II', 'disciplina': 'Urgência e Emergência', 'professor': '-', 'ch_teorica': '60', 'ch_pratica': '20', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Recuperação e Reablilitação II', 'disciplina': 'Enfermagem em UTI', 'professor': '-', 'ch_teorica': '60', 'ch_pratica': '20', 'media': '', 'situacao': 'APROVADO'},
    {'bloco': 'Recuperação e Reablilitação II', 'disciplina': 'Saúde do Idoso', 'professor': '-', 'ch_teorica': '40', 'ch_pratica': '20', 'media': '', 'situacao': 'APROVADO'},
]

dados_estagio_base = [
    {'disciplina': 'Estágio Supervisionado I - ESF', 'supervisor': '-', 'ch_teorica': '200', 'ch_pratica': '200', 'media': '-', 'situacao': 'CONCLUÍDO'},
    {'disciplina': 'Estágio Supervisionado II - Hospitalar', 'supervisor': '-', 'ch_teorica': '200', 'ch_pratica': '200', 'media': '-', 'situacao': 'CONCLUÍDO'},
]

# ----------------- 2. Funções de Lógica e PDF -----------------

def generate_random_grades(disciplines_list):
    new_list = []
    for disc in disciplines_list:
        d = disc.copy()
        if d['media'] == '':
            grade = round(random.uniform(7.5, 9.8), 1)
            d['media'] = str(grade).replace('.', ',')
        new_list.append(d)
    return new_list

def create_styled_table(disciplinas_list):
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(name='TableHeader', fontSize=7, fontName='Helvetica-Bold', alignment=TA_CENTER)
    content_style = ParagraphStyle(name='TableContent', fontSize=7)
    
    table_data = [
        [Paragraph('BLOCO TEMÁTICO', header_style), Paragraph('DISCIPLINAS', header_style), Paragraph('PROFESSOR', header_style), 
         Paragraph('C.H. Teor.', header_style), Paragraph('C.H. Prat.', header_style), Paragraph('MÉDIA', header_style), Paragraph('SITUAÇÃO', header_style)]
    ]

    for d in disciplinas_list:
        table_data.append([
            Paragraph(d['bloco'], content_style), Paragraph(d['disciplina'], content_style), Paragraph(d['professor'], content_style),
            Paragraph(d['ch_teorica'], content_style), Paragraph(d['ch_pratica'], content_style), Paragraph(d['media'], content_style), Paragraph(d['situacao'], content_style)
        ])

    table = Table(table_data, colWidths=[3.5*cm, 6*cm, 3.5*cm, 1.5*cm, 1.5*cm, 1.2*cm, 2*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    return table

def create_internship_table(internship_list):
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(name='IHeader', fontSize=7, fontName='Helvetica-Bold', alignment=TA_CENTER)
    content_style = ParagraphStyle(name='IContent', fontSize=7)
    
    table_data = [[Paragraph('ESTÁGIO SUPERVISIONADO', header_style), '', '', '', ''],
                  [Paragraph('DISCIPLINA', header_style), Paragraph('SUPERVISOR', header_style), Paragraph('C.H.', header_style), Paragraph('MÉDIA', header_style), Paragraph('SITUAÇÃO', header_style)]]
    
    for i in internship_list:
        table_data.append([Paragraph(i['disciplina'], content_style), Paragraph(i['supervisor'], content_style), 
                           Paragraph(f"{i['ch_teorica']}h", content_style), Paragraph(i['media'], content_style), Paragraph(i['situacao'], content_style)])

    table = Table(table_data, colWidths=[8*cm, 5.5*cm, 2.5*cm, 1.5*cm, 2*cm])
    table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0,0), (-1,1), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    return table

def gerar_pdf_buffer(dados_aluno, partes):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=cm, leftMargin=cm, topMargin=cm, bottomMargin=cm)
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='T', alignment=TA_CENTER, fontSize=14, fontName='Helvetica-Bold')
    
    story.append(Paragraph("HISTÓRICO ESCOLAR", title_style))
    story.append(Spacer(1, 0.5*cm))

    # Dados do Aluno
    aluno_info = [[f"Aluna(o): {dados_aluno['nome']}", f"CPF: {dados_aluno['cpf']}"],
                  [f"Curso: {dados_aluno['curso']}", f"Turma: {dados_aluno['turma']}"],
                  [f"Situação: {dados_aluno['situacao']}", ""]]
    
    aluno_table = Table(aluno_info, colWidths=[12*cm, 7*cm])
    aluno_table.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 9), ('BOTTOMPADDING', (0,0), (-1,-1), 5)]))
    story.append(aluno_table)
    story.append(Spacer(1, 0.5*cm))

    # Adiciona Tabelas
    story.append(create_styled_table(partes[0]))
    story.append(Spacer(1, 0.3*cm))
    story.append(create_styled_table(partes[1]))
    story.append(Spacer(1, 0.3*cm))
    story.append(create_styled_table(partes[2]))
    story.append(Spacer(1, 0.5*cm))
    story.append(create_internship_table(dados_estagio_base))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ----------------- 3. Interface Streamlit -----------------

st.set_page_config(page_title="Gerador de Histórico", layout="wide")
st.title("🎓 Sistema de Emissão de Histórico")

with st.sidebar:
    st.header("Dados do Aluno")
    nome = st.text_input("Nome Completo")
    cpf = st.text_input("CPF")
    curso = st.text_input("Curso", value="Técnico em Enfermagem")
    turma = st.text_input("Turma")
    situacao = st.selectbox("Situação", ["CONCLUÍDO", "CURSANDO", "APROVADO"])

if st.button("Gerar Histórico Escolar"):
    if not nome or not cpf:
        st.warning("Preencha o Nome e o CPF para continuar.")
    else:
        with st.spinner("Gerando documento..."):
            dados = {'nome': nome, 'cpf': cpf, 'curso': curso, 'turma': turma, 'situacao': situacao}
            
            # Gera notas
            p1 = generate_random_grades(disciplinas_base_parte1)
            p2 = generate_random_grades(disciplinas_base_parte2)
            p3 = generate_random_grades(disciplinas_base_parte3)
            
            pdf_out = gerar_pdf_buffer(dados, [p1, p2, p3])
            
            st.success("PDF gerado com sucesso!")
            st.download_button(
                label="⬇️ Baixar Histórico (PDF)",
                data=pdf_out,
                file_name=f"Historico_{nome.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )