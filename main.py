import os
from dotenv import load_dotenv

# Módulos do LangChain para a arquitetura RAG
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Carrega as chaves de API do arquivo .env
load_dotenv()

# ==============================================================================
# PIPELINE RAG (MODO CONSOLE)
# ==============================================================================

# Modelo de Embeddings HuggingFace (Vetorização)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
caminho_banco = "./chroma_bimbam_v2.db"

# Verificação e carregamento do Banco Vetorial ChromaDB
if os.path.exists(caminho_banco):
    banco_vetorial = Chroma(
        embedding_function=embeddings,
        persist_directory=caminho_banco,
        collection_name="bimbam_buy"
    )
else:
    # Carregamento em lote dos manuais e políticas em PDF
    leitor = DirectoryLoader(
        "./documentos",
        glob="./*.pdf",
        loader_cls=PyPDFLoader
    )
    documentos = leitor.load()

    # Divisão textual (Chunking) para otimizar a janela de contexto
    chunk_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    fatias_texto = chunk_splitter.split_documents(documentos)

    # Gravação e persistência local da base de conhecimento
    banco_vetorial = Chroma.from_documents(
        documents=fatias_texto,
        embedding=embeddings,
        persist_directory=caminho_banco,
        collection_name="bimbam_buy"
    )

# Configuração do algoritmo de busca (MMR com busca dos 7 melhores fragmentos)
retriever = banco_vetorial.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 7}
)

def format_docs(docs):
    """Formata os documentos retornados em um único bloco de texto."""
    return "\n\n".join(doc.page_content for doc in docs)

# Prompt de Engenharia: Restringe alucinações da IA
system_prompt = (
    "Você é o assistente virtual oficial da plataforma BimBam Buy. "
    "Responda à pergunta do usuário usando estritamente o contexto fornecido abaixo.\n"
    "Se a informação não estiver presente no contexto, responda de forma cordial que não encontrou "
    "as informações solicitadas nas políticas da loja.\n\n"
    "Contexto:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

# Inicialização da LLM (Groq - Llama 3.3)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
output_parser = StrOutputParser()

# Montagem da Cadeia RAG via LCEL
cadeia = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

# ==============================================================================
# INTERFACE DE LINHA DE COMANDO (CLI)
# ==============================================================================
VERDE = "\033[32m"
CIANO = "\033[36m"
VERMELHO = "\033[31m"
RESET = "\033[0m"

print("--- Assistente da BimBam Buy Iniciado (digite 'sair' para encerrar) ---")

while True:
    pergunta = input(f"\n{CIANO}Você: {RESET}")
    if pergunta.lower().strip() in ["sair", "quit", "exit"]:
        print(f"{VERMELHO}== Sessão encerrada =={RESET}")
        break
    
    resposta = cadeia.invoke(pergunta)
    print(f"{VERDE}Assistente:\n{resposta}{RESET}")