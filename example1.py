
# chat service with chroma
import os
import shutil
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
load_dotenv ()


def load_chunks(docs):
    embeddings = OpenAIEmbeddings(
        model = "text-embeddings-ada-002"
    )
    vectorstore = Chroma(
        persist_directory="./chromadb",
        embedding_function=embeddings,
        collection_name="test_collection"
    )
    print("Adding documents to vectorstore")
    Chroma.add_documents(vectorstore, docs)
    print("Documents added to vectorstore")

def get_retriver():
    embeddings = OpenAIEmbeddings(
        model='text-embedding-ada-002'
    )
    vectorstore = Chroma(
        persist_directory="./chromadb",
        embedding_function=embeddings,
        collection_name="test_collection"
    )

    return vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)



LLM = ChatOpenAI(model = 'gpt-4o-mini')
retriever = get_retriver()
prompt = ChatPromptTemplate.from_template(
    """ you can answer any data from this {data}
      this is topic :{question}
"""
)

chain = ({"data":  retriever |format_docs,
          "question": RunnablePassthrough()}
          | prompt
          | LLM
          | StrOutputParser())
print(chain.invoke("is project useful?"))



# print(chain.invoke({'question': "dogs"}))

# response = chain.stream({'question': "dogs"})

# for r in response:
#     print(r, end="", flush= True)