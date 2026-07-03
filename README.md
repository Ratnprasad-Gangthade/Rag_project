# RAG Pipeline

A simple Streamlit-based Retrieval-Augmented Generation (RAG) app for asking questions about an uploaded PDF document.

## Features

- Upload a PDF and process it into chunks
- Create embeddings with Google Gemini
- Store vectors in memory for fast similarity search
- Ask questions in a Streamlit chat interface
- Keep the UI separate from the core RAG logic

## Project Structure

- `app.py` - Streamlit frontend and chat flow
- `rag_core.py` - Core RAG pipeline, retrieval, and response generation
- `requirements.txt` - Python dependencies
- `.env` - Local environment variables, including your Google API key
- `.gitignore` - Prevents local environment and cache files from being tracked

## Requirements

- Python 3.13
- A Google Gemini API key
- The packages listed in `requirements.txt`

## Setup

1. Create and activate your virtual environment:

```powershell
.\env\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Add your Google API key to `.env`:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Run the App

Start the Streamlit app with:

```powershell
streamlit run app.py
```

Then open the local URL shown in the terminal.

## How It Works

1. Upload a PDF in the Streamlit UI.
2. The app saves it locally as `uploaded_document.pdf`.
3. `rag_core.build_vector_db()` loads the PDF, splits it into chunks, and creates embeddings.
4. When you ask a question, `rag_core.answer_query()` retrieves the most relevant chunks and sends them to Gemini.
5. The answer is shown in the chat UI.

## Notes

- The app currently uses an in-memory vector store, so the index is rebuilt each time the app restarts.
- `uploaded_document.pdf` is a temporary local file and is ignored by Git.
- Keep your `.env` file private because it contains your API key.

## Troubleshooting

- If imports are not resolved in VS Code, make sure the interpreter is set to `env/Scripts/python.exe`.
- If the app cannot access Gemini, confirm that `GOOGLE_API_KEY` is present in `.env`.
- If you upload a new PDF, the previous in-memory index will be replaced after processing.
