from flask import render_template, request, jsonify
from app.utils.ai_review import analyze_essay
from app.utils.ai_chat import chat_with_ai

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
        # 这里可以添加从数据库获取范文的逻辑
        # 现在先使用模拟数据
        example_data = {
            1: {
                "title": "春天的早晨",
                "grade": "高中",
                "type": "记叙文",
                "content": """
                清晨，第一缕阳光透过窗帘洒在书桌上，我推开窗，深深地呼吸着春天的气息。
                远处的山峦笼罩在薄薄的晨雾中，像是一幅水墨画。小区里的樱花树开得正艳，
                粉白的花瓣随风飘落，在空中划出优美的弧线。鸟儿在枝头欢快地啼叫，仿佛在
                歌颂这美好的春日。
                
                漫步在小区的林荫道上，我感受着春天的气息。嫩绿的草地上布满了晶莹的露珠，
                在阳光下闪闪发光。蒲公英的绒球随风摇曳，像是在跳一支优美的华尔兹。
                
                这样的春天，让人心旷神怡，充满希望。我站在这里，聆听着春天的声音，感受
                着生命的律动，内心充满了对未来的期待。
                """,
                "analysis": """
                这篇作文以细腻的笔触描绘了春天早晨的美景，通过视觉、听觉、嗅觉等多种感官的描写，
                生动地展现了春天的勃勃生机。文章结构清晰，语言优美，意境深远。
                
                亮点：
                1. 运用了丰富的修辞手法，如比喻、拟人等
                2. 多角度、多层次的细节描写
                3. 感情真挚自然，与景物描写完美融合
                
                写作技巧：
                1. 善于运用感官描写，让画面更加生动
                2. 注重细节刻画，突出春天的特征
                3. 情景交融，抒情自然不做作
                """
            },
            # 可以添加更多范文数据
        }
        
        example = example_data.get(example_id)
        if not example:
            return "范文不存在", 404
            
        return render_template('example_detail.html', example=example)