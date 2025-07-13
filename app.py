# app.py
import streamlit as st
import os
import tempfile
from main import load_all_documents, build_vectorstore
from chains.qa_chain import build_qa_chain
from youtube_transcript_api import YouTubeTranscriptApi


st.set_page_config(page_title="Multi-Source Chatbot", layout="wide")
st.sidebar.title("🔐 API Key Setup")
user_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
st.title("🧠 Chat with Multiple Sources")

# Upload PDF and CSV files
uploaded_pdfs = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
uploaded_csvs = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

# Input YouTube links and webpage URLs
youtube_links = st.text_area("Enter YouTube links (comma-separated)")
webpages = st.text_area("Enter webpage URLs (comma-separated)")

# Convert UploadedFile objects into actual file paths using tempfile
pdf_paths = []
if uploaded_pdfs:
    for file in uploaded_pdfs:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            pdf_paths.append(tmp.name)

csv_paths = []
if uploaded_csvs:
    for file in uploaded_csvs:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(file.read())
            csv_paths.append(tmp.name)

# Prepare the sources dictionary
sources = {
    "pdfs": pdf_paths,
    "csvs": csv_paths,
    "youtube_links": [link.strip() for link in youtube_links.split(",") if link.strip()],
    "webpages": [url.strip() for url in webpages.split(",") if url.strip()]
}

# Handle document processing
if st.button("Process Sources"):
    if not user_api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
    else:
        with st.spinner("Loading and processing documents..."):
            os.environ["OPENAI_API_KEY"] = user_api_key  
            documents = load_all_documents(sources)
            vectorstore, chunks = build_vectorstore(documents,user_api_key)
            qa_chain = build_qa_chain(vectorstore,user_api_key)
            st.session_state.qa_chain = qa_chain
            st.success("Documents processed. Start chatting!")

# Chat Interface
if "qa_chain" in st.session_state:
    query = st.text_input("Ask a question:")
    if query:
        if not user_api_key:
            st.warning("Please enter your OpenAI API key in the sidebar.")
        else:
            os.environ["OPENAI_API_KEY"] = user_api_key  
            with st.spinner("Thinking..."):
                response = st.session_state.qa_chain.invoke({"query": query})
                st.write("### 💬 Answer:", response["result"])

                with st.expander("📚 Source Documents"):
                    for i, doc in enumerate(response["source_documents"]):
                        st.markdown(f"**Document {i+1}:**")
                        st.write(doc.page_content[:500])  
