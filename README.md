# Data Analyst Chatbot

This repository contains the code for a **Data Analyst Chatbot** built using OpenAI's Assistant (Code Interpreter) and Streamlit. The chatbot allows users to upload datasets and interact with the data through natural language queries. It leverages OpenAI’s powerful data analysis capabilities to perform operations like summarization, visualization, and statistical analysis.

---

## Features

- **File Uploads**: Users can upload CSV files for analysis.
- **Natural Language Interaction**: Chat with the bot to analyze and explore the uploaded datasets.
- **Code Interpreter**: Executes Python code to generate insights, visualizations, and more.
- **Streamlit UI**: Provides an intuitive and interactive user interface for data analysis tasks.
- **File Management**: Upload, attach, and delete files seamlessly.

---

## How It Works

1. **File Upload**:
   - Upload your dataset via the Streamlit sidebar.
   - The file is securely sent to OpenAI for processing.

2. **Thread Initialization**:
   - A new chat thread is created for every session.
   - Files are attached to the thread, enabling the assistant to access the data.

3. **Chat Interaction**:
   - Ask questions like:
     - "What are the top 5 entries in this dataset?"
     - "Visualize the data distribution."
     - "Perform a correlation analysis."
   - Receive responses in text or visual form (e.g., charts).

4. **File Management**:
   - Delete files securely from the OpenAI storage via the sidebar.

---

## Prerequisites

- Python 3.8+
- OpenAI API key with access to Assistant and Code Interpreter features
- Streamlit library
- dotenv library for environment variables

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/data-analyst-chatbot.git
   cd data-analyst-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key and Assistant ID:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     ASSISTANT_ID=your_assistant_id
     ```

4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

---

## File Structure

```plaintext
.
├── app.py                 # Main application script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # Documentation
```

---

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Upload a dataset (CSV) in the sidebar.

3. Start chatting with the assistant in the main interface:
   - Example prompts:
     - "Summarize the dataset."
     - "Plot the distribution of column X."
     - "Find missing values in the dataset."

4. Manage uploaded files through the sidebar options.

---

## Example Interactions

- **Text Query**:
  - User: "Show me the first 5 rows of the dataset."
  - Assistant: Displays the first 5 rows as a table.

- **Visualization**:
  - User: "Generate a scatter plot of columns A and B."
  - Assistant: Displays the scatter plot.

---

## Known Issues and Limitations

1. **File Size Limits**: Restricted by OpenAI’s file upload limits.
2. **Processing Time**: Responses may take a few seconds due to API processing.
3. **Data Privacy**: Ensure sensitive data is anonymized before uploading.

---

## Future Enhancements

- Add support for more file types.
- Improve response time by optimizing API interactions.
- Enhance visualization options.

---


## Acknowledgments

- OpenAI for the Assistant and Code Interpreter API.
- Streamlit for the interactive user interface framework.

---

For any questions or suggestions, feel free to contact [davin@aiforindonesia.org].

