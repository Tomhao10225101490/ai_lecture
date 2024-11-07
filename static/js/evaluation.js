document.getElementById('submitBtn').addEventListener('click', async function() {
    const title = document.getElementById('title').value.trim();
    const content = document.getElementById('content').value.trim();
    const grade = document.getElementById('gradeLevel').value;
    
    if (!title || !content) {
        alert('请填写完整的作文信息');
        return;
    }
    
    // 显示加载状态
    this.disabled = true;
    this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>评阅中...';
    
    try {
        const response = await fetch('/api/review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title,
                content,
                grade: getGradeText(grade)
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 将评阅结果存储到 sessionStorage
            sessionStorage.setItem('reviewResult', JSON.stringify({
                title,
                grade: getGradeText(grade),
                content,
                ...result.data
            }));
            
            // 跳转到结果页面
            window.location.href = '/result';
        } else {
            alert(result.message || '评阅失败，请稍后重试');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('网络错误，请稍后重试');
    } finally {
        // 恢复按钮状态
        this.disabled = false;
        this.innerHTML = '<i class="fas fa-pen-fancy"></i>开始评阅';
    }
});

// 转换年级值为中文
function getGradeText(value) {
    const gradeMap = {
        'primary': '小学',
        'junior': '初中',
        'senior': '高中'
    };
    return gradeMap[value] || value;
} 