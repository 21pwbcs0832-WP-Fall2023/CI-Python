import gradio as gr
from example1 import chain

# Define the function for handling chat
def chat(question, history):
    if question == "":
        response = "Please ask a question"
        history.append({"role": "assistant", "content": response})
    else:
        response = chain.stream(question)
        history.append({"role": "assistant", "content": ""})

        for i in response:
            history[-1]['content'] += i
            yield "", history

# Create the Gradio interface
with gr.Blocks(title="Chat with GPT-4") as demo:
    gr.Markdown("# Chat with GPT-4 DEMO")
    with gr.Row():
        gr.Markdown("")
    with gr.Column(scale=6):
        chatbox = gr.Chatbot(type="messages")
        with gr.Row():
            textbox = gr.Textbox(
                scale=7, container=False, placeholder="Ask a question"
            )
            submit_button = gr.Button(value="Submit", scale=3, variant="primary")
    gr.Markdown("")

    # Define the event listeners inside the `with gr.Blocks` context
    textbox.submit(chat, inputs=[textbox, chatbox], outputs=[textbox, chatbox])
    submit_button.click(chat, inputs=[textbox, chatbox], outputs=[textbox, chatbox])

# Launch the Gradio interface
demo.launch(
    server_name = "0.0.0.0",
    server_port = 7860
)

# gr.ChatInterface (
#     fn = chat,
#     type = "messages"
# ).launch(
#     share = True,
# )

