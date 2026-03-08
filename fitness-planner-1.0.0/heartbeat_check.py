#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健身计划自动提醒 - Heartbeat 检查脚本
每天早上 9:00 预告今日计划
训练前 30 分钟提醒（工作日 20:00，周末 15:30）
"""

import os
import sys
import json
from datetime import datetime, timedelta

# 添加技能目录到路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)

from fitness_planner import load_data

# 状态文件
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "memory", "fitness-reminder-state.json")

def load_state():
    """加载提醒状态"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_morning_reminder": None,
        "last_workout_reminder": None,
        "last_date": None
    }

def save_state(state):
    """保存提醒状态"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def should_send_morning_reminder(now, state):
    """检查是否应该发送早上提醒（9:00）"""
    today_str = now.strftime("%Y-%m-%d")
    
    # 如果今天已经提醒过，不再提醒
    if state.get("last_morning_reminder") == today_str:
        return False
    
    # 9:00-9:30 之间发送
    if now.hour == 9 and now.minute < 30:
        return True
    
    return False

def should_send_workout_reminder(now, state, is_weekend):
    """检查是否应该发送训练前提醒"""
    today_str = now.strftime("%Y-%m-%d")
    
    # 如果今天已经提醒过，不再提醒
    if state.get("last_workout_reminder") == today_str:
        return False
    
    if is_weekend:
        # 周末 15:30-16:00 之间发送
        if now.hour == 15 and now.minute >= 30:
            return True
    else:
        # 工作日 20:00-20:30 之间发送
        if now.hour == 20 and now.minute < 30:
            return True
    
    return False

def get_today_plan():
    """获取今日训练计划"""
    data = load_data()
    
    if not data.get("plan"):
        return None
    
    weekday = datetime.now().weekday()
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    today_name = days[weekday]
    
    plan = data["plan"]
    workout_time = plan.get("workout_time", "未设置")
    weekend_time = plan.get("weekend_time", "未设置")
    
    is_weekend = weekday >= 5
    time_slot = weekend_time if is_weekend else workout_time
    
    for item in plan["weekly_schedule"]:
        if item["day"] == today_name:
            return {
                "day": today_name,
                "is_weekend": is_weekend,
                "time_slot": time_slot,
                "plan": item
            }
    
    return None

def generate_morning_message(today_info):
    """生成早上提醒消息"""
    plan = today_info["plan"]
    day = today_info["day"]
    time_slot = today_info["time_slot"]
    
    if plan["duration"] == 0:
        return f"""🌅 早上好！今天是 {day}，休息日！

💡 建议：
• 适当拉伸放松
• 保证充足睡眠
• 为明天的训练做准备

明天见！💪"""
    
    workout_type = plan["type"]
    duration = plan["duration"]
    intensity = plan.get("intensity", "")
    focus = plan.get("focus", "")
    
    msg = f"""🌅 早上好！今日健身计划

📅 {day} | {workout_type}训练
⏰ 时间：{time_slot}
⏱️ 时长：{duration}分钟"""
    
    if intensity:
        msg += f"\n🔥 强度：{intensity}"
    if focus:
        msg += f"\n🎯 重点：{focus}"
    
    msg += "\n\n💪 记得按时完成训练！"
    
    return msg

def generate_workout_reminder(today_info):
    """生成训练前提醒消息"""
    plan = today_info["plan"]
    time_slot = today_info["time_slot"]
    
    if plan["duration"] == 0:
        return None  # 休息日不提醒
    
    workout_type = plan["type"]
    duration = plan["duration"]
    
    return f"""🔔 训练时间到！

⏰ 还有30分钟开始训练
📍 时间：{time_slot}
🏋️ 内容：{workout_type} - {duration}分钟

💪 准备好了吗？加油！"""

def main():
    now = datetime.now()
    state = load_state()
    
    # 检查是否需要重置（新的一天）
    today_str = now.strftime("%Y-%m-%d")
    if state.get("last_date") != today_str:
        state["last_morning_reminder"] = None
        state["last_workout_reminder"] = None
        state["last_date"] = today_str
        save_state(state)
    
    # 获取今日计划
    today_info = get_today_plan()
    if not today_info:
        print("[ERROR] 没有找到健身计划")
        return
    
    reminders_sent = []
    
    # 检查早上提醒（9:00）
    if should_send_morning_reminder(now, state):
        msg = generate_morning_message(today_info)
        print("[MORNING_REMINDER]")
        print(msg)
        state["last_morning_reminder"] = today_str
        reminders_sent.append("morning")
    
    # 检查训练前提醒
    if should_send_workout_reminder(now, state, today_info["is_weekend"]):
        msg = generate_workout_reminder(today_info)
        if msg:  # 只有训练日才提醒
            print("[WORKOUT_REMINDER]")
            print(msg)
            state["last_workout_reminder"] = today_str
            reminders_sent.append("workout")
    
    # 保存状态
    if reminders_sent:
        save_state(state)
        print(f"\n[OK] 已发送提醒: {', '.join(reminders_sent)}")
    else:
        print("[SKIP] 暂无需要发送的提醒")

if __name__ == "__main__":
    main()
