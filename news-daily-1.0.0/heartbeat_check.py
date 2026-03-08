import json
import os
from datetime import datetime
import subprocess

STATE_FILE = r"C:\Users\MyPC\.openclaw\workspace\memory\news-daily-state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "lastMorningPushChina": None,
        "lastMorningPushUS": None,
        "lastEveningPushChina": None,
        "lastEveningPushUS": None,
        "today": datetime.now().strftime("%Y-%m-%d")
    }

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def should_push(state, key, hour):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    # 新的一天，重置状态
    if state.get("today") != today:
        state["today"] = today
        state["lastMorningPushChina"] = None
        state["lastMorningPushUS"] = None
        state["lastEveningPushChina"] = None
        state["lastEveningPushUS"] = None
        save_state(state)
    
    # 检查是否已过指定时间且今天未推送
    if now.hour >= hour:
        if state.get(key) != today:
            return True
    return False

def push_news(region):
    """推送新闻到群聊"""
    try:
        # 这里调用新闻生成和推送逻辑
        # 暂时使用现有的news_daily.py
        result = subprocess.run(
            ["python", "C:/Users/MyPC/.openclaw/workspace/skills/news-daily-1.0.0/news_daily.py", "push", region],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[{datetime.now()}] 推送失败: {e}")
        return False

def main():
    state = load_state()
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    pushed = []
    
    # 早上 8:00 中国新闻
    if should_push(state, "lastMorningPushChina", 8) and now.hour == 8:
        print(f"[{now}] 推送早上中国AI新闻...")
        if push_news("china"):
            state["lastMorningPushChina"] = today
            pushed.append("早上-中国")
    
    # 早上 8:05 美国新闻
    if should_push(state, "lastMorningPushUS", 8) and now.hour == 8 and now.minute >= 5:
        print(f"[{now}] 推送早上美国AI新闻...")
        if push_news("us"):
            state["lastMorningPushUS"] = today
            pushed.append("早上-美国")
    
    # 晚上 20:00 中国新闻
    if should_push(state, "lastEveningPushChina", 20) and now.hour == 20:
        print(f"[{now}] 推送晚上中国AI新闻...")
        if push_news("china"):
            state["lastEveningPushChina"] = today
            pushed.append("晚上-中国")
    
    # 晚上 20:05 美国新闻
    if should_push(state, "lastEveningPushUS", 20) and now.hour == 20 and now.minute >= 5:
        print(f"[{now}] 推送晚上美国AI新闻...")
        if push_news("us"):
            state["lastEveningPushUS"] = today
            pushed.append("晚上-美国")
    
    if pushed:
        save_state(state)
        print(f"[{now}] 已推送: {', '.join(pushed)}")
    else:
        print(f"[{now}] 暂无需要推送的新闻")

if __name__ == "__main__":
    main()
