import streamlit as st
import google.generativeai as genai
import io
import os

# --- Application Configuration ---
st.set_page_config(
    page_title="🤖 Gemini Multimodal Chatbot",
    page_icon="✨",
    layout="centered",
)

# --- Google Gemini Model Initialization and Secret Management ---
google_api_key = st.secrets.get("GOOGLE_API_KEY")
model = None

if google_api_key:
    try:
        genai.configure(api_key=google_api_key)
        # Using a powerful multimodal model like gemini-1.5-pro
        # It's excellent for handling various file types.
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Failed to configure Google API: {e}")
else:
    st.error("Google API Key not found. Please set it in your secrets.toml file.")

# --- UI Elements ---
st.title("🤖 Chat with Google Gemini")
st.caption("Ask a question, or upload a file from the sidebar to discuss it.")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm an AI assistant powered by Google Gemini. How can I help you today?"}
    ]
# This will store the uploaded file's data for the *next* chat message
if "uploaded_file_data" not in st.session_state:
    st.session_state.uploaded_file_data = None

# --- Sidebar ---
with st.sidebar:
    st.header("Controls & Information")

    # --- File Uploader for Multimodal Input ---
    # Gemini 1.5 Pro supports a wide range of file types.
    # See docs: https://ai.google.dev/gemini-api/docs/prompting_with_media
    uploaded_file = st.file_uploader(
        "Upload a file (optional)",
        type=["png", "jpg", "jpeg", "gif", "webp", "mp3", "wav", "aiff", "aac", "ogg", "flac", "mp4", "mov", "avi", "webm", "txt", "pdf", "docx", "md", "py", "json", "html", "css"],
        help="Upload an image, audio, video, or document to discuss with the chatbot."
    )

    if uploaded_file is not None:
        # Store file details in session state to be used with the next prompt
        st.session_state.uploaded_file_data = {
            "name": uploaded_file.name,
            "type": uploaded_file.type,
            "data": uploaded_file.getvalue()
        }
        st.success(f"File '{uploaded_file.name}' is ready. It will be sent with your next message.")

    st.markdown("---")
    if st.button("Start New Conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "New conversation started! Go ahead and type your message."}
        ]
        st.session_state.uploaded_file_data = None
        st.rerun()

    st.markdown("---")
    st.header("About This Bot")
    st.markdown("""
    This bot uses a multimodal AI model from Google to assist you.
    Simply type your request or upload a file and see the magic! ✨
    """)
    st.subheader("Model Used:")
    st.markdown("Google Gemini 2.5 Flash")
    st.markdown("---")
    st.markdown("Original code by Mohammad Aris Darmawan (Modified for Multimodal Gemini API)")

# --- Chat History Display ---
for message in st.session_state.messages:
    # The API uses "model" for assistant's role, but we display "assistant"
    role = "assistant" if message["role"] == "model" else message["role"]
    with st.chat_message(role):
        st.markdown(message["content"])

# --- Chat Input and Google Gemini API Call Logic ---
user_prompt = st.chat_input("Type your message here...")

if user_prompt and model:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Prepare chat history for the Google API
            # Format: {'role': 'user'/'model', 'parts': [text]}
            chat_history = []
            for msg in st.session_state.messages[:-1]: # All but the last user prompt
                role = "model" if msg["role"] == "assistant" else msg["role"]
                chat_history.append({"role": role, "parts": [msg["content"]]})

            # --- Prepare the final prompt with text and/or file ---
            prompt_parts = []
            
            # If a file was uploaded, add it to the prompt parts
            if st.session_state.get("uploaded_file_data"):
                file_data = st.session_state.uploaded_file_data
                prompt_parts.append({
                    "mime_type": file_data["type"],
                    "data": file_data["data"]
                })
                # Clear the file from session state after using it once
                st.session_state.uploaded_file_data = None
            
            # Add the user's text prompt
            prompt_parts.append(user_prompt)

            # Start a chat session with the existing history
            chat_session = model.start_chat(history=chat_history)
            
            # Send the final prompt (with file and text) in a streaming fashion
            response = chat_session.send_message(prompt_parts, stream=True)

            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌") # Typing effect
            
            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Oops! An error occurred with the Google API: {e}")
            full_response = "Sorry, I'm having trouble connecting right now. 🥺"
            message_placeholder.markdown(full_response)

    # Save the complete response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

elif not model and user_prompt:
    st.warning("Chatbot is not active. Please configure your Google API Key correctly.")
