# PyDayflow 安装和使用指南

## Windows用户快速开始

### 方法1: 使用启动脚本（推荐）

1. **下载项目**
   ```
   从GitHub下载ZIP文件并解压
   或使用git: git clone https://github.com/Kozmosa/PyDayflow.git
   ```

2. **双击运行**
   ```
   双击 start.bat 文件
   ```
   
   脚本会自动:
   - 检查Python是否已安装
   - 安装所需的依赖
   - 启动应用
   - 在浏览器中打开 http://localhost:5000

### 方法2: 手动安装

1. **确保已安装Python**
   - 下载Python 3.8+: https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. **打开命令提示符**
   - 按 Win+R
   - 输入 "cmd" 并回车

3. **进入项目目录**
   ```cmd
   cd C:\path\to\PyDayflow
   ```

4. **安装依赖**
   ```cmd
   pip install -r requirements.txt
   ```

5. **配置环境变量**
   ```cmd
   copy .env.example .env
   notepad .env
   ```
   
   编辑.env文件，设置您的配置:
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=你的API密钥
   ```

6. **运行应用**
   ```cmd
   python main.py
   ```

7. **打开浏览器**
   访问: http://localhost:5000

## Linux/Mac用户

1. **打开终端**

2. **进入项目目录**
   ```bash
   cd /path/to/PyDayflow
   ```

3. **使用启动脚本**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

   或手动运行:
   ```bash
   pip3 install -r requirements.txt
   python3 main.py
   ```

## 配置说明

### 获取Gemini API密钥

1. 访问: https://ai.google.dev/
2. 点击 "Get API Key"
3. 登录Google账号
4. 创建API密钥
5. 复制密钥到.env文件

### 使用本地LLM（可选）

如果您想要完全离线运行:

1. **安装Ollama**
   - Windows: https://ollama.com/download/windows
   - Mac: `brew install ollama`
   - Linux: `curl -fsSL https://ollama.com/install.sh | sh`

2. **拉取模型**
   ```bash
   ollama pull llava
   ```

3. **配置.env**
   ```
   AI_PROVIDER=local
   LOCAL_LLM_URL=http://localhost:11434
   ```

## 使用教程

### 第一次使用

1. **启动应用**
   - 运行start.bat (Windows) 或 start.sh (Linux/Mac)
   - 或直接运行: `python main.py`

2. **打开Web界面**
   - 浏览器自动打开 http://localhost:5000
   - 或手动访问该地址

3. **开始录制**
   - 点击"开始录制"按钮
   - 应用开始以1 FPS捕获屏幕
   - 状态指示器显示"正在录制"

4. **等待分析**
   - 默认每15分钟自动分析一次
   - 或点击"立即分析"手动触发
   - AI会生成活动摘要

5. **查看时间线**
   - 在时间线区域查看您的活动
   - 使用日期选择器查看历史
   - 点击卡片查看详细信息

### 日常使用

1. **开机启动**
   - Windows: 将start.bat快捷方式添加到启动文件夹
     - Win+R → `shell:startup`
     - 将start.bat快捷方式拖入

2. **后台运行**
   - 最小化命令窗口
   - 应用继续在后台录制

3. **查看时间线**
   - 随时打开 http://localhost:5000
   - 查看今天的活动
   - 选择其他日期查看历史

### 数据管理

1. **清理旧数据**
   - 点击"清理旧数据"按钮
   - 删除超过3天的录制（可配置）

2. **数据位置**
   - Windows: `C:\Users\你的用户名\PyDayflow\`
   - Linux/Mac: `~/PyDayflow/`

3. **备份数据**
   - 复制整个数据目录
   - 包含录制和数据库

## 常见问题

### 应用无法启动

**问题**: Python未找到
- **解决**: 安装Python 3.8+ 并添加到PATH

**问题**: 依赖安装失败
- **解决**: 
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt --no-cache-dir
  ```

### 录制不工作

**问题**: 屏幕捕获权限
- **Windows**: 检查隐私设置 → 屏幕捕获
- **Mac**: 系统偏好设置 → 安全性 → 屏幕录制

**问题**: 录制文件太大
- **解决**: 降低FPS或减少保留天数
  ```
  CAPTURE_FPS=0.5
  RETENTION_DAYS=1
  ```

### AI分析失败

**问题**: API密钥无效
- **解决**: 检查.env文件中的GEMINI_API_KEY

**问题**: 网络连接
- **解决**: 检查网络连接或使用本地LLM

**问题**: 分析时间长
- **解决**: Gemini更快，本地LLM较慢

### 性能问题

**问题**: CPU占用高
- **解决**: 降低帧率
  ```
  CAPTURE_FPS=0.5
  ```

**问题**: 存储空间不足
- **解决**: 
  - 减少保留天数
  - 手动清理旧数据
  - 增加磁盘空间

## 高级配置

### 自定义端口

```env
WEB_PORT=8080
```

### 自定义数据目录

```env
DATA_DIR=D:\MyDayflowData
```

### 调整分析频率

```env
ANALYSIS_INTERVAL=1800  # 30分钟
```

### 启用调试模式

```env
DEBUG=True
```

## 技术支持

遇到问题？

1. 查看日志文件: `pydayflow.log`
2. 检查GitHub Issues
3. 创建新Issue并提供:
   - 操作系统版本
   - Python版本
   - 错误信息
   - 日志文件

## 卸载

1. **停止应用**
   - 关闭命令窗口

2. **删除数据**
   - 删除数据目录（如 `C:\Users\你的用户名\PyDayflow\`）

3. **删除程序**
   - 删除PyDayflow文件夹

## 下一步

- 探索时间线功能
- 尝试不同的AI提供商
- 调整配置优化性能
- 查看API文档进行集成

祝您使用愉快！🎉
