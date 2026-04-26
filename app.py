import streamlit as st
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline


# -------------------------------
# 📄 Extract text from PDFs
# -------------------------------
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
    return text


# -------------------------------
# ✂️ Better chunking
# -------------------------------
def get_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250
    )
    return splitter.split_text(text)


# -------------------------------
# 🔢 Vector store (persistent + reusable)
# -------------------------------
@st.cache_resource
def get_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"  # 🔥 better embedding
    )

    db = Chroma.from_texts(
        chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    return db


# -------------------------------
# 🤖 Balanced LLM (FAST + GOOD)
# -------------------------------
@st.cache_resource
def load_llm():
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",   # ⚡ balanced model
        max_new_tokens=256,
        temperature=0.3
    )
    return HuggingFacePipeline(pipeline=pipe)


# -------------------------------
# ❓ RAG function (smart retrieval)
# -------------------------------
def answer_question(vector_store, question):
    # 🔥 retrieve with score
    results = vector_store.similarity_search_with_score(question, k=6)

    # 🔥 filter irrelevant chunks
    docs = [doc for doc, score in results if score < 0.75]

    if not docs:
        docs = [doc for doc, _ in results[:3]]  # fallback

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a helpful AI assistant.

Answer the question using the context below.

Rules:
- Do NOT repeat instructions
- Give clear and structured answers
- If partially available, explain what is found
- Only say "I couldn't find relevant information" if truly nothing matches

Context:
{context}

Question: {question}

Answer:
"""

    llm = load_llm()
    response = llm.invoke(prompt)

    return response, docs


# -------------------------------
# 🌐 UI
# -------------------------------
def main():
    st.set_page_config(page_title="DocQuery AI", layout="wide")

    st.title("📄 Ask My PDF - AI ChatBot")
    st.caption("Fast + Accurate PDF Q&A 🚀")

    # Sidebar
    with st.sidebar:
        st.header("📂 Upload PDFs")
        pdf_docs = st.file_uploader(
            "Upload PDF files",
            accept_multiple_files=True
        )
        process = st.button("🚀 Process Documents")

    # Session state
    if "db" not in st.session_state:
        st.session_state.db = None

    # Process PDFs
    if process and pdf_docs:
        with st.spinner("Processing documents..."):
            text = get_pdf_text(pdf_docs)
            chunks = get_chunks(text)
            st.session_state.db = get_vector_store(chunks)
        st.success("✅ Documents processed!")

    # Question input
    question = st.text_input("💬 Ask a question")

    if question:
        if st.session_state.db is None:
            st.warning("⚠️ Upload and process PDFs first")
        else:
            with st.spinner("Thinking..."):
                answer, docs = answer_question(
                    st.session_state.db,
                    question
                )

            st.subheader("📌 Answer")
            st.write(answer)

            # 🔍 Debug (important for learning)
            with st.expander("🔍 Retrieved Context"):
                for i, d in enumerate(docs):
                    st.write(f"Chunk {i+1}:")
                    st.write(d.page_content[:400] + "...")


# -------------------------------
# ▶️ Run app
# -------------------------------
if __name__ == "__main__":
    main()