from flask import render_template, request, jsonify
from app.utils.ai_review import analyze_essay
from app.utils.ai_chat import chat_with_ai
from app.models import db, EssayHistory
from datetime import datetime, timedelta
from sqlalchemy import func

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/history')
    def history():
        return render_template('history.html')

    @app.route('/examples')
    def examples():
        return render_template('examples.html')

    @app.route('/analysis')
    def analysis():
        return render_template('analysis.html')

    @app.route('/guide')
    def guide():
        return render_template('guide.html')

    @app.route('/result')
    def result():
        return render_template('result.html')
        
    @app.route('/api/review', methods=['POST'])
    def review_essay():
        try:
            data = request.get_json()
            title = data.get('title', '')
            content = data.get('content', '')
            grade = data.get('grade', '')
            essay_type = data.get('type', '记叙文')  # 从请求中获取文章类型
            
            if not all([title, content, grade]):
                return jsonify({
                    'success': False,
                    'message': '请填写完整的作文信息'
                }), 400
                
            result = analyze_essay(title, content, grade)
            
            if result is None:
                return jsonify({
                    'success': False,
                    'message': '评阅失败，请稍后重试'
                }), 500
            
            # 保存评阅历史
            history = EssayHistory(
                title=title,
                content=content,
                grade=grade,
                total_score=result['total_score'],
                review_result=result,
                essay_type=essay_type,  # 确保设置文章类型
                is_example=result['total_score'] >= 88  # 88分以上自动标记为优秀范文
            )
            db.session.add(history)
            db.session.commit()
                
            return jsonify({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            print(f"Error in review_essay: {e}")
            return jsonify({
                'success': False,
                'message': '服务器错误'
            }), 500

    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.get_json()
            message = data.get('message', '')
            
            if not message:
                return jsonify({
                    'success': False,
                    'message': '请输入消息'
                }), 400
                
            response = chat_with_ai(message)
            
            return jsonify({
                'success': True,
                'data': response
            })
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return jsonify({
                'success': False,
                'message': '服务器错误'
            }), 500 

    @app.route('/example/<int:example_id>')
    def example_detail(example_id):
        try:
            example = EssayHistory.query.get_or_404(example_id)
            
            # 确保只能查看88分以上的作文
            if example.total_score < 88:
                return "范文不存在", 404
                
            return render_template('example_detail.html', example={
                'title': example.title,
                'grade': example.grade,
                'type': example.essay_type,
                'content': example.content,
                'analysis': example.review_result.get('overall_review', '')
            })
            
        except Exception as e:
            print(f"Error in example_detail: {e}")
            return "范文加载失败", 500

    @app.route('/api/history')
    def get_history():
        try:
            # 获取筛选参数
            grade = request.args.get('grade', 'all')
            time_range = request.args.get('time_range', 'all')
            
            # 构建查询
            query = EssayHistory.query
            
            if grade != 'all':
                query = query.filter_by(grade=grade)
                
            if time_range != 'all':
                if time_range == 'week':
                    days = 7
                elif time_range == 'month':
                    days = 30
                elif time_range == 'year':
                    days = 365
                    
                from datetime import timedelta
                cutoff = datetime.utcnow() - timedelta(days=days)
                query = query.filter(EssayHistory.created_at >= cutoff)
            
            # 按时间倒序排序
            histories = query.order_by(EssayHistory.created_at.desc()).all()
            
            return jsonify({
                'success': True,
                'data': [history.to_dict() for history in histories]
            })
            
        except Exception as e:
            print(f"Error in get_history: {e}")
            return jsonify({
                'success': False,
                'message': '获取历史记录失败'
            }), 500

    @app.route('/api/history/<int:history_id>', methods=['GET'])
    def get_history_detail(history_id):
        try:
            history = EssayHistory.query.get_or_404(history_id)
            
            # 构建返回数据
            data = {
                'title': history.title,
                'content': history.content,
                'grade': history.grade,
                'total_score': history.total_score,
                'created_at': history.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                **history.review_result  # 展开评阅结果
            }
            
            return jsonify({
                'success': True,
                'data': data
            })
            
        except Exception as e:
            print(f"Error in get_history_detail: {e}")
            return jsonify({
                'success': False,
                'message': '获取评阅结果失败'
            }), 500

    @app.route('/api/history/<int:history_id>', methods=['DELETE'])
    def delete_history(history_id):
        try:
            history = EssayHistory.query.get_or_404(history_id)
            db.session.delete(history)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': '删除成功'
            })
            
        except Exception as e:
            print(f"Error in delete_history: {e}")
            return jsonify({
                'success': False,
                'message': '删除失败'
            }), 500

    @app.route('/api/examples')
    def get_examples():
        try:
            # 获取筛选参数
            grade = request.args.get('grade', 'all')
            essay_type = request.args.get('type', 'all')
            
            # 构建查询
            query = EssayHistory.query.filter(
                EssayHistory.total_score >= 88  # 88分以上的作文
            )
            
            if grade != 'all':
                query = query.filter_by(grade=grade)
                
            if essay_type != 'all':
                query = query.filter_by(essay_type=essay_type)
            
            # 按分数降序排序
            examples = query.order_by(EssayHistory.total_score.desc()).all()
            
            return jsonify({
                'success': True,
                'data': [example.to_dict() for example in examples]
            })
            
        except Exception as e:
            print(f"Error in get_examples: {e}")
            return jsonify({
                'success': False,
                'message': '获取范文失败'
            }), 500

    @app.route('/api/analysis/stats')
    def get_analysis_stats():
        try:
            # 获取当前月份的开始日期
            now = datetime.utcnow()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # 计算各项统计数据
            monthly_count = EssayHistory.query.filter(
                EssayHistory.created_at >= month_start
            ).count()
            
            avg_score = db.session.query(
                func.avg(EssayHistory.total_score)
            ).scalar() or 0
            
            max_score = db.session.query(
                func.max(EssayHistory.total_score)
            ).scalar() or 0
            
            excellent_count = EssayHistory.query.filter(
                EssayHistory.total_score >= 88
            ).count()
            
            return jsonify({
                'success': True,
                'data': {
                    'monthly_count': monthly_count,
                    'avg_score': round(float(avg_score), 1),
                    'max_score': int(max_score),
                    'excellent_count': excellent_count
                }
            })
        except Exception as e:
            print(f"Error in get_analysis_stats: {e}")
            return jsonify({
                'success': False,
                'message': '获取统计数据失败'
            }), 500

    @app.route('/api/analysis/trend')
    def get_score_trend():
        try:
            time_range = request.args.get('range', 'week')
            
            # 确定时间范围
            now = datetime.utcnow()
            if time_range == 'week':
                start_date = now - timedelta(days=7)
                group_by = func.date(EssayHistory.created_at)
                date_format = '%Y-%m-%d'
            elif time_range == 'month':
                start_date = now - timedelta(days=30)
                group_by = func.date(EssayHistory.created_at)
                date_format = '%Y-%m-%d'
            else:  # year
                start_date = now - timedelta(days=365)
                group_by = func.date_format(EssayHistory.created_at, '%Y-%m')
                date_format = '%Y-%m'
            
            # 查询每天的平均分数
            scores = db.session.query(
                group_by.label('date'),
                func.avg(EssayHistory.total_score).label('score')
            ).filter(
                EssayHistory.created_at >= start_date
            ).group_by('date').all()
            
            # 格式化结果
            result = [
                {
                    'date': date.strftime(date_format) if isinstance(date, datetime) else date,
                    'score': round(float(score), 1)
                }
                for date, score in scores
            ]
            
            return jsonify({
                'success': True,
                'data': result
            })
        except Exception as e:
            print(f"Error in get_score_trend: {e}")
            return jsonify({
                'success': False,
                'message': '获取趋势数据失败'
            }), 500

    @app.route('/api/analysis/dimensions')
    def get_dimension_analysis():
        try:
            # 计算各维度的平均分数
            dimensions = ['内容立意', '结构布局', '语言表达', '书写规范']
            current_scores = []
            avg_scores = []
            
            for dimension in dimensions:
                # 获取最近一次评阅的分数
                latest = EssayHistory.query.order_by(
                    EssayHistory.created_at.desc()
                ).first()
                
                if latest:
                    for dim in latest.review_result['dimensions']:
                        if dim['name'] == dimension:
                            current_scores.append(dim['score'])
                            break
                else:
                    current_scores.append(0)
                
                # 计算历史平均分
                total = 0
                count = 0
                histories = EssayHistory.query.all()
                for history in histories:
                    for dim in history.review_result['dimensions']:
                        if dim['name'] == dimension:
                            total += dim['score']
                            count += 1
                            break
                
                avg_scores.append(round(total / count if count > 0 else 0, 1))
            
            return jsonify({
                'success': True,
                'data': {
                    'dimensions': dimensions,
                    'current_scores': current_scores,
                    'avg_scores': avg_scores
                }
            })
        except Exception as e:
            print(f"Error in get_dimension_analysis: {e}")
            return jsonify({
                'success': False,
                'message': '获取维度分析失败'
            }), 500