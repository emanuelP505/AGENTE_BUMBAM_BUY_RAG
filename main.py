
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0)





embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

if os.path.exists("./chroma.db"):
    banco_vetorial = Chroma(
              embedding_function=embeddings,
              persist_directory="./chroma_bimbam.db",
              collection_name="bimbam_buy"
          )
else:
    leitor=DirectoryLoader(
        "./documentos",
        glob="./*.pdf",
        loader_cls=PyPDFLoader
    )

    documento=leitor.load()
    chunk=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
    fatias=chunk.split_documents(documento)
    banco_vetorial = Chroma.from_documents(
             documents=fatias,
             embedding=embeddings,
             persist_directory="./chroma_bimbam.db",
             collection_name="bimbam_buy"
         )

retriever=banco_vetorial.as_retriever(
    search_type="mmr",
    search_kwargs={"k":2}
)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

system_prompt = (
       "Você é o assistente virtual oficial da plataforma BimBam Buy. "
        "Responda à pergunta do usuário usando estritamente o contexto fornecido abaixo.\n"
        "Se a informação não estiver presente no contexto, responda de forma cordial que não encontrou "
        "as informações solicitadas nas políticas da loja.\n\n"
        "Contexto:\n{context}"
    )

prompt=ChatPromptTemplate.from_messages(
    [
       (
            "system",system_prompt
                
       ),
       ("user","{input}")
    ]
)

output_parser=StrOutputParser()

cadeia=({
    "context":retriever|format_docs,"input":RunnablePassthrough()
})|prompt|llm|output_parser


VERDE = "\033[32m"
CIANO = "\033[36m"
VERMELHO = "\033[31m"
RESET = "\033[0m"

print("--- Assistente da BumBam Buy Iniciado (digite 'sair' para encerrar) ---")
while True:
    pergunta=input(f"\n{CIANO}Você: {RESET}")
    if pergunta.lower().strip() in ["sair","quit","exit"]:
        print(f"{VERMELHO}==Sessao encerrada =={RESET}")
        break
    resposta=cadeia.invoke(pergunta)
    print(f"{VERDE} Assistente : \n {resposta}{RESET}")