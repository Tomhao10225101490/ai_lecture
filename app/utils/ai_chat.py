import requests
import json

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

def chat_with_ai(message):
    """与AI助手对话"""
    access_token = get_access_token()
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/yi_34b_chat?access_token={access_token}"
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    })
    
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    
    try:
        response_json = response.json()
        result = response_json.get("result", "抱歉,我现在无法回答这个问题。")
        return result
    except Exception as e:
        print(f"Error in chat_with_ai: {e}")
        return "抱歉,发生了一些错误。" 