"""Screen recording module for Windows using mss"""

import time
import logging
from datetime import datetime
from pathlib import Path
from threading import Thread, Event
import cv2
import numpy as np
from mss import mss

logger = logging.getLogger(__name__)


class ScreenRecorder:
    """Screen recorder that captures at 1 FPS"""
    
    def __init__(self, config, storage_manager):
        """Initialize screen recorder
        
        Args:
            config: Application configuration
            storage_manager: Storage manager instance
        """
        self.config = config
        self.storage_manager = storage_manager
        self.is_recording = False
        self.recording_thread = None
        self.stop_event = Event()
        self.fps = config.capture_fps
        self.current_chunk_frames = []
        self.chunk_start_time = None
        self.chunk_duration = 15  # Save video chunks every 15 seconds
        
    def start_recording(self):
        """Start screen recording"""
        if self.is_recording:
            logger.warning("Recording already in progress")
            return False
        
        logger.info("Starting screen recording...")
        self.is_recording = True
        self.stop_event.clear()
        self.recording_thread = Thread(target=self._record_loop, daemon=True)
        self.recording_thread.start()
        return True
    
    def stop_recording(self):
        """Stop screen recording"""
        if not self.is_recording:
            logger.warning("No recording in progress")
            return False
        
        logger.info("Stopping screen recording...")
        self.is_recording = False
        self.stop_event.set()
        
        if self.recording_thread:
            self.recording_thread.join(timeout=5)
        
        # Save any remaining frames
        if self.current_chunk_frames:
            self._save_chunk()
        
        return True
    
    def _record_loop(self):
        """Main recording loop"""
        with mss() as sct:
            # Get the primary monitor
            monitor = sct.monitors[1]
            
            frame_interval = 1.0 / self.fps
            self.chunk_start_time = datetime.now()
            
            while not self.stop_event.is_set():
                try:
                    start_time = time.time()
                    
                    # Capture screenshot
                    screenshot = sct.grab(monitor)
                    
                    # Convert to numpy array
                    frame = np.array(screenshot)
                    
                    # Convert BGRA to BGR (remove alpha channel)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    
                    # Add frame to current chunk
                    self.current_chunk_frames.append(frame)
                    
                    # Check if we should save the chunk
                    elapsed = (datetime.now() - self.chunk_start_time).total_seconds()
                    if elapsed >= self.chunk_duration:
                        self._save_chunk()
                        self.current_chunk_frames = []
                        self.chunk_start_time = datetime.now()
                    
                    # Sleep to maintain FPS
                    elapsed_time = time.time() - start_time
                    sleep_time = max(0, frame_interval - elapsed_time)
                    time.sleep(sleep_time)
                    
                except Exception as e:
                    logger.error(f"Error capturing frame: {e}", exc_info=True)
    
    def _save_chunk(self):
        """Save current chunk of frames as video"""
        if not self.current_chunk_frames:
            return
        
        try:
            end_time = datetime.now()
            duration = len(self.current_chunk_frames) / self.fps
            
            # Save video using storage manager
            video_path = self.storage_manager.save_recording_chunk(
                self.current_chunk_frames,
                self.chunk_start_time,
                end_time,
                self.fps
            )
            
            logger.info(f"Saved recording chunk: {video_path} ({len(self.current_chunk_frames)} frames)")
            
        except Exception as e:
            logger.error(f"Error saving chunk: {e}", exc_info=True)
    
    def get_status(self):
        """Get recording status"""
        return {
            'is_recording': self.is_recording,
            'fps': self.fps,
            'chunk_duration': self.chunk_duration
        }
