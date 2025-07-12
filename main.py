from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from utils.pdf_loader import load_pdf
from utils.csv_loader import load_csv
from utils.youtube_loader import load_youtube
from utils.web_loader import load_webpage

def load_all_documents(sources: dict):
    all_docs = []
    if sources.get("pdfs"):
        for pdf in sources["pdfs"]:
            all_docs.extend(load_pdf(pdf))
    if sources.get("csvs"):
        for csv in sources["csvs"]:
            all_docs.extend(load_csv(csv))
    if sources.get("youtube_links"):
        for yt in sources["youtube_links"]:
            all_docs.extend(load_youtube(yt))
    if sources.get("webpages"):
        for url in sources["webpages"]:
            all_docs.extend(load_webpage(url))
    return all_docs

def build_vectorstore(docs,api_key: str):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    chunks=text_splitter.split_documents(docs)
    embeddings=OpenAIEmbeddings(openai_api_key=api_key)
    return FAISS.from_documents(chunks,embeddings),chunks
