# 🛒 Assistente Virtual RAG - BimBam Buy

Este projeto é um agente inteligente de suporte baseado em **RAG (Retrieval-Augmented Generation)** desenvolvido para responder dúvidas de clientes sobre **entregas, frete, pagamentos, trocas, reembolsos e programa de afiliados** da plataforma **BimBam Buy**.

---

##  Sobre o Projeto

A solução utiliza técnicas modernas de recuperação de informação e modelos de linguagem de grande porte (LLMs) para fornecer respostas precisas e contextualizadas, alimentadas estritamente pelas políticas internas em PDF da loja.

O projeto oferece duas formas de interação:
1. **Interface Web Interativa (`app.py`)**: Desenvolvida com Streamlit para uso em navegador.
2. **Interface via Terminal (`main.py`)**: Execução rápida direta no console.

---

## Tecnologias Utilizadas

- **Linguagem de Programação:** Python 3.10+
- **Interface Web:** [Streamlit](https://streamlit.io/)
- **Orquestração RAG:** [LangChain](https://www.langchain.com/) (sintaxe LCEL)
- **Modelo de Linguagem (LLM):** `llama-3.3-70b-versatile` (via [Groq API](https://groq.com/))
- **Embeddings:** `all-MiniLM-L6-v2` (via `HuggingFaceEmbeddings`)
- **Banco de Dados Vetorial:** [Chroma DB](https://www.trychroma.com/)
- **Leitura Multi-Documentos:** `DirectoryLoader` + `PyPDFLoader` + `RecursiveCharacterTextSplitter`

---

## 🏗️ Arquitetura da Solução

```text
[ Pasta ./documentos/*.pdf ] ──> [ DirectoryLoader ] ──> [ Text Splitter ]
                                                                │
                                                                ▼
                                                   [ HuggingFace Embeddings ]
                                                                │
                                                                ▼
[ Usuário (Streamlit ou Terminal) ] ──> [ Retriever (MMR, k=5) ] ──> [ Chroma DB ]
                │                                     │
                ▼                                     ▼
       [ Prompt Template ] ──────────────> [ Groq / Llama 3.3 ] ──> [ Resposta ]
 Como Executar o Projeto
Pré-requisitos:
Python instalado (versão 3.10 ou superior)

Chave de API da Groq

Passo a Passo
Clonar o repositório:

Bash
git clone [https://github.com/SEU_USUARIO/RAG_BumBam_Buy.git](https://github.com/SEU_USUARIO/RAG_BumBam_Buy.git)
cd RAG_BumBam_Buy
Criar e ativar o ambiente virtual:

PowerShell
python -m venv .venv

# No Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# No Linux/Mac:
source .venv/bin/activate
Instalar as dependências:

Bash
python -m pip install -r requirements.txt
Configurar as variáveis de ambiente:
Crie um arquivo .env na raiz do projeto contendo a sua chave da Groq:

Fragmento do código
GROQ_API_KEY=sua_chave_groq_aqui
Organizar os Documentos:
Certifique-se de que a pasta documentos existe na raiz do projeto e contém os PDFs das políticas do BimBam Buy.

Modo de Execução
Você pode rodar a aplicação de duas maneiras:

Opção A: Interface Web (Streamlit) - Recomendado
Bash
python -m streamlit run app.py
Abre automaticamente no navegador no endereço http://localhost:8501.

Opção B: Interface via Terminal
Bash
python main.py
Executa o chat interativo diretamente na linha de comando.

--Exemplo de Uso
Usuário: Qual o limite para ter frete grátis na loja?

Assistente BimBam Buy: De acordo com a nossa Política de Envios, o frete é gratuito para compras acima de R$ 199,00 para todo o Brasil.