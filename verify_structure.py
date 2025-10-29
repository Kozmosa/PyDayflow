"""
PyDayflow项目结构验证
验证所有必需的文件和目录是否存在
"""

import os
from pathlib import Path

def check_structure():
    """Check project structure"""
    print("检查PyDayflow项目结构...")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    
    # Required directories
    required_dirs = [
        "pydayflow",
        "pydayflow/core",
        "pydayflow/core/ai",
        "pydayflow/core/analysis",
        "pydayflow/core/recording",
        "pydayflow/core/storage",
        "pydayflow/models",
        "pydayflow/utils",
        "pydayflow/web",
        "pydayflow/web/static",
        "pydayflow/web/static/css",
        "pydayflow/web/static/js",
        "pydayflow/web/templates",
    ]
    
    # Required files
    required_files = [
        "main.py",
        "requirements.txt",
        ".env.example",
        "PYDAYFLOW_README.md",
        "start.bat",
        "start.sh",
        "pydayflow/__init__.py",
        "pydayflow/utils/config.py",
        "pydayflow/models/database.py",
        "pydayflow/core/ai/ai_service.py",
        "pydayflow/core/analysis/analysis_manager.py",
        "pydayflow/core/recording/screen_recorder.py",
        "pydayflow/core/storage/storage_manager.py",
        "pydayflow/web/app.py",
        "pydayflow/web/templates/index.html",
        "pydayflow/web/static/css/style.css",
        "pydayflow/web/static/js/app.js",
    ]
    
    all_good = True
    
    print("\n📁 检查目录:")
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists() and full_path.is_dir():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} - 缺失！")
            all_good = False
    
    print("\n📄 检查文件:")
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists() and full_path.is_file():
            size = full_path.stat().st_size
            print(f"  ✓ {file_path} ({size} bytes)")
        else:
            print(f"  ✗ {file_path} - 缺失！")
            all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("✓ 项目结构完整！")
        print("\n下一步:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 配置环境: 复制 .env.example 到 .env 并配置")
        print("3. 运行应用: python main.py")
        print("4. 打开浏览器: http://localhost:5000")
    else:
        print("✗ 项目结构不完整，存在缺失的文件或目录")
    
    return all_good

if __name__ == "__main__":
    import sys
    success = check_structure()
    sys.exit(0 if success else 1)
