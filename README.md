#  Assistente Virtual RAG - Clínica Médica +VIDA

Este projeto é um agente inteligente baseado em **RAG (Retrieval-Augmented Generation)** desenvolvido para responder dúvidas de pacientes e usuários com base em um documento interno de diretrizes/informações da clínica.

---

## Sobre o Projeto

A solução utiliza técnicas modernas de recuperação de informação e modelos de linguagem de grande porte (LLMs) para fornecer respostas precisas e contextualizadas, evitando alucinações ao se limitar estritamente ao conteúdo fornecido no documento em PDF.

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Orquestração RAG:** [LangChain](https://www.langchain.com/) (sintaxe LCEL)
- **Modelo de Linguagem (LLM):** `llama-3.3-70b-versatile` (via [Groq API](https://groq.com/))
- **Embeddings:** `all-MiniLM-L6-v2` (via `HuggingFaceEmbeddings`)
- **Banco de Dados Vetorial:** [Chroma DB](https://www.trychroma.com/) (com persistência local)
- **Leitura & Processamento:** `PyPDFLoader` + `RecursiveCharacterTextSplitter`

---

## Arquitetura da Solução

```text
[ Documento PDF ] ──> [ Text Splitter ] ──> [ HuggingFace Embeddings ]
                                                       │
                                                       ▼
[ Usuário (Terminal) ] ──> [ Retriever (MMR) ] ──> [ Chroma DB ]
         │                        │
         ▼                        ▼
[ Prompt Template ] ──> [ Groq / Llama 3.3 ] ──> [ Resposta no Console ]
Ingestão & Indexação: O documento PDF é lido, dividido em fragmentos (chunks de 1000 caracteres com overlap de 200) e convertido em vetores armazenados no ChromaDB.Carregamento Eficiente: O banco vetorial persiste localmente na pasta ./chroma.db, evitando reprocessar o PDF em execuções subsequentes.Recuperação (Retrieval): Utiliza busca por diversidade maximal (MMR - Maximal Marginal Relevance) recuperando os $k=2$ trechos mais relevantes.Geração (Generation): A pergunta do usuário junta-se ao contexto recuperado e é enviada ao Llama 3.3 via Groq para gerar a resposta final.🚀 Como Executar o ProjetoPré-requisitosPython instalado (versão 3.10 ou superior)Microsoft Visual C++ Redistributable (Necessário no Windows para suporte ao PyTorch/C10)

1. Clonar o repositório:
git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git) cd SEU_REPOSITORIO

2. Criar e ativar o ambiente virtual:
python -m venv .venv

#Para Windows (PowerShell):
.venv\Scripts\Activate.ps1

#Para Linux/Mac:
source .venv/bin/activate

3. Instalar as dependências:
pip install -r requirements.txt

4. Configurar as variáveis de ambiente
Crie um arquivo .env na raiz do projeto com as suas chaves de API:Fragmento do código
GROQ_API_KEY=sua_chave_groq_aqui
HF_TOKEN=seu_token_huggingface_aqui


5. Executar a aplicação
Certifique-se de que o arquivo documento_clinica.pdf está na raiz do projeto e execute:
python main.py

Exemplo de Uso e Respostas/Pergunta:Qual o horário de funcionamento da clínica?Resposta do Assistente:A clínica funciona de segunda a sexta-feira, das 08h às 18h, e aos sábados das 08h às 12h.