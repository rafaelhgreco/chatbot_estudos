# 🚀 Guia Rápido: Chatbot de Estudos

## 📥 Como Instalar e Usar

### Opção 1: Usar Online (Recomendado)

**Acesse diretamente:** https://chatbot-estudos.streamlit.app/

✅ Não precisa instalar nada  
✅ Funciona em qualquer dispositivo  
✅ Sempre atualizado  

---

### Opção 2: Executar Localmente

#### Pré-requisitos

- ✅ Python 3.10 ou superior
- ✅ pip (gerenciador de pacotes Python)
- ✅ Git (opcional, para clonar repositório)

#### Passo 1: Obter o Código

**Opção A: Clonar com Git**
```bash
git clone https://github.com/rafaelhgreco/chatbot_estudos.git
cd chatbot_estudos
```

**Opção B: Download Direto**
1. Acesse: https://github.com/rafaelhgreco/chatbot_estudos
2. Clique em "Code" → "Download ZIP"
3. Extraia o arquivo
4. Navegue até a pasta no terminal

#### Passo 2: Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

#### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

**Pacotes instalados:**
- streamlit
- requests
- python-dotenv
- pydantic
- pytest
- reportlab

#### Passo 4: Configurar API Key do Gemini

**4.1 - Obter API Key Gratuita**

1. Acesse: https://aistudio.google.com/
2. Faça login com conta Google
3. Clique em **"Get API Key"**
4. Clique em **"Create API Key"**
5. Copie a chave gerada

**4.2 - Configurar no Projeto**

```bash
# Criar arquivo .env
cp .env.example .env

# Editar .env (use seu editor favorito)
nano .env
# ou
code .env
```

**Conteúdo do .env:**
```
GEMINI_API_KEY=sua_chave_aqui_copiada_do_google
```

⚠️ **IMPORTANTE:** Nunca compartilhe sua API key!

#### Passo 5: Executar o Aplicativo

```bash
streamlit run streamlit_app.py
```

✅ O navegador abrirá automaticamente em: http://localhost:8501

---

## 💬 Como Usar o Chatbot

### Passo 1: Informar o Tema

O bot perguntará: **"Qual tema você gostaria de estudar?"**

**Exemplos de respostas válidas:**
- ✅ "Python para Data Science"
- ✅ "Inglês para entrevistas de emprego"
- ✅ "Cálculo Diferencial e Integral"
- ✅ "Marketing Digital para iniciantes"
- ❌ "Python" (muito vago - bot pedirá mais detalhes)

### Passo 2: Escolher a Metodologia

O bot apresentará **6 metodologias**:

| 🎯 Metodologia | 📌 Melhor Para |
|---------------|---------------|
| **Long-life Learning** | Aprendizado sustentável, sem pressa |
| **Shoshin** | Iniciantes totais, mente aberta |
| **Kumon** | Domínio através da repetição |
| **Pomodoro** | Quem tem dificuldade de foco |
| **Spaced Repetition** | Memorização de longo prazo |
| **Feynman** | Compreensão profunda de conceitos |

**Digite o nome da metodologia escolhida** (não precisa ser exato)

### Passo 3: Informar Tempo Disponível

O bot perguntará: **"Quanto tempo você pode dedicar por dia?"**

**Exemplos:**
- "2 horas por dia"
- "30 minutos diários"
- "1 hora nos dias de semana, 3 horas no fim de semana"

### Passo 4: Informar Prazo

O bot perguntará: **"Qual seu prazo para alcançar o objetivo?"**

**Exemplos:**
- "3 meses"
- "6 semanas"
- "1 ano"
- "Até dezembro de 2025"

### Passo 5: Informar Nível Atual

O bot perguntará: **"Qual seu nível atual de conhecimento?"**

**Exemplos:**
- "Iniciante completo"
- "Básico - já conheço um pouco"
- "Intermediário"
- "Avançado - só preciso aprofundar"

### Passo 6: Receber o Cronograma

