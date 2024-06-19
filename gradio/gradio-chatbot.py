import gradio as gr
from openai import OpenAI

# Configure the OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Initial system message for the chatbot
system_message = {
    "role": "system",
    "content": "You will be provided with a piece of code, and your task is to explain it in a concise way."
}

# Initialize chat history
history = [
    system_message,
    {
        "role": "user",
        "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."
    }
]


def chatbot(user_input, chat_history):
    global history

    # Append user message to chat history
    history.append({"role": "user", "content": user_input})

    # Make a completion request
    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    # Extract and append the response message
    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)

    # Update the chat history with the new messages
    chat_history.append(
        ("You: " + user_input, "AI: " + new_message["content"]))

    return "", chat_history  # Clear the input box and update chat history


def reset_chat():
    """Reset the chat history."""
    global history
    history = [
        system_message,
        {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."}
    ]
    return [("", "")]  # Clear the chat history in the UI


with gr.Blocks() as demo:
    gr.Markdown("## Code Explainer Chatbot")

    chatbot_ui = gr.Chatbot()
    user_input = gr.Textbox(
        placeholder="Enter your code or question here...", lines=4)
    submit_button = gr.Button("Submit")
    clear_button = gr.Button("Clear Chat")

    # Bind actions
    submit_button.click(chatbot, [user_input, chatbot_ui], [
                        user_input, chatbot_ui])
    user_input.submit(chatbot, [user_input, chatbot_ui], [
                      user_input, chatbot_ui])
    clear_button.click(reset_chat, [], chatbot_ui)

demo.launch()
