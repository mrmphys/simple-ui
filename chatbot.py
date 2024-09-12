import streamlit as st
import requests

# Set page configuration to center the content
st.set_page_config(page_title="Chipper Chatbot", layout="centered")

# Display the chatbot name at the top with blue color
st.markdown("<h1 style='color: blue;'>Chipper</h1>", unsafe_allow_html=True)

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Function to send the request to the chatbot API endpoint and get a response
def get_bot_response(user_input, history):
    # Prepare the payload in the required format
    payload = {
        "message": user_input,
        "history": history
    }

    try:
        # Send the request to the endpoint
        response = requests.post(
            "https://chipper-meds-1f42429118d4.herokuapp.com/generate",
            json=payload
        )

        # Check if the response is successful
        if response.status_code == 200:
            # Extract the bot's response from the API response
            return response.json().get("response", "Chipper: I couldn't understand that.")
        else:
            # Handle the case where the response is not successful
            return "Chipper: Sorry, I encountered an error. Please try again."
    except Exception as e:
        # Handle any exceptions during the request
        return f"Chipper: An error occurred: {e}"


# Chat input area in the main container
st.write("### Chat with Chipper")

# Create a form for user input to keep the chat UI clean
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "", key="input")
    submit_button = st.form_submit_button("Send")

# Process the input when the form is submitted
if submit_button and user_input:
    # Convert session messages into the required history format
    history = [{"role": "user" if msg["sender"] == "User" else "model", "parts": msg["text"]} for msg in
               st.session_state.messages]

    # Get the response from the bot by calling the API
    bot_response = get_bot_response(user_input, history)

    # Add user message and bot response to chat history
    st.session_state.messages.append({"sender": "User", "text": user_input})
    st.session_state.messages.append({"sender": "Bot", "text": bot_response})

# Display the conversation history with the most recent messages at the top
for message in reversed(st.session_state.messages):
    if message["sender"] == "User":
        st.markdown(f"**You:** {message['text']}")
    else:
        st.markdown(f"**Chipper:** {message['text']}")
