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
    
    # 构建评阅提示词，使用三重引号和转义字符
    prompt = f"""你现在是一个严格的作文评阅老师，请根据以下作文内容进行客观、公正的评分和详细点评。请仔细阅读作文内容，根据实际水平给出合理的分数，避免给出重复或固定的分数。每篇作文的得分都应该根据其实际表现来决定。

作文信息：
标题：{title}
年级：{grade}
内容：{content}

评分标准：
1. 内容立意（20分）
- 优秀(17-20分)：主题突出，思想深刻，见解独到
- 良好(13-16分)：主题明确，思想健康，有一定见解
- 一般(9-12分)：主题基本明确，思想较浅显
- 不足(0-8分)：主题不明，思想混乱或偏离题意

2. 结构布局（20分）
- 优秀(17-20分)：结构严谨，层次分明，过渡自然
- 良好(13-16分)：结构完整，层次清晰，过渡较好
- 一般(9-12分)：结构基本完整，层次尚可
- 不足(0-8分)：结构混乱，缺少条理

3. 语言表达（30分）
- 优秀(25-30分)：语言生动，修辞恰当，句式丰富
- 良好(19-24分)：语言通顺，用词准确，句式多样
- 一般(13-18分)：语言基本通顺，用词基本准确
- 不足(0-12分)：语言不通，用词不当，病句较多

4. 书写规范（30分）
- 优秀(25-30分)：标点正确，几乎无错别字，格式规范
- 良好(19-24分)：标点基本正确，错别字较少，格式基本规范
- 一般(13-18分)：有一些标点错误和错别字
- 不足(0-12分)：标点混乱，错别字较多，格式不规范

重要提示：
1. 请仔细阅读作文内容，根据实际水平给出分数
2. 不同作文的分数应该有所区别，避免给出相同的分数
3. 评分要客观公正，体现作文之间的水平差异
4. 同等级作文也要有细微的分数区分
5. 总分和各项得分都要根据具体内容来定，不要给出固定分数
6. 评语要具体详实，针对该作文的实际特点
7. 优点和不足都要具体指出，不要笼统评价
8. 严格按照评分标准的分数区间给分，不要超出范围
9. 总分应该是各维度得分的总和

请严格按照以下JSON格式返回评阅结果（注意：分数必须根据实际内容评定，避免重复）：

{{
    "total_score": 根据四个维度的得分总和计算,
    "dimensions": [
        {{
            "name": "内容立意",
            "score": 根据实际水平在0-20分之间评定,
            "comment": "详细说明该维度的得分理由，包括优点和不足，至少100字"
        }},
        {{
            "name": "结构布局",
            "score": 根据实际水平在0-20分之间评定,
            "comment": "详细说明该维度的得分理由，包括优点和不足，至少100字"
        }},
        {{
            "name": "语言表达",
            "score": 根据实际水平在0-30分之间评定,
            "comment": "详细说明该维度的得分理由，包括优点和不足，至少100字"
        }},
        {{
            "name": "书写规范",
            "score": 根据实际水平在0-30分之间评定,
            "comment": "详细说明该维度的得分理由，包括优点和不足，至少100字"
        }}
    ],
    "excellent_sentences": [
        {{
            "sentence": "从文中选取的精彩句子",
            "analysis": "分析这句话的写作特点和表达效果，至少50字"
        }}
    ],
    "highlights": [
        {{
            "point": "作文的亮点",
            "detail": "详细说明这个亮点的具体表现，至少50字"
        }}
    ],
    "suggestions": [
        {{
            "issue": "需要改进的问题",
            "solution": "具体的改进建议和修改示例，至少50字"
        }}
    ],
    "overall_review": "整体评价，包括总体水平、特色亮点、改进方向等，至少300字"
}}"""

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
        print("Raw AI response:", result)
        
        # 尝试从响应中提取JSON
        review_result = extract_json_from_text(result)
        if not review_result:
            print("Failed to extract JSON from response")
            return None
            
        # 验证和清理数据
        if 'overall_review' in review_result:
            # 确保 overall_review 是一个完整的字符串
            review_result['overall_review'] = review_result['overall_review'].strip()
            if not review_result['overall_review'].endswith('"'):
                review_result['overall_review'] = review_result['overall_review'].split('\n')[0]
        
        # 验证返回的数据结构是否完整
        required_fields = ['total_score', 'dimensions', 'highlights', 'suggestions']
        if not all(field in review_result for field in required_fields):
            print("Missing required fields in result:", review_result)
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
            # 使用正则表达式查找 { 和 } 之间的内容，并确保 JSON 格式正确
            json_match = re.search(r'\{.*?\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                # 检查并修复常见的 JSON 格式问题
                json_str = json_str.strip()
                # 确保字符串正确结束
                if not json_str.endswith('}'):
                    json_str += '}'
                # 修复缺少引号的问题
                json_str = re.sub(r'([{,]\s*)(\w+)(:)', r'\1"\2"\3', json_str)
                # 修复多余的逗号
                json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
                # 修复未闭合的字符串
                json_str = re.sub(r'([^"])"([^"]*?)$', r'\1"\2"', json_str)
                
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    print(f"Error parsing fixed JSON: {e}")
                    print("Fixed JSON string:", json_str)
                    
                    # 如果还是失败，尝试更激进的修复
                    try:
                        # 移除所有换行符和多余的空格
                        json_str = ' '.join(json_str.split())
                        # 确保所有字段都有引号
                        json_str = re.sub(r'([{,]\s*)([^"\s]+)(\s*:)', r'\1"\2"\3', json_str)
                        # 确保所有值都有引号（除了数字和布尔值）
                        json_str = re.sub(r':\s*([^"{}\[\],\s][^,}\]]*?)([,}\]])', r': "\1"\2', json_str)
                        return json.loads(json_str)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing aggressively fixed JSON: {e}")
                        return None
        except Exception as e:
            print(f"Error extracting JSON: {e}")
    return None