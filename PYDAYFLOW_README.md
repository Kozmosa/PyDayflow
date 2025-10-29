# PyDayflow - Windows版本

<div align="center">
  <em>Dayflow的Python重写版本，专为Windows系统设计，使用Web UI界面</em><br>
  自动记录屏幕活动，通过AI生成时间线摘要
</div>

## 🌟 特性

- **自动屏幕录制** - 以1 FPS的速率捕获屏幕（低CPU和存储占用）
- **AI分析** - 每15分钟自动分析并生成活动摘要
- **Web界面** - 现代化的Web UI，可在任何浏览器中访问
- **时间线视图** - 直观地查看您的每日活动
- **多AI提供商** - 支持Gemini API或本地LLM（Ollama）
- **自动清理** - 3天后自动删除旧录制
- **跨平台** - 主要为Windows设计，也可在其他平台运行

## 📋 系统要求

- Windows 10/11（或其他支持Python的操作系统）
- Python 3.8+
- 推荐4GB+ RAM
- 推荐500MB+ 可用磁盘空间

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆仓库
git clone https://github.com/Kozmosa/PyDayflow.git
cd PyDayflow

# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置

创建 `.env` 文件（从模板复制）：

```bash
copy .env.example .env
```

编辑 `.env` 文件，配置您的设置：

```env
# 如果使用Gemini
AI_PROVIDER=gemini
GEMINI_API_KEY=your_api_key_here

# 或者使用本地LLM
AI_PROVIDER=local
LOCAL_LLM_URL=http://localhost:11434
```

**获取Gemini API密钥：**
访问 https://ai.google.dev/gemini-api/docs/api-key

### 3. 运行

```bash
python main.py
```

应用将在 `http://localhost:5000` 启动

## 🎯 使用方法

1. **打开浏览器** 访问 `http://localhost:5000`
2. **开始录制** 点击"开始录制"按钮
3. **等待分析** 应用会每15分钟自动分析录制内容
4. **查看时间线** 在界面中查看您的活动时间线

## 📁 项目结构

```
PyDayflow/
├── pydayflow/               # 主应用包
│   ├── core/               # 核心功能模块
│   │   ├── recording/      # 屏幕录制
│   │   ├── analysis/       # 分析管理
│   │   ├── ai/            # AI集成
│   │   └── storage/       # 存储管理
│   ├── models/            # 数据库模型
│   ├── utils/             # 工具函数
│   └── web/               # Web应用
│       ├── static/        # 静态文件（CSS/JS）
│       └── templates/     # HTML模板
├── main.py                # 应用入口
├── requirements.txt       # Python依赖
└── .env.example          # 配置模板
```

## 🔧 配置选项

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DEBUG` | False | 调试模式 |
| `WEB_PORT` | 5000 | Web服务器端口 |
| `DATA_DIR` | ~/PyDayflow | 数据存储目录 |
| `CAPTURE_FPS` | 1.0 | 录制帧率 |
| `ANALYSIS_INTERVAL` | 900 | 分析间隔（秒） |
| `RETENTION_DAYS` | 3 | 录制保留天数 |
| `AI_PROVIDER` | gemini | AI提供商 (gemini/local) |
| `GEMINI_API_KEY` | - | Gemini API密钥 |
| `GEMINI_MODEL` | gemini-1.5-flash | Gemini模型 |
| `LOCAL_LLM_URL` | http://localhost:11434 | 本地LLM地址 |

## 🤖 AI提供商

### Gemini（推荐）

- 快速高效（每15分钟仅2次LLM调用）
- 原生视频理解
- 需要API密钥（免费额度可用）

### 本地LLM（Ollama）

- 完全私密（数据不离开您的电脑）
- 需要更多资源
- 安装Ollama：https://ollama.com/

```bash
# 安装Ollama后，拉取视觉模型
ollama pull llava
```

## 📊 数据和隐私

- **所有录制数据** 存储在本地计算机（默认：`~/PyDayflow/`）
- **使用Gemini时** 视频片段会发送到Google的Gemini API进行分析
- **使用本地模式** 所有处理都在您的计算机上进行
- **自动清理** 3天后自动删除录制文件

## 🛠️ 开发

### 运行测试

```bash
pytest
```

### 代码风格

```bash
# 使用black格式化代码
black .

# 使用flake8检查代码
flake8 .
```

## 📝 API端点

- `GET /` - Web界面
- `GET /api/status` - 获取系统状态
- `POST /api/recording/start` - 开始录制
- `POST /api/recording/stop` - 停止录制
- `GET /api/timeline?date=YYYY-MM-DD` - 获取时间线
- `POST /api/analyze` - 手动触发分析
- `POST /api/cleanup` - 清理旧数据

## 🔍 故障排除

### 录制不工作

- 确保Python有屏幕录制权限
- Windows: 检查隐私设置 → 屏幕捕获权限

### AI分析失败

- 检查API密钥是否正确
- 验证网络连接
- 查看日志文件 `pydayflow.log`

### 内存占用高

- 降低 `CAPTURE_FPS`
- 减少 `RETENTION_DAYS`
- 更频繁地运行清理

## 🤝 贡献

欢迎贡献！请随时提交问题或拉取请求。

## 📄 许可证

MIT许可证 - 详见 LICENSE 文件

## 🙏 致谢

- 基于原始的 [Dayflow](https://github.com/JerryZLiu/Dayflow) macOS应用
- 使用 [mss](https://github.com/BoboTiG/python-mss) 进行屏幕捕获
- 使用 [Flask](https://flask.palletsprojects.com/) 构建Web界面
- AI功能由 [Google Gemini](https://ai.google.dev/) 提供支持

## 📞 支持

如有问题或需要帮助，请：
1. 查看故障排除部分
2. 检查现有的GitHub问题
3. 创建新问题并提供详细信息

---

<div align="center">
  使用 ❤️ 和 Python 制作
</div>
