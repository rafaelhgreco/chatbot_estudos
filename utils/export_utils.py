"""
Utilitários para exportação de relatórios e cronogramas.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
import re
from datetime import datetime


def gerar_pdf_cronograma(tema: str, metodologia: str, cronograma: str, 
                        tempo: str = "", prazo: str = "", nivel: str = "") -> bytes:
    """
    Gera um PDF formatado com o cronograma de estudos.
    
    Args:
        tema: Tema do cronograma
        metodologia: Metodologia escolhida
        cronograma: Texto do cronograma gerado
        tempo: Tempo disponível por dia
        prazo: Prazo para conclusão
        nivel: Nível de conhecimento
    
    Returns:
        bytes: Conteúdo do PDF em bytes
    """
    buffer = BytesIO()
    
    # Criar documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para título
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1f77b4',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulo
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2c3e50',
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    texto_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )
    
    # Estilo para metadados
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['BodyText'],
        fontSize=10,
        textColor='#555555',
        spaceAfter=6
    )
    
    # Construir conteúdo
    story = []
    
    # Título principal
    story.append(Paragraph("📚 Cronograma de Estudos Personalizado", titulo_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Informações do cronograma
    story.append(Paragraph(f"<b>Tema:</b> {tema}", info_style))
    story.append(Paragraph(f"<b>Metodologia:</b> {metodologia}", info_style))
    
    if tempo:
        story.append(Paragraph(f"<b>Tempo disponível:</b> {tempo}", info_style))
    if prazo:
        story.append(Paragraph(f"<b>Prazo:</b> {prazo}", info_style))
    if nivel:
        story.append(Paragraph(f"<b>Nível:</b> {nivel}", info_style))
    
    story.append(Paragraph(f"<b>Data de geração:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", info_style))
    story.append(Spacer(1, 1*cm))
    
    # Processar o cronograma
    # Divide o texto em linhas e processa formatação markdown básica
    linhas = cronograma.split('\n')
    
    for linha in linhas:
        linha = linha.strip()
        
        if not linha:
            story.append(Spacer(1, 0.3*cm))
            continue
        
        # Remover markdown de negrito (**texto** ou __texto__)
        linha_limpa = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', linha)
        linha_limpa = re.sub(r'__(.*?)__', r'<b>\1</b>', linha_limpa)
        
        # Remover markdown de itálico (*texto* ou _texto_)
        linha_limpa = re.sub(r'\*(.*?)\*', r'<i>\1</i>', linha_limpa)
        linha_limpa = re.sub(r'_(.*?)_', r'<i>\1</i>', linha_limpa)
        
        # Detectar títulos (# ou ##)
        if linha.startswith('###'):
            texto = linha.replace('###', '').strip()
            story.append(Paragraph(texto, subtitulo_style))
        elif linha.startswith('##'):
            texto = linha.replace('##', '').strip()
            story.append(Paragraph(texto, subtitulo_style))
        elif linha.startswith('#'):
            texto = linha.replace('#', '').strip()
            story.append(Paragraph(texto, titulo_style))
        # Detectar listas (- ou *)
        elif linha.startswith('- ') or linha.startswith('* '):
            texto = '• ' + linha_limpa[2:]
            story.append(Paragraph(texto, texto_style))
        # Detectar listas numeradas
        elif re.match(r'^\d+\.', linha):
            story.append(Paragraph(linha_limpa, texto_style))
        # Texto normal
        else:
            story.append(Paragraph(linha_limpa, texto_style))
    
    # Rodapé
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("---", texto_style))
    story.append(Paragraph(
        "<i>Gerado pelo Chatbot de Estudos Personalizados</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, 
                      textColor='#888888', alignment=TA_CENTER)
    ))
    
    # Gerar PDF
    doc.build(story)
    
    # Retornar bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def sanitizar_nome_arquivo(texto: str, max_length: int = 50) -> str:
    """
    Sanitiza um texto para ser usado como nome de arquivo.
    
    Args:
        texto: Texto a ser sanitizado
        max_length: Comprimento máximo do nome
    
    Returns:
        str: Texto sanitizado
    """
    # Remover caracteres especiais
    sanitizado = re.sub(r'[^\w\s-]', '', texto)
    # Substituir espaços por underscores
    sanitizado = re.sub(r'[\s]+', '_', sanitizado)
    # Limitar comprimento
    sanitizado = sanitizado[:max_length]
    # Remover underscores do início e fim
    sanitizado = sanitizado.strip('_')
    
    return sanitizado or "cronograma"
