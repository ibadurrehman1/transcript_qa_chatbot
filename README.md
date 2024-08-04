

# Medical QA Bot Demo

This repository showcases a Question-Answering (QA) bot specifically designed to assist doctors and patients in quickly retrieving information from old medical transcripts. By leveraging advanced natural language processing techniques, this bot enables efficient access to historical medical data, improving decision-making and patient care.

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ibadurrehman1/transcript_qa_chatbot.git
    cd transcript_qa_chatbot
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    ```

3. **Activate the Virtual Environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install Required Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```


5. **Create an Environment File**:
    - Create a file named `.env` in the project root directory and add the following content:
      ```plaintext
      GROQ_API_KEY="YOUR_GROQ_API_KEY"
      OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
      ```

    *Obtain API Keys*:

    - Create a GROQ API key from: [GROQ API Console](https://console.groq.com/keys)
    - Create an OpenAI API key from: [OpenAI Platform](https://platform.openai.com/docs/overview)

6. **Run the Application**:
    ```bash
    chainlit run main.py
    ```

## Frontend Instructions

1. **Ingest the Transcript File**:
    - Upload the transcript file in either `.txt` or `.pdf` format through the frontend interface.

2. **Start Chatting**:
    - Once the file is uploaded, you can start asking questions and the QA bot will retrieve the relevant information from the ingested transcript.

