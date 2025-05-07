import streamlit as st
from utils.file_handler import upload_to_openai, delete_openai_file

def sidebar_file_manager():
    st.sidebar.header("File Management")
    file_uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    if st.sidebar.button("Upload File") and file_uploaded:
        file_id = upload_to_openai(file_uploaded)
        if file_id:
            st.session_state.file_id_list.append(file_id)

    if st.sidebar.button("Delete All Uploaded Files"):
        for file_id in st.session_state.file_id_list:
            delete_openai_file(file_id)
        st.session_state.file_id_list.clear()

    if st.sidebar.button("Delete Generated Files"):
        for file_id in st.session_state.generated_file_ids:
            delete_openai_file(file_id)
        st.session_state.generated_file_ids.clear()
