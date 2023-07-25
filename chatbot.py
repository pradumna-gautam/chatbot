from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Set your OpenAI GPT-3.5 API key
openai.api_key = "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"

# Initialize the chat history queue
chat_history = []

# FastAPI app
app = FastAPI()

# Chat message schema
class ChatMessage(BaseModel):
    role: str
    content: str

# API endpoint for chatting
@app.post("/chat/")
async def chat(message: List[ChatMessage]):
    if not message:
        raise HTTPException(status_code=400, detail="Empty conversation")

    # Retrieve user messages from the request
    user_messages = [msg.content for msg in message if msg.role == "user"]

    # Append user messages to chat history
    chat_history.extend(user_messages)

    # Prepare the conversation prompt
    conversation = "\n".join(chat_history)

    try:
        # Generate response using GPT-3.5
        response = openai.Completion.create(
            model="text-davinci-003",  # GPT-3.5 model
            prompt=conversation,
            max_tokens=150,  # Limit the response length
            temperature=0.7,  # Adjust the randomness of the response
            stop=["\n"],  # Stop generating after a complete message
        )

        # Retrieve and append the chatbot response
        chat_history.append(response.choices[0].text.strip())

        # Return the chatbot response to the user
        return {"response": response.choices[0].text.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
