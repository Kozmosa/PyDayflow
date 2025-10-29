"""
PyDayflow - Windows版本的Dayflow，使用Python和Web UI
自动记录屏幕活动并通过AI生成时间线摘要
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from pydayflow.web.app import create_app
from pydayflow.core.recording.screen_recorder import ScreenRecorder
from pydayflow.core.analysis.analysis_manager import AnalysisManager
from pydayflow.core.storage.storage_manager import StorageManager
from pydayflow.utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pydayflow.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for PyDayflow"""
    try:
        logger.info("Starting PyDayflow...")
        
        # Load configuration
        config = Config()
        
        # Create Flask app
        app = create_app(config)
        
        # Start web server
        logger.info(f"Starting web server on http://localhost:{config.web_port}")
        app.run(
            host='0.0.0.0',
            port=config.web_port,
            debug=config.debug,
            threaded=True
        )
        
    except Exception as e:
        logger.error(f"Error starting PyDayflow: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
