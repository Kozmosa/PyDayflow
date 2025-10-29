"""Configuration management for PyDayflow"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    def __init__(self):
        # Application settings
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        self.web_port = int(os.getenv('WEB_PORT', '5000'))
        
        # Storage settings
        self.data_dir = Path(os.getenv('DATA_DIR', 
                                       os.path.join(os.path.expanduser('~'), 'PyDayflow')))
        self.recordings_dir = self.data_dir / 'recordings'
        self.database_path = self.data_dir / 'pydayflow.db'
        
        # Recording settings
        self.capture_fps = float(os.getenv('CAPTURE_FPS', '1.0'))  # 1 FPS like original
        self.analysis_interval = int(os.getenv('ANALYSIS_INTERVAL', '900'))  # 15 minutes in seconds
        self.retention_days = int(os.getenv('RETENTION_DAYS', '3'))  # Keep recordings for 3 days
        
        # AI settings
        self.ai_provider = os.getenv('AI_PROVIDER', 'gemini')  # 'gemini' or 'local'
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', '')
        self.local_llm_url = os.getenv('LOCAL_LLM_URL', 'http://localhost:11434')  # Ollama default
        self.gemini_model = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        
        # Create directories if they don't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.recordings_dir.mkdir(parents=True, exist_ok=True)
    
    def validate(self):
        """Validate configuration"""
        if self.ai_provider == 'gemini' and not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when using Gemini provider")
        
        return True
