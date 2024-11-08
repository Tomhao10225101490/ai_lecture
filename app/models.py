from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EssayHistory(db.Model):
    __tablename__ = 'essay_history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100, collation='utf8mb4_unicode_ci'), nullable=False)
    content = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    grade = db.Column(db.String(20, collation='utf8mb4_unicode_ci'), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # 存储详细评阅结果（JSON格式）
    review_result = db.Column(db.JSON, nullable=False)
    
    # 添加是否为优秀范文的标记（分数>=88分自动标记为优秀范文）
    is_example = db.Column(db.Boolean, default=False)
    essay_type = db.Column(db.String(20, collation='utf8mb4_unicode_ci'))  # 记叙文、议论文等
    
    # 添加索引
    __table_args__ = (
        db.Index('idx_grade_created', 'grade', 'created_at'),
        db.Index('idx_score_example', 'total_score', 'is_example'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'grade': self.grade,
            'total_score': self.total_score,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'review_result': self.review_result,
            'is_example': self.is_example,
            'essay_type': self.essay_type
        } 