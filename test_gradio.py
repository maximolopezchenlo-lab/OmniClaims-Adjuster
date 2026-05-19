import gradio as gr
app = gr.Blocks()
with app:
    gr.Markdown("Hello")
try:
    app.launch(theme=gr.themes.Default(), css="body { background: red; }", prevent_thread_lock=True, server_port=7861)
except Exception as e:
    print(f"Error: {e}")
