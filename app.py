# app.py
import os
import google.generativeai as genai
import gradio as gr

# --------------------------
# Configure Gemini API Key
# --------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --------------------------
# Gemini Response Generator
# --------------------------
def get_gemini_response(user_message, therapy_type=None):
    """
    Generate response using Gemini AI.
    Fully AI-based; does NOT rely on any knowledge base.
    """
    system_prompt = """
You are an empathetic Ayurvedic assistant specializing in Panchakarma.
Answer the user's questions fully, clearly, and accurately.
- Use bullet points where appropriate.
- Focus on the therapy type if provided.
- End with: "This is general guidance based on traditional Ayurveda—consult your qualified practitioner for personalized advice."
"""
    if therapy_type:
        system_prompt += f"\n\nFocus on therapy type: {therapy_type}"

    prompt = f"{system_prompt}\n\nUser question: {user_message}"

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content([{"role": "user", "parts": prompt}])
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}. Check your Gemini API key and internet connection."

# --------------------------
# Gradio Chatbot Interface
# --------------------------
# Store chat history in-memory
chat_history = []

def chatbot_interface(user_message, therapy_type=""):
    global chat_history
    response = get_gemini_response(user_message, therapy_type or None)
    chat_history.append(("You", user_message))
    chat_history.append(("Bot", response))

    # Build formatted chat history for display
    formatted_history = ""
    for speaker, message in chat_history:
        formatted_history += f"**{speaker}:** {message}\n\n"
    return formatted_history

# Create Gradio interface
iface = gr.Interface(
    fn=chatbot_interface,
    inputs=[
        gr.Textbox(lines=2, placeholder="Ask your question here...", label="Your Question"),
        gr.Textbox(lines=1, placeholder="Optional: Therapy Type", label="Therapy Type")
    ],
    outputs=gr.Markdown(),
    title="🧘 Panchakarma Chatbot",
    description="Ask any question about Panchakarma or Ayurvedic practices. Powered by **Google Gemini AI**.",
    allow_flagging="never"
)

# Launch app
if __name__ == "__main__":
    iface.launch()
