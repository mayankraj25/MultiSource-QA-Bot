from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

def build_qa_chain(vectorstore,api_key: str):
    retriever=vectorstore.as_retriever()
    llm=ChatOpenAI(model="gpt-4o-mini",temperature=0.1,openai_api_key=api_key)
    qa_chain=RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )
    qa_chain.return_source_documents = True
    return qa_chain
