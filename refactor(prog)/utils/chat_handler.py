import time
import io
import streamlit as st
from config import client, ASSISTANT_ID
from utils.logger import logger
from instruction import INSTRUCTIONS

def create_thread_and_attach_file(file_id):
    try:
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Please analyze the uploaded data file.",
            attachments=[{"file_id": file_id, "tools": [{"type": "code_interpreter"}]}]
        )
        return thread.id
    except Exception as e:
        logger.error("Thread creation/attachment failed: %s", e)
        st.sidebar.error(f"Thread creation failed: {e}")
        return None

def run_assistant(thread_id, user_input):
    try:
        client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_input)
        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=ASSISTANT_ID, instructions=INSTRUCTIONS)

        while run.status not in ["completed", "failed"]:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        return run
    except Exception as e:
        logger.error("Assistant run error: %s", e)
        st.error(f"Assistant run error: {e}")
        return None

def get_assistant_messages(thread_id, run_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return [msg for msg in messages if msg.run_id == run_id and msg.role == "assistant"]
