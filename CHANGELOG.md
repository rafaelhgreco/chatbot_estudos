# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2025-11-20

### ✨ Adicionado

#### Persistência de Histórico no LocalStorage
- Histórico de conversas agora é automaticamente salvo no navegador
- Sobrevive a reloads de página (F5)
- Dados são preservados até que o usuário clique em "Limpar Tudo"
- Implementado via JavaScript integrado ao Streamlit
- Codificação em base64 para garantir compatibilidade

#### Exportação de Cronogramas em PDF
- Nova funcionalidade para baixar cronogramas em formato PDF
- PDFs profissionais e bem formatados em A4
- Inclui todos os metadados (tema, metodologia, tempo, prazo, nível)
- Suporte a formatação markdown (negrito, itálico, títulos, listas)
- Nome de arquivo automático e sanitizado: `cronograma_[tema]_[timestamp].pdf`
- Data e hora de geração incluídas no documento
- Rodapé personalizado

#### Novos Controles na Sidebar
- **Botão "🔄 Nova Conversa"**: Inicia nova conversa mantendo histórico salvo
- **Botão "🗑️ Limpar Tudo"**: Remove completamente o histórico e reseta aplicação
- **Seção "💾 Exportar Cronograma"**: Aparece automaticamente quando cronograma é gerado
- Mensagens de feedback ao usuário sobre ações realizadas

### 📦 Dependências Adicionadas
- `reportlab==4.4.5` - Biblioteca para geração de PDFs
- `streamlit-js-eval==0.1.7` - Integração com JavaScript/localStorage

### 📝 Documentação
- Criado `NOVAS_FUNCIONALIDADES.md` com documentação completa das features
- Criado `tests/test_export.py` com testes para funções de exportação
- Atualizado `README.md` com lista de novas funcionalidades
- Criado este `CHANGELOG.md`

### 🔧 Arquivos Modificados
- `streamlit_app.py`: Adicionadas funções de localStorage e integração com PDF
- `requirements.txt`: Adicionadas novas dependências
- `utils/export_utils.py`: Novo arquivo com funções de geração de PDF

### 🎯 Cenários BDD Implementados

**Cenário: Persistência de Histórico**
```gherkin
Dado que o usuário usou o chatbot e gerou um cronograma
Quando ele fizer reload da página e voltar
Então o histórico dele deve ser armazenado no localStorage
E somente ser resetado quando ele clicar no botão de reset
```

**Cenário: Exportação de PDF**
```gherkin
Dado que o usuário gerou um relatório
Então ele quer salvar e exportar esse relatório
Então ele tem a opção de baixar um PDF desse relatório que foi gerado anteriormente
```

### 🧪 Testes
- Função `sanitizar_nome_arquivo()` testada e validada
- Função `gerar_pdf_cronograma()` testada e validada
- PDFs gerados confirmados como válidos (header `%PDF`)
- Tamanho médio dos PDFs: ~3-5KB

---

## [1.0.0] - 2025-11-XX

### ✨ Lançamento Inicial

#### Funcionalidades Core
- Chatbot conversacional para criação de cronogramas de estudo
- Integração com Google Gemini 2.5 Flash
- Máquina de estados para gerenciar fluxo de conversa
- Coleta interativa de requisitos (tema, metodologia, parâmetros)
- Geração de cronogramas personalizados
- Sistema de feedback e refinamento iterativo
- Barra de progresso visual

#### Metodologias Suportadas
- Long-life Learning
- Shoshin
- Kumon
- Pomodoro
- Spaced Repetition
- Feynman

#### Arquitetura
- Separação de responsabilidades em módulos
- Validação com Pydantic
- Templates de prompts organizados
- Testes unitários

#### Documentação
- README completo
- PLANEJAMENTO.md com análise BDD
- Comentários no código
- Exemplos de uso

---

## Tipos de Mudanças

- `✨ Adicionado` - Para novas funcionalidades
- `🔄 Modificado` - Para mudanças em funcionalidades existentes
- `🗑️ Removido` - Para funcionalidades removidas
- `🐛 Corrigido` - Para correção de bugs
- `🔒 Segurança` - Para correções de vulnerabilidades
- `📦 Dependências` - Para atualizações de dependências
- `📝 Documentação` - Para mudanças na documentação
