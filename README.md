# Contract-Rag

A Streamlit application for asking grounded questions about contract and maritime PDF documents. It uses retrieval-augmented generation (RAG) to retrieve relevant passages from an uploaded document before generating an answer with Google Gemini.

## What it uses

- **Streamlit** for the upload and chat interface
- **LangChain** for the document, splitter, embedding, and LLM integrations
- **PyPDFLoader** (`pypdf`) to read PDF pages
- **RecursiveCharacterTextSplitter** with 1,000-character chunks and 200-character overlap
- **Google Gemini**
  - `gemini-2.5-flash` for answers
  - `gemini-embedding-2-preview` for document embeddings
- **FAISS** for vector similarity search
- **python-dotenv** to load `GOOGLE_API_KEY` from `.env`
- **Docker** for containerized deployment

## Features

- Upload one PDF contract or maritime document per session
- Create a FAISS vector index from the document
- Retrieve the two most relevant chunks for each question
- Answer only from retrieved document context
- Preserve legal meaning and request clause/section citations where available
- Highlight missing information, conflicts, obligations, and penalty conditions when relevant
- Retain the chat history during the active Streamlit session

## Project structure

```text
Contract-Rag/
|-- app.py                 # Streamlit upload and chat UI
|-- rag_core.py            # PDF ingestion, FAISS indexing, and Gemini answers
|-- requirements.txt       # Python dependencies
|-- Dockerfile             # Container build instructions
|-- .env                   # Local Google API key (not committed)
|-- faiss_index/           # Locally saved FAISS index (generated)
`-- uploaded_document.pdf  # Most recently uploaded PDF (generated)
```

## Prerequisites

- Python 3.11 or later (the Docker image uses Python 3.11)
- A Google Gemini API key with access to the configured Gemini models

## Local setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install the dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

4. Start the application:

```powershell
streamlit run app.py
```

Open the local URL displayed by Streamlit, upload a PDF, wait for processing to finish, then ask questions in the chat box.

## How the RAG flow works

1. `app.py` saves the uploaded file as `uploaded_document.pdf`.
2. `build_vector_db()` loads PDF pages with `PyPDFLoader`.
3. The pages are split into overlapping chunks and embedded with Gemini.
4. FAISS stores the chunks and saves the generated index in `faiss_index/`.
5. For each question, `answer_query()` retrieves the two closest chunks.
6. Gemini receives those chunks and a contract/maritime analysis prompt, then returns a Markdown-formatted answer.

## Docker

Build the image:

```powershell
docker build -t contract-rag .
```

Run it, passing the API key as an environment variable:

```powershell
docker run --rm -p 8501:8501 -e GOOGLE_API_KEY=your_google_gemini_api_key contract-rag
```

Then visit `http://localhost:8501`.

## Current behavior and limitations

- The app processes a single uploaded PDF for the current browser session.
- Each processed upload overwrites `uploaded_document.pdf` and regenerates `faiss_index/`.
- Although the index is saved locally, the application currently builds a new index after an upload rather than loading a previously saved one.
- Retrieval uses `k=2`, so each answer is based on the two most similar chunks.
- The model is instructed to avoid outside knowledge; if the retrieved context does not contain the answer, it should say so.

## Troubleshooting

- **Gemini authentication errors:** confirm `GOOGLE_API_KEY` is present in `.env` locally, or passed with `-e GOOGLE_API_KEY=...` when using Docker.
- **Module import errors:** activate the virtual environment and reinstall with `pip install -r requirements.txt`.
- **No useful answer:** make the question more specific or verify that the relevant clause is present and readable in the uploaded PDF.
- **VS Code cannot resolve imports:** select the interpreter at `.venv\Scripts\python.exe` (or the virtual environment you created).

## Security note

Do not commit `.env`, uploaded PDFs, or generated FAISS indexes if they contain confidential contract information. These paths are excluded by the repository's ignore rules.
