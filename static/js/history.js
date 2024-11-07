class HistoryManager {
    constructor() {
        // 获取DOM元素
        this.filterGrade = document.querySelector('.filter-select[data-type="grade"]');
        this.filterTime = document.querySelector('.filter-select[data-type="time"]');
        this.historyList = document.querySelector('.history-list');

        // 初始化事件监听器
        this.initializeEventListeners();
        
        // 加载初始数据
        this.loadHistoryData();
    }

    initializeEventListeners() {
        // 添加筛选器变化事件
        if (this.filterGrade) {
            this.filterGrade.addEventListener('change', () => this.filterHistory());
        }
        if (this.filterTime) {
            this.filterTime.addEventListener('change', () => this.filterHistory());
        }

        // 为所有删除按钮添加事件委托
        if (this.historyList) {
            this.historyList.addEventListener('click', (e) => {
                const deleteBtn = e.target.closest('.delete-btn');
                const viewBtn = e.target.closest('.view-btn');
                
                if (deleteBtn) {
                    const historyItem = deleteBtn.closest('.history-item');
                    if (historyItem) {
                        const id = historyItem.dataset.id;
                        this.deleteHistory(id);
                    }
                }
                
                if (viewBtn) {
                    const historyItem = viewBtn.closest('.history-item');
                    if (historyItem) {
                        const id = historyItem.dataset.id;
                        this.viewHistory(id);
                    }
                }
            });
        }
    }

    async loadHistoryData() {
        // 这里可以添加加载动画
        try {
            // 模拟从服务器获取数据
            const historyData = [
                {
                    id: 1,
                    title: "我的理想生活",
                    grade: "高中",
                    date: "2024-03-20",
                    score: 92
                },
                {
                    id: 2,
                    title: "难忘的一天",
                    grade: "初中",
                    date: "2024-03-19",
                    score: 88
                }
                // 可以添加更多示例数据
            ];

            this.renderHistoryList(historyData);
        } catch (error) {
            console.error('Error loading history:', error);
            // 显示错误提示
            this.showError('加载历史记录失败，请稍后重试');
        }
    }

    renderHistoryList(data) {
        if (!this.historyList) return;

        this.historyList.innerHTML = data.map(item => `
            <div class="history-item" data-id="${item.id}">
                <div class="history-info">
                    <h3>${item.title}</h3>
                    <div class="history-meta">
                        <span><i class="fas fa-graduation-cap"></i> ${item.grade}</span>
                        <span><i class="fas fa-calendar"></i> ${item.date}</span>
                    </div>
                </div>
                <div class="history-score">${item.score}分</div>
                <div class="history-actions">
                    <button class="action-btn view-btn">
                        <i class="fas fa-eye"></i>查看
                    </button>
                    <button class="action-btn delete-btn">
                        <i class="fas fa-trash"></i>删除
                    </button>
                </div>
            </div>
        `).join('');
    }

    filterHistory() {
        const grade = this.filterGrade ? this.filterGrade.value : 'all';
        const time = this.filterTime ? this.filterTime.value : 'all';
        
        // 这里可以实现筛选逻辑
        console.log('Filtering by:', { grade, time });
        // 重新加载数据
        this.loadHistoryData();
    }

    async deleteHistory(id) {
        if (!confirm('确定要删除这条记录吗？')) return;

        try {
            // 这里添加删除的API调用
            console.log('Deleting history:', id);
            // 重新加载数据
            this.loadHistoryData();
        } catch (error) {
            console.error('Error deleting history:', error);
            this.showError('删除失败，请稍后重试');
        }
    }

    viewHistory(id) {
        // 跳转到详情页面
        window.location.href = `/result?id=${id}`;
    }

    showError(message) {
        // 简单的错误提示
        alert(message);
    }
}

// 当DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new HistoryManager();
}); 