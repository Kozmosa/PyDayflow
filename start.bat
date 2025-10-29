@echo off
REM PyDayflow启动脚本 (Windows)

echo ========================================
echo PyDayflow - 屏幕活动时间线追踪器
echo ========================================
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python！
    echo 请从 https://www.python.org/downloads/ 安装Python 3.8+
    pause
    exit /b 1
)

echo 检查依赖...
pip install -r requirements.txt >nul 2>&1

echo.
echo 启动PyDayflow...
echo Web界面将在 http://localhost:5000 打开
echo.
echo 按 Ctrl+C 停止应用
echo ========================================
echo.

python main.py

pause
