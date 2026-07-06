from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def build_vector_db(pdf_path: str) -> FAISS:

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )

    vector_db = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    vector_db.save_local("faiss_index")

    return vector_db


def answer_query(vector_db: FAISS, query: str, k: int = 2) -> str:
    documents = vector_db.similarity_search(query=query, k=k)
    context = ""

    for doc in documents:
        context += doc.page_content + "\n"

    prompt = f""" You are an expert Contract and Maritime Document Analysis Assistant.

Answer ONLY from the provided context.

Rules:
- Never use outside knowledge or guess.
- If information is missing, clearly say so.
- Preserve the original legal meaning.
- Cite relevant Article, Clause, Section, or Heading.
- Merge related clauses when needed.
- Mention conflicts if found.
- Group obligations by responsible party.
- For penalties, include condition, penalty, and exception.
- Use clear markdown formatting.

                 context:{context} and
                 question is : {query} """

    result = llm.invoke(prompt)
    return result.content
