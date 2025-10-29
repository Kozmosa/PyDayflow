# 🚀 PyDayflow 快速开始

## 一分钟启动指南

### Windows用户

1. **下载项目**
   ```
   下载并解压PyDayflow
   ```

2. **双击启动**
   ```
   双击 start.bat 文件
   ```

3. **配置API密钥（首次使用）**
   - 复制 `.env.example` 重命名为 `.env`
   - 访问 https://ai.google.dev/ 获取免费的Gemini API密钥
   - 编辑 `.env` 文件，填入您的API密钥：
     ```
     GEMINI_API_KEY=你的密钥
     ```

4. **开始使用**
   - 浏览器自动打开 http://localhost:5000
   - 点击"开始录制"
   - 等待15分钟后查看时间线

就这么简单！✨

---

### Linux/Mac用户

```bash
# 1. 进入项目目录
cd PyDayflow

# 2. 运行启动脚本
chmod +x start.sh
./start.sh

# 3. 打开浏览器
# 访问 http://localhost:5000
```

---

## 📖 详细文档

需要更多帮助？查看：

- **[安装指南](docs/INSTALLATION_GUIDE.md)** - 详细安装说明和故障排除
- **[项目概览](docs/PROJECT_OVERVIEW.md)** - 完整项目介绍
- **[架构文档](docs/ARCHITECTURE.md)** - 技术架构说明
- **[Python版README](PYDAYFLOW_README.md)** - Python版本完整说明

---

## 💡 提示

### 首次使用建议

1. **获取API密钥**
   - 免费的Gemini API密钥：https://ai.google.dev/
   - 每天有慷慨的免费额度

2. **或使用本地LLM**
   ```bash
   # 安装Ollama
   # 从 https://ollama.com 下载安装
   
   # 拉取模型
   ollama pull llava
   
   # 在.env中设置
   AI_PROVIDER=local
   ```

3. **调整设置**
   - 降低帧率节省空间：`CAPTURE_FPS=0.5`
   - 增加保留天数：`RETENTION_DAYS=7`
   - 更改端口：`WEB_PORT=8080`

---

## ❓ 常见问题

### Q: 需要一直打开浏览器吗？
**A:** 不需要！关闭浏览器后，后台会继续录制。需要查看时随时打开 http://localhost:5000

### Q: 录制会占用多少空间？
**A:** 约100MB/天（1 FPS录制）。可通过降低FPS或减少保留天数来节省空间。

### Q: 如何停止应用？
**A:** 在命令窗口按 `Ctrl+C`，或直接关闭命令窗口。

### Q: 数据存储在哪里？
**A:** Windows: `C:\Users\你的用户名\PyDayflow\`

### Q: 可以离线使用吗？
**A:** 可以！使用本地LLM（Ollama）即可完全离线运行。

---

## 🎯 快速功能演示

### 录制您的活动
```
1. 点击"开始录制"
2. 继续正常工作
3. 应用在后台以1 FPS捕获屏幕
```

### 查看时间线
```
1. 等待15分钟（或点击"立即分析"）
2. AI自动分析生成摘要
3. 在时间线中查看活动卡片
```

### 浏览历史
```
1. 使用日期选择器
2. 查看任意日期的活动
3. 了解时间使用情况
```

---

## 🔧 系统要求

- ✅ Windows 10/11（或Linux/Mac）
- ✅ Python 3.8+
- ✅ 4GB+ RAM（推荐）
- ✅ 500MB+ 磁盘空间
- ✅ 网络连接（使用Gemini时）

---

## 📞 获取帮助

- 🐛 **遇到问题？** 查看 `pydayflow.log` 日志文件
- 📖 **需要帮助？** 阅读[安装指南](docs/INSTALLATION_GUIDE.md)
- 💬 **有建议？** 在GitHub创建Issue

---

## ⭐ 下一步

完成设置后：

1. ✅ 让应用运行一整天
2. ✅ 晚上回顾您的时间线
3. ✅ 发现时间使用模式
4. ✅ 提高工作效率！

---

<div align="center">

**准备好开始了吗？**

运行 `start.bat` 然后访问 http://localhost:5000

祝您使用愉快！🎉

</div>
