"""Storage management for recordings and data"""

import logging
import cv2
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class StorageManager:
    """Manages storage of recordings and cleanup"""
    
    def __init__(self, config, db_manager):
        """Initialize storage manager
        
        Args:
            config: Application configuration
            db_manager: Database manager instance
        """
        self.config = config
        self.db_manager = db_manager
        self.recordings_dir = config.recordings_dir
        
    def save_recording_chunk(self, frames, start_time, end_time, fps):
        """Save a chunk of frames as a video file
        
        Args:
            frames: List of frame arrays
            start_time: Start datetime
            end_time: End datetime
            fps: Frames per second
            
        Returns:
            Path to saved video file
        """
        if not frames:
            return None
        
        # Create filename with timestamp
        timestamp = start_time.strftime('%Y%m%d_%H%M%S')
        date_dir = self.recordings_dir / start_time.strftime('%Y%m%d')
        date_dir.mkdir(exist_ok=True)
        
        video_path = date_dir / f"recording_{timestamp}.mp4"
        
        # Get frame dimensions
        height, width = frames[0].shape[:2]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(video_path), fourcc, fps, (width, height))
        
        # Write frames
        for frame in frames:
            out.write(frame)
        
        out.release()
        
        # Save to database
        session = self.db_manager.get_session()
        try:
            from pydayflow.models.database import Recording
            
            recording = Recording(
                start_time=start_time,
                end_time=end_time,
                file_path=str(video_path),
                duration=(end_time - start_time).total_seconds(),
                analyzed=False
            )
            session.add(recording)
            session.commit()
            
        except Exception as e:
            logger.error(f"Error saving recording to database: {e}", exc_info=True)
            session.rollback()
        finally:
            session.close()
        
        return video_path
    
    def cleanup_old_recordings(self):
        """Remove recordings older than retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)
            
            session = self.db_manager.get_session()
            try:
                from pydayflow.models.database import Recording
                
                # Get old recordings
                old_recordings = session.query(Recording).filter(
                    Recording.start_time < cutoff_date
                ).all()
                
                deleted_count = 0
                for recording in old_recordings:
                    # Delete file
                    try:
                        file_path = Path(recording.file_path)
                        if file_path.exists():
                            file_path.unlink()
                            logger.info(f"Deleted old recording: {file_path}")
                        
                        # Delete from database
                        session.delete(recording)
                        deleted_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error deleting recording {recording.file_path}: {e}")
                
                session.commit()
                logger.info(f"Cleaned up {deleted_count} old recordings")
                
                # Also delete empty date directories
                self._cleanup_empty_dirs()
                
            except Exception as e:
                logger.error(f"Error during cleanup: {e}", exc_info=True)
                session.rollback()
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Error in cleanup_old_recordings: {e}", exc_info=True)
    
    def _cleanup_empty_dirs(self):
        """Remove empty date directories"""
        try:
            for date_dir in self.recordings_dir.iterdir():
                if date_dir.is_dir() and not any(date_dir.iterdir()):
                    date_dir.rmdir()
                    logger.info(f"Removed empty directory: {date_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up empty directories: {e}")
    
    def get_storage_stats(self):
        """Get storage statistics"""
        try:
            total_size = 0
            file_count = 0
            
            for file_path in self.recordings_dir.rglob('*.mp4'):
                total_size += file_path.stat().st_size
                file_count += 1
            
            return {
                'total_size_mb': total_size / (1024 * 1024),
                'file_count': file_count,
                'recordings_dir': str(self.recordings_dir)
            }
        except Exception as e:
            logger.error(f"Error getting storage stats: {e}")
            return None
