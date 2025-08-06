#!/usr/bin/env python3
"""
History Manager for TTS Audio Files
Manages audio file storage, history tracking, and automatic cleanup
"""

import os
import json
import time
import uuid
import shutil
import logging
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class HistoryManager:
    def __init__(self, storage_dir="audio_history", max_files=100, auto_cleanup_days=7):
        self.storage_dir = storage_dir
        self.max_files = max_files
        self.auto_cleanup_days = auto_cleanup_days
        self.history_file = os.path.join(storage_dir, "history.json")
        
        # Create storage directory
        os.makedirs(storage_dir, exist_ok=True)
        
        # Load existing history
        self.history = self._load_history()
        
        # Start cleanup timer
        self._start_cleanup_timer()
    
    def _load_history(self) -> List[Dict]:
        """Load history from JSON file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load history: {e}")
        return []
    
    def _save_history(self):
        """Save history to JSON file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def add_audio(self, text: str, voice: str, model_type: str, audio_data: bytes) -> Dict:
        """Add new audio to history"""
        # Generate unique ID
        audio_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Create filename
        filename = f"{audio_id}.wav"
        filepath = os.path.join(self.storage_dir, filename)
        
        # Save audio file
        try:
            with open(filepath, 'wb') as f:
                f.write(audio_data)
        except Exception as e:
            logger.error(f"Failed to save audio file: {e}")
            return None
        
        # Create history entry
        entry = {
            "id": audio_id,
            "text": text[:200],  # Truncate long text
            "full_text": text,
            "voice": voice,
            "model_type": model_type,
            "filename": filename,
            "filepath": filepath,
            "timestamp": timestamp,
            "size": len(audio_data)
        }
        
        # Add to history (newest first)
        self.history.insert(0, entry)
        
        # Limit history size
        if len(self.history) > self.max_files:
            # Remove oldest entries
            for old_entry in self.history[self.max_files:]:
                self._delete_audio_file(old_entry)
            self.history = self.history[:self.max_files]
        
        # Save history
        self._save_history()
        
        logger.info(f"Added audio to history: {audio_id}")
        return entry
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get history entries"""
        if limit:
            return self.history[:limit]
        return self.history
    
    def get_audio_file(self, audio_id: str) -> Optional[str]:
        """Get audio file path by ID"""
        for entry in self.history:
            if entry["id"] == audio_id:
                filepath = entry["filepath"]
                if os.path.exists(filepath):
                    return filepath
                else:
                    # File missing, remove from history
                    self.history.remove(entry)
                    self._save_history()
                    break
        return None
    
    def delete_audio(self, audio_id: str) -> bool:
        """Delete specific audio by ID"""
        for i, entry in enumerate(self.history):
            if entry["id"] == audio_id:
                # Delete file
                self._delete_audio_file(entry)
                # Remove from history
                self.history.pop(i)
                self._save_history()
                logger.info(f"Deleted audio: {audio_id}")
                return True
        return False
    
    def clear_all(self) -> int:
        """Clear all audio files"""
        count = 0
        for entry in self.history:
            if self._delete_audio_file(entry):
                count += 1
        
        self.history.clear()
        self._save_history()
        
        logger.info(f"Cleared {count} audio files")
        return count
    
    def _delete_audio_file(self, entry: Dict) -> bool:
        """Delete audio file from disk"""
        try:
            if os.path.exists(entry["filepath"]):
                os.remove(entry["filepath"])
                return True
        except Exception as e:
            logger.error(f"Failed to delete file {entry['filepath']}: {e}")
        return False
    
    def cleanup_old_files(self) -> int:
        """Clean up files older than auto_cleanup_days"""
        if self.auto_cleanup_days <= 0:
            return 0
        
        cutoff_date = datetime.now() - timedelta(days=self.auto_cleanup_days)
        removed_count = 0
        
        # Filter out old entries
        new_history = []
        for entry in self.history:
            try:
                entry_date = datetime.fromisoformat(entry["timestamp"])
                if entry_date < cutoff_date:
                    # Delete old file
                    if self._delete_audio_file(entry):
                        removed_count += 1
                else:
                    new_history.append(entry)
            except Exception as e:
                logger.error(f"Error processing entry: {e}")
                new_history.append(entry)  # Keep entry if date parsing fails
        
        if removed_count > 0:
            self.history = new_history
            self._save_history()
            logger.info(f"Cleaned up {removed_count} old audio files")
        
        return removed_count
    
    def _start_cleanup_timer(self):
        """Start automatic cleanup timer"""
        if self.auto_cleanup_days > 0:
            # Run cleanup every 24 hours
            def cleanup_task():
                while True:
                    time.sleep(24 * 60 * 60)  # 24 hours
                    try:
                        self.cleanup_old_files()
                    except Exception as e:
                        logger.error(f"Cleanup task error: {e}")
            
            cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
            cleanup_thread.start()
            logger.info(f"Started automatic cleanup (every 24h, keep {self.auto_cleanup_days} days)")
    
    def get_stats(self) -> Dict:
        """Get storage statistics"""
        total_size = 0
        total_files = len(self.history)
        
        for entry in self.history:
            total_size += entry.get("size", 0)
        
        return {
            "total_files": total_files,
            "total_size": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "storage_dir": self.storage_dir,
            "auto_cleanup_days": self.auto_cleanup_days
        }

# Global instance
history_manager = None

def get_history_manager():
    """Get global history manager instance"""
    global history_manager
    if history_manager is None:
        history_manager = HistoryManager()
    return history_manager
