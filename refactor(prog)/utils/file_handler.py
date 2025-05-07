from config import client
from utils.logger import logger
import streamlit as st

def upload_to_openai(file):
    try:
        response = client.files.create(file=(file.name, file), purpose="assistants")
        logger.info("File uploaded successfully: %s", response.id)
        return response.id
    except Exception as e:
        logger.error("Upload failed: %s", e)
        st.error(f"Upload failed: {e}")
        return None

def delete_openai_file(file_id):
    try:
        client.files.delete(file_id)
        logger.info("Deleted file: %s", file_id)
        st.success(f"Deleted file {file_id}")
    except Exception as e:
        logger.error("Delete failed: %s", e)
        st.error(f"Failed to delete file {file_id}: {e}")
