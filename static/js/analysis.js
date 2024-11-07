class AnalysisDashboard {
    constructor() {
        this.initializeCharts();
    }

    initializeCharts() {
        // 分数分布趋势图
        const scoreCtx = document.getElementById('scoreChart').getContext('2d');
        new Chart(scoreCtx, {
            type: 'line',
            data: {
                labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
                datasets: [{
                    label: '作文分数',
                    data: [85, 88, 82, 90, 85, 92, 88],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 60,
                        max: 100
                    }
                }
            }
        });

        // 评分维度分析图
        const dimensionCtx = document.getElementById('dimensionChart').getContext('2d');
        new Chart(dimensionCtx, {
            type: 'radar',
            data: {
                labels: ['内容立意', '结构布局', '语言表达', '书写规范'],
                datasets: [{
                    label: '当前水平',
                    data: [85, 78, 82, 90],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.2)',
                    pointBackgroundColor: '#3498db',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#3498db'
                }, {
                    label: '平均水平',
                    data: [75, 75, 75, 75],
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.2)',
                    pointBackgroundColor: '#e74c3c',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#e74c3c'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    r: {
                        min: 0,
                        max: 100,
                        beginAtZero: true,
                        ticks: {
                            stepSize: 20
                        }
                    }
                }
            }
        });

        // 为图表选择器添加事件监听
        const chartSelect = document.querySelector('.chart-select');
        if (chartSelect) {
            chartSelect.addEventListener('change', (e) => {
                this.updateChartData(e.target.value);
            });
        }
    }

    updateChartData(timeRange) {
        // 这里可以根据选择的时间范围更新图表数据
        console.log('Updating chart for time range:', timeRange);
        // 可以添加API调用来获取不同时间范围的数据
    }

    // 可以添加更多方法来处理其他功能
}

// 当DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new AnalysisDashboard();
}); 