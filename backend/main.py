from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Stan ChatBot API", version="1.0.0")

# CORS middleware - FIXED for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
try:
    from memory_manager import MemoryManager
    from chatbot import ChatBot
    from models import ChatRequest, ChatResponse
    
    memory_manager = MemoryManager()
    chatbot = ChatBot()
    logger.info("✅ All components initialized successfully!")
    
except Exception as e:
    logger.error(f"❌ Component initialization failed: {e}")
    raise

@app.get("/")
async def root():
    return {"message": "Stan ChatBot API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chatbot-api"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"📨 Received message from user {request.user_id}: {request.message}")
        
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Extract simple facts from message
        message_lower = request.message.lower()
        if "my name is" in message_lower:
            name = request.message.split("my name is")[-1].strip()
            if len(name) < 50:
                memory_manager.update_user_profile(request.user_id, {"name": name.split(".")[0]})
                logger.info(f"💾 Saved user name: {name}")
        
        # Get user context and relevant memories
        user_profile = memory_manager.get_user_profile(request.user_id)
        relevant_memories = memory_manager.get_relevant_memories(request.user_id, request.message)
        
        logger.info(f"🧠 User profile: {user_profile.get('name', 'No name')}")
        logger.info(f"📚 Relevant memories found: {len(relevant_memories)}")
        
        # Build prompt and generate response
        user_context = {"profile": user_profile}
        prompt = chatbot.build_prompt(user_context, relevant_memories, request.message)
        response_text = chatbot.generate_response(prompt)
        
        # Store conversation
        memory_manager.store_conversation(request.user_id, request.message, response_text)
        
        memory_used = len(relevant_memories) > 0 or bool(user_profile.get("name"))
        
        logger.info(f"📤 Sending response: {response_text[:50]}...")
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            memory_used=memory_used
        )
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Stan ChatBot API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")