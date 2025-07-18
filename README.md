# 🤖 Streamlit Gemini Multimodal Chatbot

A user-friendly web application built with Streamlit that leverages the power of Google's Gemini 2.5 Flash model. This chatbot can engage in conversations and analyze a wide variety of uploaded files, including images, audio, video, PDFs, and more.

-----

## \#\# ✨ Features

  * **Interactive Chat Interface**: A clean and simple UI for natural conversation.
  * **True Multimodality**: Upload and ask questions about images, audio, videos, PDFs, text files, and more.
  * **Powered by Gemini 1.5 Pro**: Utilizes a powerful, state-of-the-art multimodal AI model from Google.
  * **Streaming Responses**: See the AI's response generate in real-time for a dynamic user experience.
  * **Conversation Management**: Easily start a new conversation to clear the history and context.

-----

## \#\# 🛠️ Technology Stack

  * **Language**: Python
  * **Framework**: Streamlit
  * **AI Model**: Google Gemini 1.5 Pro
  * **API Wrapper**: `google-generativeai` Python SDK

-----

## \#\# 🚀 Setup and Installation

Follow these steps to get the application running on your local machine.

### \#\#\# 1. Clone the Repository

```bash
git clone https://github.com/marisdarmawan/multimodal-genai.git
cd multimodal-genai
```

### \#\#\# 2. Create a Virtual Environment (Recommended)

  * **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
  * **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### \#\#\# 3. Install Dependencies

Install the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

-----

## \#\# ⚙️ Configuration

To use the chatbot, you need to provide your Google API key. The application is set up to use Streamlit's built-in secrets management.

1.  Create a new folder in your project's root directory named `.streamlit`.

2.  Inside the `.streamlit` folder, create a new file named `secrets.toml`.

3.  Add your Google API key to the `secrets.toml` file as shown below:

    ```toml
    # .streamlit/secrets.toml

    GOOGLE_API_KEY = "your_api_key_here"
    ```

Replace `"your_api_key_here"` with your actual API key from Google AI Studio.

-----

## \#\# ▶️ How to Run

Once you have completed the setup and configuration, run the following command in your terminal:

```bash
streamlit run app.py
```

The application will open automatically in a new tab in your web browser. Now you can start chatting with your AI assistant\!

-----

## \#\# 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

-----

## \#\# 🙏 Acknowledgments

This project is a modification of an original concept by **Mohammad Aris Darmawan**, adapted to use the full multimodal capabilities of the Google Gemini API.
