# 🏛️ Alexandri.ia

O **Alexandri.ia** é um tutor educacional inteligente com foco estrito em **História e Geografia**. Desenvolvido em Python com a interface construída em Streamlit, o chatbot utiliza o poder da LLM do Google (Gemini) para responder dúvidas, ler materiais de estudo e gerar quizzes interativos, tudo em uma interface limpa, intuitiva e agradável.

## ✨ Funcionalidades

* **🤖 Tutor Especializado:** Prompt engessado para atuar estritamente como professor de História e Geografia, fornecendo respostas curtas e didáticas.
* **📂 Histórico de Conversas:** Salvamento automático de sessões em arquivos `.json` locais. O usuário pode alternar entre chats antigos a qualquer momento pela barra lateral.
* **📎 Análise de Material (RAG Simples):** Upload de arquivos `.txt` e `.pdf`. O bot lê o conteúdo e utiliza o material como contexto para responder às dúvidas do usuário.
* **🎯 Modo Quiz:** Geração de perguntas de múltipla escolha sob demanda para testar o conhecimento do estudante.
* **🎨 UI/UX Otimizada:** Interface customizada via CSS injetado, com barra lateral proporcional, botões responsivos e leitura confortável.

## 🛠️ Tecnologias Utilizadas

* **[Python 3](https://www.python.org/)** - Linguagem principal
* **[Streamlit](https://streamlit.io/)** - Framework para a interface web
* **[Google Generative AI (Gemini)](https://aistudio.google.com/)** - LLM utilizada (modelo `gemini-2.5-flash`)
* **[PyPDF2](https://pypi.org/project/PyPDF2/)** - Extração de texto de arquivos PDF
* **[Pillow (PIL)](https://pillow.readthedocs.io/)** - Manipulação das imagens de avatar e logo
* **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Gerenciamento de variáveis de ambiente

## 📁 Estrutura do Projeto

A arquitetura do projeto foi pensada para manter o código-fonte isolado das configurações globais:

```
ChatbotEduPython/
├── .env                  # Variáveis de ambiente (Chave da API)
└── src/                  # Código-fonte principal
    ├── assets/           # Imagens estáticas (logos, avatares)
    ├── conversas_salvas/ # Histórico de chats armazenados em JSON
    └── app.py            # Script principal da aplicação Streamlit

```

🚀 Como Executar

1. Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina. É recomendado o uso de um ambiente virtual (venv).

2. Instalação das dependências
Abra o terminal na raiz do projeto e instale as bibliotecas necessárias:

```
Bash

pip install streamlit google-generativeai pypdf2 python-dotenv pillow

```

1. Configuração da API
Crie um arquivo chamado .env na raiz do projeto (fora da pasta src) e adicione sua chave de API do Google Gemini:

```
Snippet de código

GEMINI_API_KEY=sua_chave_de_api_aqui

```

1. Rodando a Aplicação
Navegue até a pasta src e inicie o servidor do Streamlit:

```
Bash

cd src
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão no endereço <http://localhost:8501>.

👩‍💻 Desenvolvedora
Projeto desenvolvido por Karolini, estudante de Tecnologias da Informação e Comunicação (TIC).
O foco desta aplicação foi alinhar a integração de APIs de Inteligência Artificial com boas práticas de design de interface (UI) e garantia de qualidade da experiência do usuário (QA).
