"""AI service for analyzing recordings"""

import logging
import base64
import requests
from pathlib import Path
import google.generativeai as genai

logger = logging.getLogger(__name__)


class AIService:
    """AI service for analyzing screen recordings"""
    
    def __init__(self, config):
        """Initialize AI service
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.provider = config.ai_provider
        
        if self.provider == 'gemini':
            self._init_gemini()
        elif self.provider == 'local':
            self._init_local()
    
    def _init_gemini(self):
        """Initialize Gemini AI"""
        if not self.config.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini provider")
        
        genai.configure(api_key=self.config.gemini_api_key)
        self.model = genai.GenerativeModel(self.config.gemini_model)
        logger.info(f"Initialized Gemini AI with model: {self.config.gemini_model}")
    
    def _init_local(self):
        """Initialize local LLM (Ollama)"""
        self.local_url = self.config.local_llm_url
        logger.info(f"Initialized local LLM at: {self.local_url}")
    
    def analyze_video_chunk(self, video_path, start_time, end_time):
        """Analyze a video chunk and generate activity summary
        
        Args:
            video_path: Path to video file
            start_time: Start datetime
            end_time: End datetime
            
        Returns:
            Dictionary with analysis results
        """
        try:
            if self.provider == 'gemini':
                return self._analyze_with_gemini(video_path, start_time, end_time)
            elif self.provider == 'local':
                return self._analyze_with_local(video_path, start_time, end_time)
            else:
                raise ValueError(f"Unknown AI provider: {self.provider}")
                
        except Exception as e:
            logger.error(f"Error analyzing video: {e}", exc_info=True)
            return None
    
    def _analyze_with_gemini(self, video_path, start_time, end_time):
        """Analyze video with Gemini"""
        try:
            # Upload video file
            video_file = genai.upload_file(path=str(video_path))
            logger.info(f"Uploaded video to Gemini: {video_file.name}")
            
            # Create prompt
            prompt = f"""Analyze this screen recording from {start_time.strftime('%H:%M:%S')} to {end_time.strftime('%H:%M:%S')}.

Please provide:
1. A concise title (max 50 characters) describing the main activity
2. A brief summary (2-3 sentences) of what the user was doing
3. Category: 'work', 'personal', or 'distraction'
4. Confidence score (0.0 to 1.0)

Format your response as JSON:
{{
    "title": "Activity title",
    "summary": "Detailed summary of the activity",
    "category": "work/personal/distraction",
    "confidence": 0.95
}}"""
            
            # Generate content
            response = self.model.generate_content([video_file, prompt])
            
            # Parse response
            import json
            result_text = response.text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(result_text)
            logger.info(f"Gemini analysis complete: {result['title']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in Gemini analysis: {e}", exc_info=True)
            return {
                'title': 'Unknown Activity',
                'summary': 'Unable to analyze this recording.',
                'category': 'personal',
                'confidence': 0.0
            }
    
    def _analyze_with_local(self, video_path, start_time, end_time):
        """Analyze video with local LLM (simplified version)"""
        try:
            # For local LLM, we'll extract frames and analyze them
            # This is a simplified version - full implementation would need frame extraction
            import cv2
            
            # Extract a few frames
            cap = cv2.VideoCapture(str(video_path))
            frames = []
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Extract up to 5 frames evenly distributed
            indices = [int(i * frame_count / 5) for i in range(5)]
            
            for idx in indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    frames.append(frame)
            
            cap.release()
            
            # For now, return a placeholder result
            # Full implementation would send frames to local LLM
            logger.warning("Local LLM analysis not fully implemented, returning placeholder")
            
            return {
                'title': 'Screen Activity',
                'summary': f'Activity recorded from {start_time.strftime("%H:%M")} to {end_time.strftime("%H:%M")}',
                'category': 'personal',
                'confidence': 0.5
            }
            
        except Exception as e:
            logger.error(f"Error in local analysis: {e}", exc_info=True)
            return {
                'title': 'Unknown Activity',
                'summary': 'Unable to analyze this recording.',
                'category': 'personal',
                'confidence': 0.0
            }
