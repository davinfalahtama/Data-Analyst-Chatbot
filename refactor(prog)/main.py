import streamlit as st
from config import client
from components.sidebar import sidebar_file_manager
from utils.chat_handler import create_thread_and_attach_file, run_assistant, get_assistant_messages

st.set_page_config(page_title="Chat with Your Data", page_icon=":bar_chart:")
sidebar_file_manager()

# Inisialisasi session state...

# Buat thread jika perlu
if st.session_state.file_id_list and st.session_state.thread_id is None:
    thread_id = create_thread_and_attach_file(st.session_state.file_id_list[0])
    if thread_id:
        st.session_state.thread_id = thread_id
        st.session_state.start_chat = True

# Chat UI dan logika percakapan...
