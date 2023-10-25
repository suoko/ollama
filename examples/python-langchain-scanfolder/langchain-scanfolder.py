# You will need to run "pip install langchain pypdf chromadb tiktoken docx2txt unstructured" before

import sys
import os
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredHTMLLoader

from langchain.llms import Ollama
ollama = Ollama(base_url='http://localhost:11434', 
model="llama2")
#model="starcoder")



#print(ollama("why is the sky blue"))


documents = []
for file in os.listdir("/home/user/docs"):
    if file.endswith(".pdf"):
        pdf_path = "/home/user/docs/" + file
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())
    elif file.endswith('.docx') or file.endswith('.doc'):
        doc_path = "/home/user/docs/" + file
        loader = Docx2txtLoader(doc_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        text_path = "/home/user/docs/" + file
        loader = TextLoader(text_path)
        documents.extend(loader.load())
    elif file.endswith('.html') or file.endswith('.htm'):
        text_path = "/home/user/docs/" + file
        loader = UnstructuredHTMLLoader(text_path)
        documents.extend(loader.load())


text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=20)
all_splits = text_splitter.split_documents(documents)

from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

question="in case of problems with the inverter 3PH 10KTL-15KTL-V2, which steps do I have to follow ?"
docs = vectorstore.similarity_search(question)
len(docs)

from langchain.chains import RetrievalQA
qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
print(qachain({"query": question}))
