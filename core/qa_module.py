from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from prompts import contextualize_q_system_prompt, qa_system_prompt


def create_contextualize_prompt():

    return ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )


def create_qa_prompt():

    return ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )


def create_rag_chain(llm, retriever):
    contextualize_q_prompt = create_contextualize_prompt()
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_prompt = create_qa_prompt()
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    return create_retrieval_chain(history_aware_retriever, question_answer_chain)
