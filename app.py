import os
from dotenv import load_dotenv
import openai
import time
import streamlit as st
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
client = openai.Client(api_key=os.environ.get("OPENAI_API_KEY"))
ASSISTANT_ID = os.environ.get("ASSISTANT_ID")

# Initialize Streamlit Page
st.set_page_config(page_title="Chat with Your Data", page_icon=":bar_chart:")

# Initialize all session states
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "generated_file_ids" not in st.session_state:
    st.session_state.generated_file_ids = []

# Function to upload file to OpenAI
def upload_to_openai(filepath):
    try:
        with open(filepath, "rb") as file:
            response = client.files.create(file=(os.path.basename(filepath), file),
                                           purpose="assistants")
        logger.info("File uploaded successfully with file ID: %s", response.id)
        return response.id
    except Exception as e:
        logger.error("File upload failed: %s", e)
        st.error(f"File upload failed: {e}")
        return None

# Function to delete file from OpenAI
def delete_openai_file(file_id):
    try:
        client.files.delete(file_id)
        logger.info("File %s deleted successfully from OpenAI.", file_id)
        st.success(f"File {file_id} deleted successfully from OpenAI.")
    except Exception as e:
        logger.error("Failed to delete file %s: %s", file_id, e)
        st.error(f"Failed to delete file {file_id}: {e}")

# Sidebar for File Upload and Deletion
st.sidebar.header("File Management")
file_uploaded = st.sidebar.file_uploader("Upload a file to analyze", type=["csv"])

# Upload Button
if st.sidebar.button("Upload File"):
    if file_uploaded:
        # Save file locally
        file_path = f"{file_uploaded.name}"
        with open(file_path, "wb") as f:
            f.write(file_uploaded.getbuffer())
        
        # Upload to OpenAI
        uploaded_file_id = upload_to_openai(file_path)
        if uploaded_file_id:
            st.session_state.file_id_list.append(uploaded_file_id)
            st.sidebar.success(f"File uploaded successfully! File ID: {uploaded_file_id}")
        else:
            st.sidebar.error("Failed to upload file to OpenAI.")

# Button to Delete All Uploaded Files
if st.sidebar.button("Delete All Uploaded Files"):
    for file_id in st.session_state.file_id_list:
        delete_openai_file(file_id)
    st.session_state.file_id_list = []  # Clear list after deletion

# Button to Delete Generated Files
if st.sidebar.button("Delete Generated Files"):
    for file_id in st.session_state.generated_file_ids:
        delete_openai_file(file_id)
    st.session_state.generated_file_ids = []  # Clear list after deletion

# Start a thread and attach file
if st.session_state.file_id_list and st.session_state.thread_id is None:
    try:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        logger.info("New thread created with ID: %s", thread.id)
        st.sidebar.success(f"New thread created: {thread.id}")

        # Attach file to thread
        file_id = st.session_state.file_id_list[0]
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content="Please analyze the uploaded data file.",
            attachments=[{"file_id": file_id, "tools": [{"type": "code_interpreter"}]}]
        )
        logger.info("File %s attached successfully to the thread.", file_id)
        st.sidebar.success("File attached successfully to the thread.")
        st.session_state.start_chat = True
    except Exception as e:
        logger.error("Failed to create thread or attach file: %s", e)
        st.sidebar.error(f"Failed to create thread or attach file: {e}")

# Main Chat Section
st.title("Chat with Your Data :bar_chart:")

# Display Messages
for message in st.session_state.messages:
    if message["type"] == "text":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    elif message["type"] == "image":
        with st.chat_message("assistant"):
            st.image(message["content"], caption="Assistant Response")

# User Input and Chat Process
if st.session_state.start_chat:
    if prompt := st.chat_input("Ask me anything about the data!"):
        # Add User Message
        st.session_state.messages.append({"type": "text", "role": "user", "content": prompt})
        logger.info("User input received: %s", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Send message to OpenAI API
        try:
            logger.info("Sending user input to OpenAI API...")
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )

            # Run assistant with max tokens
            logger.info("Starting assistant run with token limits...")
            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=ASSISTANT_ID,
                instructions="Please analyze the uploaded file and answer any questions based on its content.",
            )

            # Wait for assistant response
            with st.spinner("Thinking..."):
                while run.status not in ["completed", "failed"]:
                    logger.info("Run ID: %s - Status: %s (waiting)", run.id, run.status)
                    time.sleep(1)
                    run = client.beta.threads.runs.retrieve(
                        thread_id=st.session_state.thread_id, run_id=run.id
                    )

                if run.status == "failed":
                    logger.error("Run failed with ID: %s. Possible input or configuration issue.", run.id)
                    st.error(f"Assistant run failed. Run ID: {run.id}. Please check your inputs and try again.")
                elif run.status == "completed":
                    logger.info("Run completed with status: %s", run.status)

            # Retrieve assistant messages if run was successful
            if run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
                assistant_messages = [msg for msg in messages if msg.run_id == run.id and msg.role == "assistant"]

                # Display assistant response
                for msg in assistant_messages:
                    for content in msg.content:
                        if hasattr(content, "text"):
                            response_text = content.text.value
                            st.session_state.messages.append({"type": "text", "role": "assistant", "content": response_text})
                            logger.info("Assistant response: %s", response_text)
                            with st.chat_message("assistant"):
                                st.markdown(response_text)
                        elif hasattr(content, "image_file"):
                            # Display Generated Images
                            image_file_id = content.image_file.file_id
                            logger.info("Processing image with file ID: %s", image_file_id)
                            st.session_state.generated_file_ids.append(image_file_id)
                            try:
                                image_response = client.files.content(image_file_id)
                                if image_response:
                                    image_bytes = io.BytesIO(image_response.read())
                                    st.session_state.messages.append({"type": "image", "role": "assistant", "content": image_bytes})
                                    with st.chat_message("assistant"):
                                        st.image(image_bytes, caption="Assistant Response")
                            except Exception as e:
                                logger.error("Error while processing image file ID %s: %s", image_file_id, e)
        except Exception as e:
            logger.error("An error occurred: %s", e)
            st.error(f"An error occurred: {e}")

# Cleanup Uploaded Files (optional)
if st.session_state.file_id_list and st.sidebar.button("End Chat and Delete Files"):
    for file_id in st.session_state.file_id_list:
        delete_openai_file(file_id)
    st.session_state.file_id_list = []
    st.session_state.start_chat = False
    st.session_state.thread_id = None
    st.session_state.messages = []
    logger.info("All uploaded files deleted, and chat session ended.")
    st.success("All uploaded files deleted, and chat session ended.")
