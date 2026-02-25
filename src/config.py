import os
from typing import Optional

class Config:
    """Configuration management for the application"""
    
    def __init__(self):
        self.api_key = self._load_api_key()
        self.api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    
    def _load_api_key(self) -> str:
        """Load API key from environment variable"""
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        if not api_key:
            raise ValueError(
                "❌ API key not found!\n\n"
                "Please set HUGGINGFACE_API_KEY in your .env file.\n\n"
                "Steps to get your API key:\n"
                "1. Go to https://huggingface.co/settings/tokens\n"
                "2. Click 'New token'\n"
                "3. Give it a name and select 'Read' permission\n"
                "4. Copy the token (starts with 'hf_')\n"
                "5. Add it to your .env file: HUGGINGFACE_API_KEY=your_token_here"
            )
        
        if not api_key.startswith("hf_"):
            raise ValueError(
                "❌ Invalid API key format!\n\n"
                "Hugging Face tokens should start with 'hf_'\n"
                "Please check your .env file and make sure you copied the complete token."
            )
        
        return api_key
