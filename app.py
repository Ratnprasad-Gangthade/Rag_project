import streamlit as st 
from  time import sleep

from rag_core import answer_query, build_vector_db

if "vector_db" not in st.session_state:
    st.session_state.vector_db=None

if "messages" not in st.session_state:
    st.session_state.messages=[]



## document loading 
def document_process(path):
    st.session_state.vector_db = build_vector_db(path)



### streamlit UI

st.subheader("Ask anything about the document ")
if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded=False

if not st.session_state.document_uploaded:
    file=st.file_uploader(label="select your pdf file", type="pdf")
    if file:
        with open("uploaded_document.pdf","wb") as f:
            f.write(file.getvalue())
        


        with st.spinner("processing >>>"):
            document_process("./uploaded_document.pdf")
        st.session_state.document_uploaded=True
        
        st.markdown("Document processed successfully ........")
        sleep(2)
        st.rerun()


if st.session_state.document_uploaded and st.session_state.vector_db:

    for message in st.session_state.messages:
        role=message["role"]
        content=message["content"]

        st.chat_message(role).markdown(content)


    query=st.chat_input("Ask Anything...")
    if query:

        st.session_state.messages.append({"role":"user","content":query})

        st.chat_message("user").markdown(query)
        answer = answer_query(st.session_state.vector_db, query=query, k=2)
        st.session_state.messages.append({"role":"assistant","content":answer})
        st.chat_message("assistant").markdown(answer)