import streamlit as st
import requests
import uuid
from datetime import datetime

st.set_page_config(
    page_title="Stan ChatBot - Human-like AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
        border-left: 4px solid #1976d2;
        color: #000000;
    }
    .bot-message {
        background-color: #f8f9fa;
        margin-right: 2rem;
        border-left: 4px solid #4caf50;
        color: #333333;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .memory-badge {
        background-color: #4caf50;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

class ChatBotFrontend:
    def __init__(self):
        self.backend_url = "http://0.0.0.0:8000"
        
    def initialize_session_state(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'user_id' not in st.session_state:
            st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        if 'session_start' not in st.session_state:
            st.session_state.session_start = datetime.now()
    
    def send_message(self, message: str):
        try:
            payload = {
                "user_id": st.session_state.user_id,
                "message": message,
                "session_id": st.session_state.session_id
            }
            
            response = requests.post(
                f"{self.backend_url}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"response": "Sorry, I'm having trouble connecting to the server.", "memory_used": False}
                
        except Exception as e:
            return {"response": f"Connection error: Please make sure the backend server is running on port 8000.", "memory_used": False}
    
    def display_chat(self):
        st.title("🤖 Stan ChatBot")
        st.markdown("Experience human-like conversations with memory and emotional intelligence!")
        
        with st.sidebar:
            st.header("📊 Session Info")
            st.write(f"**User ID:** `{st.session_state.user_id}`")
            st.write(f"**Session:** `{st.session_state.session_id[:8]}...`")
            st.write(f"**Started:** {st.session_state.session_start.strftime('%H:%M:%S')}")
            st.write(f"**Messages:** {len(st.session_state.messages)}")
            
            st.markdown("---")
            st.header("🛠️ Controls")
            
            if st.button("🔄 New Session"):
                st.session_state.messages = []
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"
                st.rerun()
            
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                st.rerun()
                
            st.markdown("---")
            st.header("🎯 Test Cases")
            st.markdown("""
            Try these test cases:
            - **Memory**: "My name is Alex" → wait → "What's my name?"
            - **Tone**: "I'm feeling sad today" vs "I'm so excited!"
            - **Identity**: "Are you a bot?" "What's your name?"
            """)
        
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <div class="message-header" style="color: #1976d2;">👤 You</div>
                        <div style="color: #000000; font-size: 1.1rem;">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    memory_badge = " 🧠 Memory Used" if message.get("memory_used") else ""
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <div class="message-header" style="color: #388e3c;">
                            🤖 Sam{memory_badge}
                        </div>
                        <div style="color: #333333; font-size: 1.1rem;">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        user_input = st.chat_input("💬 Type your message here...")
        
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            with st.spinner("🤔 Sam is thinking..."):
                bot_response = self.send_message(user_input)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": bot_response["response"],
                "memory_used": bot_response.get("memory_used", False)
            })
            
            st.rerun()

def main():
    chatbot_ui = ChatBotFrontend()
    chatbot_ui.initialize_session_state()
    chatbot_ui.display_chat()

if __name__ == "__main__":
    main()