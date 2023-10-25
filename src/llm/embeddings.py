from langchain.embeddings import OpenAIEmbeddings

def get_openai_embeddings():
    return OpenAIEmbeddings(model="text-embedding-ada-002")