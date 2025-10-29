"""Flask web application for PyDayflow"""

import logging
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta

from pydayflow.models.database import DatabaseManager
from pydayflow.core.recording.screen_recorder import ScreenRecorder
from pydayflow.core.storage.storage_manager import StorageManager
from pydayflow.core.ai.ai_service import AIService
from pydayflow.core.analysis.analysis_manager import AnalysisManager

logger = logging.getLogger(__name__)


# Global instances
recorder = None
storage_manager = None
analysis_manager = None


def create_app(config):
    """Create and configure Flask app"""
    app = Flask(__name__)
    CORS(app)
    
    # Initialize components
    global recorder, storage_manager, analysis_manager
    
    # Initialize database
    db_manager = DatabaseManager(config.database_path)
    
    # Initialize storage manager
    storage_manager = StorageManager(config, db_manager)
    
    # Initialize AI service
    ai_service = AIService(config)
    
    # Initialize analysis manager
    analysis_manager = AnalysisManager(config, db_manager, ai_service)
    analysis_manager.start()
    
    # Initialize screen recorder
    recorder = ScreenRecorder(config, storage_manager)
    
    # Routes
    @app.route('/')
    def index():
        """Main page"""
        return render_template('index.html')
    
    @app.route('/api/status')
    def get_status():
        """Get application status"""
        return jsonify({
            'recording': recorder.get_status(),
            'storage': storage_manager.get_storage_stats(),
            'analysis_running': analysis_manager.is_running
        })
    
    @app.route('/api/recording/start', methods=['POST'])
    def start_recording():
        """Start screen recording"""
        success = recorder.start_recording()
        return jsonify({'success': success})
    
    @app.route('/api/recording/stop', methods=['POST'])
    def stop_recording():
        """Stop screen recording"""
        success = recorder.stop_recording()
        return jsonify({'success': success})
    
    @app.route('/api/timeline')
    def get_timeline():
        """Get timeline for a date"""
        # Get date from query params (default to today)
        date_str = request.args.get('date')
        
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        else:
            date = datetime.now()
        
        # Get timeline cards for the date
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = date.replace(hour=23, minute=59, second=59)
        
        cards = analysis_manager.get_timeline(start_date, end_date)
        
        return jsonify({
            'date': date.strftime('%Y-%m-%d'),
            'cards': cards
        })
    
    @app.route('/api/cleanup', methods=['POST'])
    def cleanup_storage():
        """Trigger storage cleanup"""
        try:
            storage_manager.cleanup_old_recordings()
            return jsonify({'success': True})
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/analyze', methods=['POST'])
    def trigger_analysis():
        """Manually trigger analysis"""
        try:
            analysis_manager.analyze_pending_recordings()
            return jsonify({'success': True})
        except Exception as e:
            logger.error(f"Error in analysis: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return app
