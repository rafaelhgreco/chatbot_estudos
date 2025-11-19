# 📚 Chatbot de Estudos Personalizados

Um chatbot inteligente que cria cronogramas de estudo personalizados baseados em metodologias comprovadas de aprendizagem, utilizando Google Gemini 2.5 Flash.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-estudos.streamlit.app/)

## 🎯 Funcionalidades

- 📝 **Coleta interativa de requisitos** - Conversa natural para entender seus objetivos
- 🎓 **Múltiplas metodologias** - Long-life Learning, Shoshin, Kumon, Pomodoro, Spaced Repetition, Feynman
- 📅 **Cronogramas personalizados** - Adaptados ao seu tempo, prazo e nível de conhecimento
- 🔄 **Refinamento iterativo** - Ajuste o cronograma com feedback em tempo real
- 📊 **Acompanhamento de progresso** - Visualize sua jornada de criação do cronograma

## 🏗️ Arquitetura

```
chatbot_estudos/
├── streamlit_app.py           # Interface principal do Streamlit
├── modules/
│   ├── workflow_manager.py    # Gerenciador de fluxo de conversa
│   └── prompt_templates.py     # Templates de prompts para Gemini
├── utils/
│   └── validators.py           # Validações de entrada com Pydantic
├── data/
│   └── metodologias.json       # Dados sobre metodologias
├── tests/                      # Testes unitários
├── .env                        # Variáveis de ambiente (API key)
└── requirements.txt
```

## 🚀 Como executar localmente

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Configure a API Key

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_api_aqui
```

Obtenha sua chave em: https://aistudio.google.com/app/apikey

### 3. Execute o app

```bash
streamlit run streamlit_app.py
```

## ☁️ Deploy no Streamlit Cloud

1. Faça push do código para o GitHub
2. Conecte seu repositório ao Streamlit Cloud
3. Configure o secret `GEMINI_API_KEY` nas configurações do app
4. Deploy automático!

## 📖 Como usar

1. **Inicie a conversa** - O chatbot te dará boas-vindas
2. **Informe o tema** - Ex: "Python para Data Science"
3. **Escolha a metodologia** - Selecione uma das sugeridas ou proponha outra
4. **Forneça parâmetros** - Tempo disponível, prazo e nível de conhecimento
5. **Receba o cronograma** - Gerado em segundos, personalizado para você
6. **Dê feedback** - Aprove ou solicite ajustes específicos
7. **Refine se necessário** - O chatbot ajusta com base no seu feedback

## 🎓 Metodologias Disponíveis

- **Long-life Learning** - Aprendizado contínuo e sustentável
- **Shoshin** - Mente de principiante, sem pressupostos
- **Kumon** - Progressão gradual com domínio completo
- **Pomodoro** - Técnica de gestão de tempo focada
- **Spaced Repetition** - Revisões em intervalos otimizados
- **Feynman** - Aprender ensinando e simplificando

## 🛠️ Stack Técnica

- **Python 3.11+**
- **Streamlit** - Interface interativa
- **Google Gemini 2.5 Flash** - Modelo de linguagem
- **Pydantic** - Validação de dados
- **python-dotenv** - Gerenciamento de variáveis

## 📝 Desenvolvimento

### Executar testes

```bash
pytest tests/
```

### Estrutura de estados

O chatbot usa uma máquina de estados para gerenciar o fluxo:

```
Inicial → Coletando Tema → Apresentando Metodologias → 
Coletando Parâmetros → Gerando Cronograma → 
Apresentando Cronograma → Coletando Feedback → 
Refinando (loop) → Aprovado
```

## 📚 Documentação

- [Planejamento Completo](PLANEJAMENTO.md) - Análise BDD e arquitetura detalhada
- [Metodologias](data/metodologias.json) - Descrição completa das metodologias

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Desenvolvido com ❤️ usando BDD, Google Gemini e Streamlit**
