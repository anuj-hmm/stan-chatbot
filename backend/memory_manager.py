import pymongo
import chromadb
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import os

class MemoryManager:
    def __init__(self):
        try:
            # MongoDB connection
            self.mongo_client = pymongo.MongoClient(
                os.getenv("MONGODB_URI", "mongodb://localhost:27017/chatbot_db"),
                serverSelectionTimeoutMS=5000
            )
            
            # Test connection immediately
            self.mongo_client.admin.command('ping')
            print("✅ MongoDB Connected Successfully!")
            
            self.db = self.mongo_client["chatbot_db"]
            self.users = self.db.users
            self.conversations = self.db.conversations
            
            # ChromaDB for semantic memory
            self.chroma_client = chromadb.Client()
            try:
                self.memory_collection = self.chroma_client.get_collection("conversation_memory")
            except:
                self.memory_collection = self.chroma_client.create_collection("conversation_memory")
                
            print("✅ Memory Manager Initialized Successfully!")
            
        except Exception as e:
            print(f"❌ Memory Manager Initialization Failed: {e}")
            raise
    
    def get_user_profile(self, user_id: str) -> Dict:
        try:
            user = self.users.find_one({"user_id": user_id})
            if not user:
                user_profile = {
                    "user_id": user_id,
                    "preferences": {},
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                self.users.insert_one(user_profile)
                return user_profile
            return user
        except Exception as e:
            print(f"❌ Error getting user profile: {e}")
            return {"user_id": user_id, "preferences": {}}
    
    def update_user_profile(self, user_id: str, updates: Dict):
        """Update user profile with new facts - FIXED METHOD"""
        try:
            updates["updated_at"] = datetime.now()
            self.users.update_one(
                {"user_id": user_id},
                {"$set": updates},
                upsert=True  # Fixed: upsert is a parameter, not part of the update
            )
            print(f"💾 Updated profile for user {user_id}: {updates}")
        except Exception as e:
            print(f"❌ Error updating user profile: {e}")
    
    def store_conversation(self, user_id: str, message: str, response: str):
        """Store conversation in both MongoDB and ChromaDB"""
        try:
            # Store in MongoDB
            conv_data = {
                "user_id": user_id,
                "message": message,
                "response": response,
                "timestamp": datetime.now()
            }
            self.conversations.insert_one(conv_data)
            
            # Store in ChromaDB for semantic search
            conversation_text = f"User: {message} Assistant: {response}"
            self.memory_collection.add(
                documents=[conversation_text],
                metadatas=[{"user_id": user_id, "type": "conversation"}],
                ids=[str(uuid.uuid4())]
            )
            print(f"💾 Stored conversation for user {user_id}")
        except Exception as e:
            print(f"❌ Error storing conversation: {e}")
    
    def get_relevant_memories(self, user_id: str, current_message: str, n_results: int = 3) -> List[str]:
        """Get relevant past conversations using semantic search"""
        try:
            results = self.memory_collection.query(
                query_texts=[current_message],
                n_results=n_results,
                where={"user_id": user_id}
            )
            memories = results['documents'][0] if results['documents'] else []
            print(f"🧠 Found {len(memories)} relevant memories for user {user_id}")
            return memories
        except Exception as e:
            print(f"❌ Error getting relevant memories: {e}")
            return []

# Test the memory manager
if __name__ == "__main__":
    mm = MemoryManager()
    print("Memory manager test completed successfully!")