#!/bin/bash
# PyDayflow启动脚本 (Linux/Mac)

echo "========================================"
echo "PyDayflow - 屏幕活动时间线追踪器"
echo "========================================"
echo ""

# 检查Python是否已安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3！"
    echo "请安装Python 3.8+"
    exit 1
fi

echo "检查依赖..."
pip3 install -r requirements.txt > /dev/null 2>&1

echo ""
echo "启动PyDayflow..."
echo "Web界面将在 http://localhost:5000 打开"
echo ""
echo "按 Ctrl+C 停止应用"
echo "========================================"
echo ""

python3 main.py
