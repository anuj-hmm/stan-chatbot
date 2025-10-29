import google.generativeai as genai
import os
from typing import Dict, List

class ChatBot:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def build_prompt(self, user_context: Dict, relevant_memories: List[str], current_message: str) -> str:
        # User facts
        profile = user_context.get("profile", {})
        facts_section = ""
        if profile.get("name"):
            facts_section += f"- User's name: {profile['name']}\n"
        for key, value in profile.get("preferences", {}).items():
            facts_section += f"- User's {key}: {value}\n"
        
        # Relevant memories
        memories_section = "\n".join([f"- {memory}" for memory in relevant_memories]) if relevant_memories else "No relevant past conversations."
        
        prompt = f"""
You are "Sam", a friendly and empathetic AI assistant. Be conversational and human-like.

User Facts:
{facts_section if facts_section else "No user facts recorded yet."}

Relevant Past Conversations:
{memories_section}

Current User Message: "{current_message}"

Instructions:
- Respond naturally as Sam
- Be empathetic and engaging
- Reference past conversations when relevant
- Keep responses concise but meaningful

Response:
"""
        return prompt
    
    def generate_response(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"I apologize, but I'm having trouble responding right now. Error: {str(e)}"