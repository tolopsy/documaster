from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema.vectorstore import VectorStoreRetriever


def create_openai_conversation_chain(*, retriever: VectorStoreRetriever):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )
