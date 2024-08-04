from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document


def pdf_to_text(pdf_file_path):

    loader = PyPDFLoader(pdf_file_path)
    pages = loader.load()
    page_texts = [page.page_content for page in pages]
    return page_texts


def split_text(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)


def convert_to_docs(splits, document_name):
    docs = [
        Document(page_content=text, metadata={"source": document_name})
        for text in splits
    ]
    return docs


def create_vectorstore(splits):

    return Chroma.from_documents(splits, embedding=OpenAIEmbeddings())
