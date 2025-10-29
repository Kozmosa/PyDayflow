// PyDayflow Frontend JavaScript

class PyDayflowApp {
    constructor() {
        this.apiBase = '';
        this.isRecording = false;
        this.init();
    }

    init() {
        // Set up event listeners
        document.getElementById('startBtn').addEventListener('click', () => this.startRecording());
        document.getElementById('stopBtn').addEventListener('click', () => this.stopRecording());
        document.getElementById('analyzeBtn').addEventListener('click', () => this.triggerAnalysis());
        document.getElementById('cleanupBtn').addEventListener('click', () => this.triggerCleanup());
        document.getElementById('refreshBtn').addEventListener('click', () => this.loadTimeline());
        
        // Set up date selector
        const dateSelector = document.getElementById('dateSelector');
        dateSelector.value = new Date().toISOString().split('T')[0];
        dateSelector.addEventListener('change', () => this.loadTimeline());
        
        // Initial load
        this.updateStatus();
        this.loadTimeline();
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            this.updateStatus();
            if (!this.isRecording) {
                this.loadTimeline();
            }
        }, 30000);
    }

    async startRecording() {
        try {
            const response = await fetch(`${this.apiBase}/api/recording/start`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                this.isRecording = true;
                this.updateRecordingUI();
                this.showNotification('开始录制屏幕', 'success');
            } else {
                this.showNotification('启动录制失败', 'error');
            }
        } catch (error) {
            console.error('Error starting recording:', error);
            this.showNotification('启动录制时出错', 'error');
        }
    }

    async stopRecording() {
        try {
            const response = await fetch(`${this.apiBase}/api/recording/stop`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                this.isRecording = false;
                this.updateRecordingUI();
                this.showNotification('已停止录制', 'info');
                // Refresh timeline after stopping
                setTimeout(() => this.loadTimeline(), 1000);
            } else {
                this.showNotification('停止录制失败', 'error');
            }
        } catch (error) {
            console.error('Error stopping recording:', error);
            this.showNotification('停止录制时出错', 'error');
        }
    }

    async triggerAnalysis() {
        try {
            this.showNotification('正在分析录制内容...', 'info');
            
            const response = await fetch(`${this.apiBase}/api/analyze`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                this.showNotification('分析完成', 'success');
                setTimeout(() => this.loadTimeline(), 1000);
            } else {
                this.showNotification('分析失败: ' + (data.error || '未知错误'), 'error');
            }
        } catch (error) {
            console.error('Error triggering analysis:', error);
            this.showNotification('触发分析时出错', 'error');
        }
    }

    async triggerCleanup() {
        if (!confirm('确定要清理旧的录制数据吗？这将删除超过保留期限的所有录制。')) {
            return;
        }
        
        try {
            this.showNotification('正在清理旧数据...', 'info');
            
            const response = await fetch(`${this.apiBase}/api/cleanup`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                this.showNotification('清理完成', 'success');
                this.updateStatus();
            } else {
                this.showNotification('清理失败: ' + (data.error || '未知错误'), 'error');
            }
        } catch (error) {
            console.error('Error triggering cleanup:', error);
            this.showNotification('触发清理时出错', 'error');
        }
    }

    async updateStatus() {
        try {
            const response = await fetch(`${this.apiBase}/api/status`);
            const data = await response.json();
            
            // Update recording status
            this.isRecording = data.recording.is_recording;
            this.updateRecordingUI();
            
            // Update stats
            const statsDiv = document.getElementById('stats');
            const storage = data.storage;
            
            statsDiv.innerHTML = `
                <p><strong>录制状态:</strong> ${this.isRecording ? '正在录制' : '未录制'}</p>
                <p><strong>采集帧率:</strong> ${data.recording.fps} FPS</p>
                <p><strong>存储空间:</strong> ${storage ? `${storage.total_size_mb.toFixed(2)} MB` : '计算中...'}</p>
                <p><strong>录制文件数:</strong> ${storage ? storage.file_count : '0'}</p>
                <p><strong>分析状态:</strong> ${data.analysis_running ? '运行中' : '已停止'}</p>
            `;
        } catch (error) {
            console.error('Error updating status:', error);
        }
    }

    updateRecordingUI() {
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const statusBadge = document.getElementById('recordingStatus');
        
        if (this.isRecording) {
            startBtn.disabled = true;
            stopBtn.disabled = false;
            statusBadge.textContent = '正在录制';
            statusBadge.classList.add('recording');
        } else {
            startBtn.disabled = false;
            stopBtn.disabled = true;
            statusBadge.textContent = '未录制';
            statusBadge.classList.remove('recording');
        }
    }

    async loadTimeline() {
        try {
            const dateSelector = document.getElementById('dateSelector');
            const selectedDate = dateSelector.value;
            
            const response = await fetch(`${this.apiBase}/api/timeline?date=${selectedDate}`);
            const data = await response.json();
            
            this.renderTimeline(data.cards);
        } catch (error) {
            console.error('Error loading timeline:', error);
            this.showNotification('加载时间线时出错', 'error');
        }
    }

    renderTimeline(cards) {
        const timelineDiv = document.getElementById('timeline');
        
        if (!cards || cards.length === 0) {
            timelineDiv.innerHTML = '<p class="timeline-empty">该日期暂无数据</p>';
            return;
        }
        
        let html = '';
        cards.forEach(card => {
            const startTime = new Date(card.start_time).toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit'
            });
            const endTime = new Date(card.end_time).toLocaleTimeString('zh-CN', {
                hour: '2-digit',
                minute: '2-digit'
            });
            
            const categoryText = {
                'work': '工作',
                'personal': '个人',
                'distraction': '分心'
            }[card.category] || card.category;
            
            html += `
                <div class="timeline-card ${card.category}">
                    <div class="card-time">${startTime} - ${endTime}</div>
                    <div class="card-title">${this.escapeHtml(card.title)}</div>
                    <div class="card-summary">${this.escapeHtml(card.summary)}</div>
                    <span class="card-category ${card.category}">${categoryText}</span>
                </div>
            `;
        });
        
        timelineDiv.innerHTML = html;
    }

    showNotification(message, type = 'info') {
        // Simple notification - you could use a more sophisticated notification library
        console.log(`[${type.toUpperCase()}] ${message}`);
        alert(message);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new PyDayflowApp();
});
