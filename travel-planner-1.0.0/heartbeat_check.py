import json
import os
from datetime import datetime
import subprocess

STATE_FILE = r"C:\Users\MyPC\.openclaw\workspace\memory\travel-planner-state.json"
SCRIPT_PATH = r"C:\Users\MyPC\.openclaw\workspace\skills\travel-planner-1.0.0\travel_planner.py"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def should_run_daily():
    """检查是否应该运行每日更新"""
    now = datetime.now()
    state = load_state()
    last_daily = state.get('reports', {}).get('last_daily_update')
    today = now.strftime("%Y-%m-%d")
    
    # 每天 10:00 后执行
    if now.hour >= 10:
        if last_daily != today:
            return True
    return False

def should_run_weekly():
    """检查是否应该运行每周报告"""
    now = datetime.now()
    state = load_state()
    last_weekly = state.get('reports', {}).get('last_weekly_report')
    
    # 每周一 09:00 后执行
    if now.weekday() == 0 and now.hour >= 9:  # Monday = 0
        week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
        if last_weekly != week_start:
            return True
    return False

def run_daily():
    """运行每日更新"""
    try:
        result = subprocess.run(
            ["python", SCRIPT_PATH, "daily"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        print(f"[{datetime.now()}] 旅行规划每日更新完成")
        return result.stdout
    except Exception as e:
        print(f"[{datetime.now()}] 每日更新失败: {e}")
        return None

def run_weekly():
    """运行每周报告"""
    try:
        result = subprocess.run(
            ["python", SCRIPT_PATH, "weekly"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        print(f"[{datetime.now()}] 旅行规划周报完成")
        return result.stdout
    except Exception as e:
        print(f"[{datetime.now()}] 周报失败: {e}")
        return None

def main():
    from datetime import timedelta
    
    print(f"[{datetime.now()}] 检查旅行规划任务...")
    
    # 检查每日更新
    if should_run_daily():
        print("执行每日更新...")
        output = run_daily()
        if output:
            print(output[:500] + "..." if len(output) > 500 else output)
    else:
        print("今日已更新或未到时间")
    
    # 检查每周报告
    if should_run_weekly():
        print("执行每周报告...")
        output = run_weekly()
        if output:
            print(output[:500] + "..." if len(output) > 500 else output)
    else:
        print("本周已报告或未到时间")

if __name__ == "__main__":
    main()
