import uuid
from typing import List

import chainlit as cl
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from core.llm import get_llm
from core.qa_module import create_rag_chain
from core.text_processing import (
    convert_to_docs,
    create_vectorstore,
    pdf_to_text,
    split_text,
)

load_dotenv()


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    store = cl.user_session.get("store")

    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


async def file_to_text(file: cl.File):

    # check if file is a text file or a pdf file
    text_splits = []

    if file.name.endswith(".txt"):
        with open(file.path, "r", encoding="utf-8") as f:
            text = f.read()
            text_splits.extend(split_text(text))
    elif file.name.endswith(".pdf"):
        page_texts = pdf_to_text(file.path)
        for page_text in page_texts:
            text_splits.extend(split_text(page_text))
    return text_splits


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("session_id", str(uuid.uuid4()))
    cl.user_session.set("store", {})
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="This application serves as a Question-Answering (QA) bot specifically designed to assist users in retrieving information from medical transcripts. To begin, please upload a transcripts text or PDF file",
            accept={"text/plain": [".txt", ".py"], "application/pdf": [".pdf"]},
            max_size_mb=20,
            timeout=180,
        ).send()
    splitted_texts = []
    for file in files:
        msg = cl.Message(content=f"Processing `{file.name}`...")
        await msg.send()
        text_splits = await file_to_text(file)

        docs = convert_to_docs(text_splits, f"{file.name}-pl")
        splitted_texts.extend(docs)

    vector_db = create_vectorstore(splitted_texts)

    msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    await msg.update()

    llm = get_llm()
    retriever = vector_db.as_retriever()

    rag_chain = create_rag_chain(llm, retriever)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    cl.user_session.set("retriever", retriever)
    cl.user_session.set("conversational_rag_chain", conversational_rag_chain)


@cl.on_message
async def main(
    message: cl.Message,
):
    conversational_rag_chain = cl.user_session.get("conversational_rag_chain")
    session_id = cl.user_session.get("session_id")
    cb = cl.AsyncLangchainCallbackHandler()
    msg = cl.Message(content="")
    await msg.send()

    response = conversational_rag_chain.invoke(
        {"input": message.content}, {"configurable": {"session_id": session_id}}
    )

    msg.content = response["answer"]
    source_documents = response["context"]  # type: List[Document]

    text_elements: List[cl.Text] = []

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):

            source_name = source_doc.metadata["source"]
            # Create the text element referenced in the message
            text_elements.append(
                cl.Text(
                    content=source_doc.page_content, name=source_name, display="side"
                )
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            source = f"\n\n\nSources: {', '.join(source_names)}"
            await msg.stream_token(source)
        else:
            no_sources = "\n\n\nNo sources found"
            await msg.stream_token(no_sources)

    if text_elements != []:
        msg.elements = text_elements

    await msg.update()


if __name__ == "__main__":
    import subprocess

    subprocess.run(["chainlit", "run", "main.py"])
