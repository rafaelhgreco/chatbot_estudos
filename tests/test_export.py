"""
Teste unitário para as funções de exportação de PDF.
"""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.export_utils import gerar_pdf_cronograma, sanitizar_nome_arquivo


def test_sanitizar_nome_arquivo():
    """Testa a sanitização de nomes de arquivo."""
    print("🧪 Testando sanitização de nomes de arquivo...")
    
    # Teste 1: Nome normal
    resultado = sanitizar_nome_arquivo("Python para Iniciantes")
    assert resultado == "Python_para_Iniciantes", f"Esperado 'Python_para_Iniciantes', obtido '{resultado}'"
    print("✅ Teste 1 passou: Nome normal")
    
    # Teste 2: Com caracteres especiais
    resultado = sanitizar_nome_arquivo("C++/C# & Java!")
    assert resultado == "CC_Java", f"Esperado 'CC_Java', obtido '{resultado}'"
    print("✅ Teste 2 passou: Caracteres especiais")
    
    # Teste 3: Nome muito longo
    resultado = sanitizar_nome_arquivo("A" * 100)
    assert len(resultado) <= 50, f"Nome muito longo: {len(resultado)} caracteres"
    print("✅ Teste 3 passou: Limite de comprimento")
    
    # Teste 4: String vazia
    resultado = sanitizar_nome_arquivo("")
    assert resultado == "cronograma", f"Esperado 'cronograma', obtido '{resultado}'"
    print("✅ Teste 4 passou: String vazia")
    
    print("✅ Todos os testes de sanitização passaram!\n")


def test_gerar_pdf():
    """Testa a geração de PDF."""
    print("🧪 Testando geração de PDF...")
    
    cronograma_exemplo = """
# Cronograma de Estudos: Python para Iniciantes

## Semana 1: Fundamentos
- Variáveis e tipos de dados
- Estruturas de controle (if, for, while)
- Funções básicas

## Semana 2: Estruturas de Dados
- Listas e tuplas
- Dicionários e sets
- Compreensão de listas

## Semana 3: Orientação a Objetos
- Classes e objetos
- Herança e polimorfismo
- **Projeto prático:** Sistema de gerenciamento

### Exercícios Recomendados
1. Criar uma classe Pessoa
2. Implementar herança com Aluno
3. Desenvolver projeto final

*Lembre-se de praticar diariamente!*
"""
    
    try:
        pdf_bytes = gerar_pdf_cronograma(
            tema="Python para Iniciantes",
            metodologia="Feynman + Pomodoro",
            cronograma=cronograma_exemplo,
            tempo="2 horas por dia",
            prazo="3 semanas",
            nivel="Iniciante"
        )
        
        assert pdf_bytes is not None, "PDF não foi gerado"
        assert len(pdf_bytes) > 1000, f"PDF muito pequeno: {len(pdf_bytes)} bytes"
        assert pdf_bytes[:4] == b'%PDF', "Não é um arquivo PDF válido"
        
        print(f"✅ PDF gerado com sucesso: {len(pdf_bytes)} bytes")
        
        # Salvar PDF de exemplo
        output_path = os.path.join(os.path.dirname(__file__), "exemplo_cronograma.pdf")
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF de exemplo salvo em: {output_path}")
        print("✅ Teste de geração de PDF passou!\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Iniciando testes das funções de exportação")
    print("=" * 60 + "\n")
    
    # Executar testes
    test_sanitizar_nome_arquivo()
    sucesso = test_gerar_pdf()
    
    print("=" * 60)
    if sucesso:
        print("✅ TODOS OS TESTES PASSARAM!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
    print("=" * 60)
