"""Analysis manager for processing recordings"""

import logging
from datetime import datetime, timedelta
from threading import Thread, Event
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


class AnalysisManager:
    """Manages periodic analysis of recordings"""
    
    def __init__(self, config, db_manager, ai_service):
        """Initialize analysis manager
        
        Args:
            config: Application configuration
            db_manager: Database manager instance
            ai_service: AI service instance
        """
        self.config = config
        self.db_manager = db_manager
        self.ai_service = ai_service
        self.scheduler = BackgroundScheduler()
        self.is_running = False
    
    def start(self):
        """Start periodic analysis"""
        if self.is_running:
            logger.warning("Analysis manager already running")
            return
        
        logger.info(f"Starting analysis manager (interval: {self.config.analysis_interval}s)")
        
        # Schedule periodic analysis
        self.scheduler.add_job(
            self.analyze_pending_recordings,
            'interval',
            seconds=self.config.analysis_interval,
            id='analyze_recordings'
        )
        
        self.scheduler.start()
        self.is_running = True
    
    def stop(self):
        """Stop periodic analysis"""
        if not self.is_running:
            return
        
        logger.info("Stopping analysis manager")
        self.scheduler.shutdown()
        self.is_running = False
    
    def analyze_pending_recordings(self):
        """Analyze all unanalyzed recordings"""
        try:
            session = self.db_manager.get_session()
            try:
                from pydayflow.models.database import Recording, TimelineCard
                
                # Get unanalyzed recordings
                recordings = session.query(Recording).filter(
                    Recording.analyzed == False
                ).order_by(Recording.start_time).all()
                
                if not recordings:
                    logger.debug("No pending recordings to analyze")
                    return
                
                logger.info(f"Analyzing {len(recordings)} pending recordings...")
                
                # Group recordings into batches (15-minute intervals)
                batches = self._group_recordings_into_batches(recordings)
                
                for batch_recordings in batches:
                    self._analyze_batch(batch_recordings, session)
                
                session.commit()
                logger.info("Analysis complete")
                
            except Exception as e:
                logger.error(f"Error analyzing recordings: {e}", exc_info=True)
                session.rollback()
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Error in analyze_pending_recordings: {e}", exc_info=True)
    
    def _group_recordings_into_batches(self, recordings):
        """Group recordings into 15-minute batches"""
        if not recordings:
            return []
        
        batches = []
        current_batch = [recordings[0]]
        batch_start = recordings[0].start_time
        
        for recording in recordings[1:]:
            # If recording is within 15 minutes of batch start, add to current batch
            if (recording.start_time - batch_start).total_seconds() < 900:  # 15 minutes
                current_batch.append(recording)
            else:
                # Start new batch
                batches.append(current_batch)
                current_batch = [recording]
                batch_start = recording.start_time
        
        # Add last batch
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def _analyze_batch(self, recordings, session):
        """Analyze a batch of recordings and create timeline card"""
        from pydayflow.models.database import TimelineCard
        
        if not recordings:
            return
        
        try:
            # For simplicity, analyze the first recording in the batch
            # In a full implementation, we might combine multiple recordings
            recording = recordings[0]
            
            # Analyze with AI
            analysis = self.ai_service.analyze_video_chunk(
                recording.file_path,
                recording.start_time,
                recording.end_time
            )
            
            if analysis:
                # Create timeline card
                card = TimelineCard(
                    start_time=recording.start_time,
                    end_time=recordings[-1].end_time,  # Use end of last recording in batch
                    title=analysis['title'],
                    summary=analysis['summary'],
                    category=analysis['category'],
                    confidence=analysis['confidence']
                )
                session.add(card)
                
                # Mark recordings as analyzed
                for rec in recordings:
                    rec.analyzed = True
                
                logger.info(f"Created timeline card: {analysis['title']}")
            
        except Exception as e:
            logger.error(f"Error analyzing batch: {e}", exc_info=True)
    
    def get_timeline(self, start_date=None, end_date=None):
        """Get timeline cards for a date range
        
        Args:
            start_date: Start date (default: today)
            end_date: End date (default: today)
            
        Returns:
            List of timeline card dictionaries
        """
        try:
            if start_date is None:
                start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if end_date is None:
                end_date = start_date.replace(hour=23, minute=59, second=59)
            
            session = self.db_manager.get_session()
            try:
                from pydayflow.models.database import TimelineCard
                
                cards = session.query(TimelineCard).filter(
                    TimelineCard.start_time >= start_date,
                    TimelineCard.start_time <= end_date
                ).order_by(TimelineCard.start_time).all()
                
                result = []
                for card in cards:
                    result.append({
                        'id': card.id,
                        'start_time': card.start_time.isoformat(),
                        'end_time': card.end_time.isoformat(),
                        'title': card.title,
                        'summary': card.summary,
                        'category': card.category,
                        'confidence': card.confidence
                    })
                
                return result
                
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Error getting timeline: {e}", exc_info=True)
            return []