O bot gerará um cronograma detalhado como:

```markdown
# Cronograma de Estudos: Python para Data Science

## Semana 1: Fundamentos Python
**Objetivo:** Dominar sintaxe básica

### Dias 1-2 (2h/dia)
- 📖 Teoria: Variáveis, tipos de dados, operadores
- 💻 Prática: 10 exercícios no HackerRank
- 🎯 Meta: Escrever primeiro script

### Dia 3 (2h)
- 📖 Teoria: Estruturas condicionais (if/else)
- 💻 Prática: Criar calculadora simples
...
```

### Passo 7: Refinar (Opcional)

Você pode pedir ajustes:

**Exemplos de refinamentos:**
- "Pode aumentar a intensidade?"
- "Adicione mais projetos práticos"
- "Reduza o tempo diário para 1 hora"
- "Foque mais em teoria"
- "Quero mais exercícios"

### Passo 8: Exportar em PDF

**Na barra lateral (Sidebar):**

1. Vá até **"💾 Exportar Cronograma"**
2. Clique em **"📥 Baixar PDF"**
3. O arquivo será baixado automaticamente

**Nome do arquivo:**
```
cronograma_<tema>_<data_hora>.pdf
```

Exemplo: `cronograma_python_data_science_20251121_143022.pdf`

---

## 🔧 Comandos Úteis

### Durante o Uso

| Ação | Como Fazer |
|------|-----------|
| 🔄 Começar nova conversa | Clique em "Nova Conversa" na sidebar |
| 📊 Ver progresso | Visualize a barra de progresso na sidebar |
| 📥 Baixar PDF | Clique em "Baixar PDF" (após cronograma gerado) |
| ⚙️ Ver dados coletados | Confira a sidebar (tema, metodologia, etc.) |

### Terminal

| Comando | Descrição |
|---------|-----------|
| `streamlit run streamlit_app.py` | Iniciar aplicação |
| `Ctrl + C` | Parar aplicação |
| `deactivate` | Sair do ambiente virtual |
| `pytest tests/` | Rodar testes |

---

## ❓ Solução de Problemas

### Erro: "GEMINI_API_KEY not found"

**Problema:** API key não configurada

**Solução:**
```bash
# Verificar se arquivo .env existe
ls -la .env

# Se não existir, criar
cp .env.example .env

# Editar e adicionar sua chave
nano .env
```

### Erro: "No module named 'streamlit'"

**Problema:** Dependências não instaladas

**Solução:**
```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate      # Windows

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Port 8501 already in use"

**Problema:** Outra instância do Streamlit rodando

**Solução:**
```bash
# Opção 1: Parar processo anterior (Ctrl+C)

# Opção 2: Usar outra porta
streamlit run streamlit_app.py --server.port 8502
```

### Bot não responde ou demora muito

**Possíveis causas:**
1. **Internet lenta** - API precisa de conexão
2. **API Key inválida** - Verificar no console
3. **Limite de requisições** - Gemini tem limite gratuito

**Solução:**
```bash
# Verificar logs no terminal
# Se API key inválida, gerar nova em aistudio.google.com
```

### PDF não está sendo gerado

**Problema:** Reportlab não instalado ou erro no cronograma

**Solução:**
```bash
# Reinstalar reportlab
pip install --upgrade reportlab

