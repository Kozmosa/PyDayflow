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


def print_banner():
    """Print startup banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    ██████╗ ██╗   ██╗██████╗  █████╗ ██╗   ██╗            ║
║    ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗╚██╗ ██╔╝            ║
║    ██████╔╝ ╚████╔╝ ██║  ██║███████║ ╚████╔╝             ║
║    ██╔═══╝   ╚██╔╝  ██║  ██║██╔══██║  ╚██╔╝              ║
║    ██║        ██║   ██████╔╝██║  ██║   ██║               ║
║    ╚═╝        ╚═╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝               ║
║           ███████╗██╗      ██████╗ ██╗    ██╗            ║
║           ██╔════╝██║     ██╔═══██╗██║    ██║            ║
║           █████╗  ██║     ██║   ██║██║ █╗ ██║            ║
║           ██╔══╝  ██║     ██║   ██║██║███╗██║            ║
║           ██║     ███████╗╚██████╔╝╚███╔███╔╝            ║
║           ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝             ║
║                                                           ║
║              自动记录屏幕活动并生成时间线                   ║
║              Windows版本 - v1.0.0                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point for PyDayflow"""
    try:
        print_banner()
        logger.info("Starting PyDayflow...")
        
        # Load configuration
        config = Config()
        
        # Create Flask app
        app = create_app(config)
        
        # Print helpful information
        print("\n✨ PyDayflow 已启动！")
        print(f"\n🌐 Web界面: http://localhost:{config.web_port}")
        print(f"📁 数据目录: {config.data_dir}")
        print(f"🤖 AI提供商: {config.ai_provider}")
        print(f"📹 录制帧率: {config.capture_fps} FPS")
        print(f"⏰ 分析间隔: {config.analysis_interval} 秒")
        print(f"🗑️  保留天数: {config.retention_days} 天")
        print("\n💡 提示:")
        print("  - 打开浏览器访问上面的Web界面地址")
        print("  - 点击'开始录制'按钮开始追踪您的活动")
        print("  - 按 Ctrl+C 停止应用")
        print("\n" + "=" * 60 + "\n")
        
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
