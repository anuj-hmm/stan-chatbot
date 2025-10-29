# Stan ChatBot - Human-like Conversational AI

A sophisticated chatbot with long-term memory and emotional intelligence, built for the STAN Internship Challenge.

## 🚀 Features

- 🧠 **Long-term Memory**: Remembers user preferences and past conversations
- 😊 **Emotional Intelligence**: Adapts tone based on user's mood
- 🔄 **Context Awareness**: Maintains conversation context across sessions
- 🎭 **Persona Consistency**: Stays in character as "Sam"
- 💾 **Dual Memory**: MongoDB for facts + ChromaDB for conversations

## 🛠️ Tech Stack

- **Backend**: Python + FastAPI
- **AI**: Google Gemini API
- **Memory**: MongoDB + ChromaDB
- **Frontend**: Streamlit
- **Deployment Ready**: Modular and scalable architecture

## 📦 Installation

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables in .env
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# Run backend
uvicorn main:app --reload --port 8000
```