# Se persistir, verificar logs no terminal
```

---

## 🎯 Dicas de Uso

### Para Melhores Resultados

1. **Seja específico no tema**
   - ❌ "Python"
   - ✅ "Python para automação de tarefas"

2. **Escolha metodologia adequada**
   - Iniciante → Shoshin
   - Memorização → Spaced Repetition
   - Foco → Pomodoro

3. **Seja realista com tempo**
   - Considere compromissos existentes
   - Melhor 30min/dia consistente que 4h esporádico

4. **Use o refinamento**
   - Primeiro cronograma é base
   - Ajuste conforme necessidade

5. **Salve o PDF**
   - Imprima ou salve em cloud
   - Consulte diariamente

### Atalhos de Teclado

- `Ctrl + Enter` - Enviar mensagem
- `Ctrl + L` - Limpar campo de entrada
- `R` - Recarregar app (se travou)

---

## 📚 Recursos Adicionais

### Documentação

- 📖 **README.md** - Visão geral do projeto
- 📋 **DOCUMENTACAO_COMPLETA.md** - Guia técnico detalhado
- 🎬 **APRESENTACAO.md** - Slides de apresentação
- 📝 **CHANGELOG.md** - Histórico de mudanças

### Links Úteis

- 🌐 **App Online:** https://chatbot-estudos.streamlit.app/
- 💻 **GitHub:** https://github.com/rafaelhgreco/chatbot_estudos
- 🤖 **Google Gemini API:** https://ai.google.dev/
- 🎨 **Streamlit Docs:** https://docs.streamlit.io/

### Suporte

- 🐛 **Bugs:** Abra issue no GitHub
- 💡 **Sugestões:** Abra discussion no GitHub
- ❓ **Dúvidas:** Consulte documentação ou abra issue

---

## 🎓 Exemplos de Uso

### Exemplo 1: Estudante Preparando Vestibular

```
Bot: Qual tema você gostaria de estudar?
Você: Física para ENEM - Mecânica e Eletromagnetismo

Bot: [Apresenta metodologias]
Você: Spaced Repetition

Bot: Quanto tempo disponível?
Você: 2 horas por dia durante a semana, 4 horas nos fins de semana

Bot: Qual prazo?
Você: 6 meses até o ENEM

Bot: Nível atual?
Você: Intermediário - sei o básico mas preciso revisar tudo

[Cronograma gerado com foco em revisões espaçadas]
```

### Exemplo 2: Profissional Mudando de Carreira

```
Bot: Qual tema você gostaria de estudar?
Você: React e TypeScript para desenvolvimento Frontend

Bot: [Apresenta metodologias]
Você: Shoshin - sou iniciante em programação web

Bot: Quanto tempo disponível?
Você: 1 hora e meia por dia após o trabalho

Bot: Qual prazo?
Você: 3 meses

Bot: Nível atual?
Você: Iniciante - só conheço HTML/CSS básico

[Cronograma com projetos práticos desde o início]
```

### Exemplo 3: Autodidata Estudando Hobby

```
Bot: Qual tema você gostaria de estudar?
Você: Violão - do zero até tocar músicas intermediárias

Bot: [Apresenta metodologias]
Você: Long-life Learning - quero aprender sem pressa

Bot: Quanto tempo disponível?
Você: 30 minutos por dia, com consistência

Bot: Qual prazo?
Você: 1 ano - sem pressa

Bot: Nível atual?
Você: Completo iniciante - nunca toquei

[Cronograma sustentável com foco em hábito diário]
```

---

## ✅ Checklist de Instalação

Use este checklist para garantir que tudo está funcionando:

- [ ] Python 3.10+ instalado (`python --version`)
- [ ] Código baixado/clonado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip list`)
- [ ] Arquivo `.env` criado
- [ ] API Key do Gemini configurada
- [ ] App iniciado com sucesso (`streamlit run streamlit_app.py`)
- [ ] Conversa teste completada
- [ ] PDF exportado com sucesso
- [ ] Tudo funcionando! 🎉

---

## 🚀 Próximos Passos

Após instalar e usar o chatbot:

1. ⭐ **Dê uma estrela** no GitHub se gostou
2. 🐛 **Reporte bugs** via issues
3. 💡 **Sugira melhorias** via discussions
4. 🤝 **Contribua** com código (PRs são bem-vindos!)
5. 📣 **Compartilhe** com amigos que possam se beneficiar

---

**Desenvolvido com ❤️ para ajudar pessoas a estudarem melhor**

*Última atualização: Novembro 2025*
