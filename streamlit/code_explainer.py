import streamlit as st
from openai import OpenAI

# Configure the OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Initial system message for the chatbot
system_message = {
    "role": "system",
    "content": "You will be provided with a piece of code, and your task is to explain it in a concise way..",
}


# Define the Streamlit app
def main():
    st.title("Code explainer chatbot")

    # Initialize chat history
    if "history" not in st.session_state:
        st.session_state.history = [
            system_message,
            {
                "role": "user",
                "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise.",
            },
        ]
        st.session_state.responses = []

    # Display chat history
    for i, msg in enumerate(st.session_state.history):
        if msg["role"] == "user" and i > 1:  # Skip initial user message
            st.write(f"You: {msg['content']}")
        elif msg["role"] == "assistant":
            st.write(f"AI: {msg['content']}")

    # User input
    user_input = st.text_input("You:", "")

    if st.button("Submit") and user_input:
        # Append user message to chat history
        st.session_state.history.append(
            {"role": "user", "content": user_input})

        # Make a completion request
        completion = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=st.session_state.history,
            temperature=0.7,
            stream=True,
        )

        # Extract and append the response message
        new_message = {"role": "assistant", "content": ""}

        for chunk in completion:
            if chunk.choices[0].delta.content:
                new_message["content"] += chunk.choices[0].delta.content

        st.session_state.history.append(new_message)

        # Clear the input box after submission
        st.session_state.responses.append(new_message["content"])
        st.rerun()


if __name__ == "__main__":
    main()
