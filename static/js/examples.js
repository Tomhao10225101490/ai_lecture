class ExamplesManager {
    constructor() {
        // 获取DOM元素
        this.gradeFilter = document.querySelector('.filter-select[data-type="grade"]');
        this.typeFilter = document.querySelector('.filter-select[data-type="type"]');
        this.examplesGrid = document.querySelector('.examples-grid');

        // 存储所有范文数据
        this.allExamples = [
            {
                id: 1,
                title: "春天的早晨",
                grade: "高中",
                type: "记叙文",
                preview: "清晨，第一缕阳光透过窗帘洒在书桌上，我推开窗，深深地呼吸着春天的气息...",
                image: "tutorial.jpg"
            },
            {
                id: 2,
                title: "科技与生活",
                grade: "高中",
                type: "议论文",
                preview: "随着科技的快速发展，我们的生活方式发生了翻天覆地的变化...",
                image: "tutorial.jpg"
            },
            {
                id: 3,
                title: "我的理想生活",
                grade: "初中",
                type: "记叙文",
                preview: "每个人都有自己憧憬的理想生活，而我的理想生活是...",
                image: "tutorial.jpg"
            },
            {
                id: 4,
                title: "保护环境",
                grade: "小学",
                type: "议论文",
                preview: "环境保护是每个人的责任，从我做起...",
                image: "tutorial.jpg"
            }
        ];

        // 初始化事件监听器
        this.initializeEventListeners();
        
        // 加载初始数据
        this.loadExamples();
    }

    initializeEventListeners() {
        // 添加筛选器变化事件
        if (this.gradeFilter) {
            this.gradeFilter.addEventListener('change', () => this.filterExamples());
        }
        if (this.typeFilter) {
            this.typeFilter.addEventListener('change', () => this.filterExamples());
        }
    }

    filterExamples() {
        const selectedGrade = this.gradeFilter.value;
        const selectedType = this.typeFilter.value;
        
        // 筛选数据
        let filteredData = this.allExamples;
        
        if (selectedGrade !== 'all') {
            filteredData = filteredData.filter(example => example.grade === this.getGradeText(selectedGrade));
        }
        
        if (selectedType !== 'all') {
            filteredData = filteredData.filter(example => example.type === this.getTypeText(selectedType));
        }
        
        // 渲染筛选后的数据
        this.renderExamples(filteredData);
    }

    getGradeText(value) {
        const gradeMap = {
            'primary': '小学',
            'junior': '初中',
            'senior': '高中'
        };
        return gradeMap[value] || value;
    }

    getTypeText(value) {
        const typeMap = {
            'narrative': '记叙文',
            'argumentative': '议论文',
            'descriptive': '描写文'
        };
        return typeMap[value] || value;
    }

    loadExamples() {
        this.renderExamples(this.allExamples);
    }

    renderExamples(data) {
        if (!this.examplesGrid) return;

        if (data.length === 0) {
            this.examplesGrid.innerHTML = `
                <div class="no-results">
                    <p>暂无符合条件的范文</p>
                </div>
            `;
            return;
        }

        this.examplesGrid.innerHTML = data.map(example => `
            <div class="example-card" data-id="${example.id}">
                <img src="/static/images/${example.image}" alt="${example.title}配图" class="example-image">
                <div class="example-content">
                    <h3 class="example-title">${example.title}</h3>
                    <div class="example-meta">
                        <span><i class="fas fa-graduation-cap"></i> ${example.grade}</span>
                        <span><i class="fas fa-tag"></i> ${example.type}</span>
                    </div>
                    <p class="example-preview">${example.preview}</p>
                    <a href="/example/${example.id}" class="read-more">阅读全文</a>
                </div>
            </div>
        `).join('');
    }
}

// 当DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new ExamplesManager();
}); 