"""Manage generation history"""
import json
import os
from datetime import datetime
from typing import List, Dict

class HistoryManager:
    """Manage image generation history"""
    
    def __init__(self, history_file: str = "generation_history.json"):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Load history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Save history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_generation(self, prompt: str, settings: Dict, success: bool = True):
        """Add a generation to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "settings": settings,
            "success": success
        }
        self.history.append(entry)
        self._save_history()
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Get recent generations"""
        return self.history[-limit:][::-1]
    
    def get_stats(self) -> Dict:
        """Get generation statistics"""
        total = len(self.history)
        successful = sum(1 for h in self.history if h.get("success", False))
        
        return {
            "total_generations": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": (successful / total * 100) if total > 0 else 0
        }
    
    def clear_history(self):
        """Clear all history"""
        self.history = []
        self._save_history()
