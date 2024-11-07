import requests
import json
import re

def get_access_token():
    """获取百度AI接口的access_token"""
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=r5B0INu5jWFYSH1U15ZvwwsI&client_secret=f4jHr6EpE1DbsX0vjuNGGEuMxdVX3pSn"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json().get("access_token")

def analyze_essay(title, content, grade):
    """分析作文内容"""
    access_token = get_access_token()
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/yi_34b_chat?access_token={access_token}"
    
    # 构建评阅提示词
    prompt = f"""你现在是一个专业的作文评阅老师，请对这篇作文进行详细的评分和点评。请给出深入的分析和具体的建议。

作文信息：
标题：{title}
年级：{grade}
内容：{content}

请按照以下维度进行评分（总分100分）并给出详细评语：
1. 内容立意（20分）：评价主题把握程度、思想深度、创新性
2. 结构布局（20分）：评价文章结构是否清晰，段落衔接和过渡是否自然
3. 语言表达（30分）：评价用词是否准确，句式是否多样，语言是否生动
4. 书写规范（30分）：评价标点符号使用、错别字检查、格式规范

同时请分析：
1. 文章的3-5个精彩句子，并说明其写作特点和表达效果
2. 文章的5-8个亮点，并详细说明
3. 5-8条具体的改进建议，包括修改示例
4. 总体评价（300字以上）

请严格按照以下JSON格式返回结果，不要包含任何注释：
{{
    "total_score": 85,
    "dimensions": [
        {{"name": "内容立意", "score": 17, "comment": "主题鲜明，思想深度有待加强，对xxx的描写富有新意...（至少100字）"}},
        {{"name": "结构布局", "score": 16, "comment": "层次较为分明，过渡自然，但xxx部分的衔接需要加强...（至少100字）"}},
        {{"name": "语言表达", "score": 25, "comment": "用词准确，句式较为丰富，在xxx处的描写尤为生动...（至少100字）"}},
        {{"name": "书写规范", "score": 27, "comment": "标点使用规范，有少量错别字，建议注意xxx...（至少100字）"}}
    ],
    "excellent_sentences": [
        {{
            "sentence": "这是一个精彩的句子",
            "analysis": "运用了xxx的写作手法，通过xxx的描写，生动地表现了xxx...（至少50字）"
        }}
    ],
    "highlights": [
        {{
            "point": "亮点摘要",
            "detail": "详细说明这个亮点的具体表现和效果...（至少50字）"
        }}
    ],
    "suggestions": [
        {{
            "issue": "需要改进的问题",
            "solution": "具体的改进建议和修改示例...（至少50字）"
        }}
    ],
    "overall_review": "整体评价，包括文章的总体特点、写作水平、情感表达等方面的详细分析...（至少300字）"
}}

注意：
1. 所有评语和分析都要具体详实，避免空泛
2. 每个维度的评语至少100字
3. 每个分析点至少50字
4. 总评至少300字
5. 返回的JSON中不要包含任何注释或说明文字"""

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response_json = response.json()
        
        if 'result' not in response_json:
            print("API response error:", response_json)
            return None
            
        result = response_json['result']
        print("Raw AI response:", result)  # 打印原始响应以便调试
        
        # 尝试从响应中提取JSON
        review_result = extract_json_from_text(result)
        if not review_result:
            print("Failed to extract JSON from response")
            return None
            
        # 验证返回的数据结构是否完整
        required_fields = ['total_score', 'dimensions', 'highlights', 'suggestions']
        if not all(field in review_result for field in required_fields):
            print("Missing required fields in result:", review_result)
            return None
            
        # 确保 dimensions 是数组格式
        if not isinstance(review_result['dimensions'], list):
            # 如果不是数组，尝试转换
            try:
                dimensions = []
                for key, value in review_result['dimensions'].items():
                    # 从字符串中提取分数
                    score = int(''.join(filter(str.isdigit, value.split('（')[0])))
                    # 提取评语
                    comment = value.split('（')[1].rstrip('）') if '（' in value else value
                    dimensions.append({
                        'name': key.replace('_', ' '),
                        'score': score,
                        'comment': comment
                    })
                review_result['dimensions'] = dimensions
            except Exception as e:
                print(f"Error converting dimensions: {e}")
                return None
            
        return review_result
        
    except Exception as e:
        print(f"Error in analyze_essay: {e}")
        return None

def extract_json_from_text(text):
    """从文本中提取JSON字符串"""
    try:
        # 首先尝试直接解析
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            # 使用正则表达式查找 { 和 } 之间的内容
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
        except Exception as e:
            print(f"Error extracting JSON: {e}")
    return None