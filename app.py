import os
import streamlit as st
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

# Configuração para página Web
st.set_page_config(page_title="Assistente da BimBam Buy", page_icon="🛒")
st.title("🛒 Assistente de Suporte - BimBam Buy")
st.caption("Tire suas dúvidas sobre entregas, pagamentos, trocas, reembolsos e afiliados.")

# Cache para carregar o RAG uma única vez na memória
@st.cache_resource
def carregar_cadeia():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists("./chroma_bimbam_v2.db"):
     banco_vetorial = Chroma(
        embedding_function=embeddings,
        persist_directory="./chroma_bimbam_v2.db",
        collection_name="bimbam_buy"
    )
    else:
        leitor_pasta= DirectoryLoader(
            "./documentos",
            glob="./*.pdf",
            loader_cls=PyPDFLoader
        )
        documento = leitor_pasta.load()
        chunk = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        fatias = chunk.split_documents(documento)
        banco_vetorial = Chroma.from_documents(
            documents=fatias,
            embedding=embeddings,
            persist_directory="./chroma_bimbam.db",
            collection_name="bimbam_buy"
        )

    retriever = banco_vetorial.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 7}
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

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    output_parser = StrOutputParser()

    return (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )

cadeia = carregar_cadeia()

#Logica do Histórico da conversa e sua Interface

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Como posso ajudar você hoje?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if pergunta := st.chat_input("Digite sua pergunta..."):
    st.session_state.messages.append({"role": "user", "content": pergunta})
    st.chat_message("user").write(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Buscando informações no documento..."):
            resposta = cadeia.invoke(pergunta)
            st.write(resposta)
    
    st.session_state.messages.append({"role": "assistant", "content": resposta})