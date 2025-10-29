# PyDayflow 架构设计

## 系统架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                      Web浏览器界面                            │
│  (HTML/CSS/JavaScript - http://localhost:5000)              │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                    Flask Web服务器                           │
│                   (pydayflow/web/app.py)                     │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      核心业务层                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ 屏幕录制器    │  │ 分析管理器    │  │ 存储管理器    │      │
│  │ScreenRecorder│  │AnalysisManager│  │StorageManager│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│          ↕                 ↕                  ↕              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   mss库      │  │  AI服务       │  │  文件系统     │      │
│  │ (屏幕捕获)    │  │  AIService    │  │  (视频存储)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                           ↕                                 │
│                    ┌──────────────┐                         │
│                    │ Gemini/Local │                         │
│                    │     LLM      │                         │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    数据持久层                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            SQLite数据库 (pydayflow.db)                 │  │
│  │  - recordings (录制记录)                               │  │
│  │  - timeline_cards (时间线卡片)                         │  │
│  │  - app_state (应用状态)                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. Web层 (pydayflow/web/)

**Flask应用 (app.py)**
- 提供REST API端点
- 处理HTTP请求和响应
- 协调各个核心服务

**前端界面**
- `templates/index.html` - HTML结构
- `static/css/style.css` - 样式表
- `static/js/app.js` - 前端逻辑

**API端点**
- GET `/` - 主页面
- GET `/api/status` - 系统状态
- POST `/api/recording/start` - 开始录制
- POST `/api/recording/stop` - 停止录制
- GET `/api/timeline` - 获取时间线
- POST `/api/analyze` - 触发分析
- POST `/api/cleanup` - 清理数据

### 2. 核心业务层 (pydayflow/core/)

**屏幕录制器 (recording/screen_recorder.py)**
- 使用mss库捕获屏幕
- 1 FPS录制（低资源消耗）
- 每15秒保存一个视频块
- 多线程后台运行

**分析管理器 (analysis/analysis_manager.py)**
- APScheduler定时任务
- 每15分钟触发分析
- 批量处理录制
- 生成时间线卡片

**AI服务 (ai/ai_service.py)**
- 支持Gemini API
- 支持本地LLM (Ollama)
- 视频分析和摘要生成
- 分类和置信度评分

**存储管理器 (storage/storage_manager.py)**
- OpenCV视频编码
- 按日期组织文件
- 自动清理旧数据
- 存储统计

### 3. 数据层 (pydayflow/models/)

**数据库模型 (database.py)**

```python
Recording:
- id: 主键
- start_time: 开始时间
- end_time: 结束时间
- file_path: 文件路径
- duration: 持续时间
- analyzed: 是否已分析

TimelineCard:
- id: 主键
- start_time: 开始时间
- end_time: 结束时间
- title: 标题
- summary: 摘要
- category: 分类 (work/personal/distraction)
- confidence: 置信度
- thumbnail_path: 缩略图路径

AppState:
- key: 配置键
- value: 配置值
```

### 4. 工具层 (pydayflow/utils/)

**配置管理 (config.py)**
- 环境变量加载
- 配置验证
- 默认值设置

## 数据流

### 录制流程

```
用户点击"开始录制"
    ↓
Flask接收POST请求
    ↓
调用ScreenRecorder.start_recording()
    ↓
启动后台线程
    ↓
循环捕获屏幕 (1 FPS)
    ↓
每15秒保存视频块
    ↓
StorageManager保存到文件系统
    ↓
Recording记录写入数据库
```

### 分析流程

```
定时任务触发 (每15分钟)
    ↓
AnalysisManager.analyze_pending_recordings()
    ↓
查询未分析的Recording
    ↓
按15分钟批次分组
    ↓
对每个批次:
    ↓
    调用AIService.analyze_video_chunk()
    ↓
    发送到Gemini/Local LLM
    ↓
    接收分析结果
    ↓
    创建TimelineCard
    ↓
    标记Recording为已分析
    ↓
提交到数据库
```

### 查看流程

```
用户打开时间线页面
    ↓
选择日期
    ↓
前端发送GET /api/timeline?date=YYYY-MM-DD
    ↓
AnalysisManager.get_timeline()
    ↓
查询数据库中的TimelineCard
    ↓
返回JSON数据
    ↓
前端渲染时间线卡片
```

## 技术栈

### 后端
- **Python 3.8+** - 主要语言
- **Flask** - Web框架
- **SQLAlchemy** - ORM
- **APScheduler** - 定时任务
- **mss** - 屏幕捕获
- **OpenCV** - 视频处理

### 前端
- **HTML5** - 结构
- **CSS3** - 样式
- **Vanilla JavaScript** - 逻辑
- **Fetch API** - HTTP请求

### AI
- **Google Gemini API** - 云端分析
- **Ollama** - 本地LLM

### 存储
- **SQLite** - 关系数据库
- **文件系统** - 视频存储

## 性能考虑

### 资源占用
- **CPU**: <5% (1 FPS录制)
- **内存**: ~200MB (Python + Flask)
- **存储**: ~100MB/天 (1 FPS, MP4压缩)

### 优化策略
1. 低帧率录制 (1 FPS)
2. 定期批量分析
3. 自动数据清理
4. 视频压缩
5. 异步处理

## 安全性

### 数据隐私
- 本地存储所有录制
- 用户控制AI提供商
- 支持完全离线模式

### 配置保护
- API密钥存储在.env
- .gitignore排除敏感文件
- 环境变量隔离

## 扩展性

### 支持的扩展
1. 新的AI提供商
2. 自定义分析规则
3. 导出功能
4. 多显示器支持
5. 更多可视化选项

### 接口设计
- 模块化架构
- 依赖注入
- 清晰的API边界
