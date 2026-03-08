#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将健身计划添加到飞书日历
"""

import json
import requests
from datetime import datetime, timedelta

# 飞书API配置
BASE_URL = "https://open.feishu.cn/open-apis"

# 健身计划数据
fitness_plan = {
    "周一": {"type": "有氧", "duration": 40, "intensity": "中", "time": "20:30-21:30"},
    "周二": {"type": "力量", "duration": 45, "focus": "全身", "time": "20:30-21:30"},
    "周三": {"type": "休息", "duration": 0, "time": ""},
    "周四": {"type": "HIIT", "duration": 30, "intensity": "高", "time": "20:30-21:30"},
    "周五": {"type": "有氧", "duration": 40, "intensity": "中", "time": "20:30-21:30"},
    "周六": {"type": "力量", "duration": 45, "focus": "全身", "time": "16:00-18:00"},
    "周日": {"type": "休息", "duration": 0, "time": ""}
}

def create_calendar_event(day, workout, start_date):
    """创建日历事件"""
    
    # 计算日期
    day_map = {"周一": 0, "周二": 1, "周三": 2, "周四": 3, "周五": 4, "周六": 5, "周日": 6}
    target_date = start_date + timedelta(days=day_map[day])
    
    if workout["type"] == "休息":
        return None
    
    # 解析时间
    time_slot = workout.get("time", "20:30-21:30")
    if not time_slot:
        time_slot = "20:30-21:30"
    
    start_time, end_time = time_slot.split("-")
    
    # 构建事件时间
    start_datetime = target_date.strftime(f"%Y-%m-%dT{start_time}:00+08:00")
    end_datetime = target_date.strftime(f"%Y-%m-%dT{end_time}:00+08:00")
    
    # 构建事件内容
    title = f"健身 - {workout['type']}"
    
    if workout["type"] == "有氧":
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n强度：{workout['intensity']}\n\n加油！💪"
    elif workout["type"] == "力量":
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n重点：{workout.get('focus', '全身')}\n\n加油！💪"
    elif workout["type"] == "HIIT":
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n强度：{workout['intensity']}\n\n加油！💪"
    else:
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n\n加油！💪"
    
    return {
        "summary": title,
        "description": description,
        "start": {"date_time": start_datetime, "time_zone": "Asia/Shanghai"},
        "end": {"date_time": end_datetime, "time_zone": "Asia/Shanghai"},
        "reminders": [
            {"minutes": 30}  # 提前30分钟提醒
        ]
    }

def main():
    """主函数"""
    print("=" * 60)
    print("健身计划 - 飞书日历导入")
    print("=" * 60)
    
    # 从明天开始
    start_date = datetime.now().date() + timedelta(days=1)
    
    events = []
    for day, workout in fitness_plan.items():
        event = create_calendar_event(day, workout, start_date)
        if event:
            events.append((day, event))
    
    print(f"\n准备创建 {len(events)} 个健身日程：\n")
    
    for day, event in events:
        print(f"{day}: {event['summary']}")
        print(f"  时间: {event['start']['date_time']} - {event['end']['date_time']}")
        print(f"  内容: {event['description'][:50]}...")
        print()
    
    print("=" * 60)
    print("注意：需要通过飞书API创建日历事件")
    print("请确保已授权 calendar:calendar.event:create 权限")
    print("=" * 60)
    
    # 保存事件数据供后续使用
    output = {
        "created_at": datetime.now().isoformat(),
        "start_date": start_date.isoformat(),
        "events": [{"day": day, "event": event} for day, event in events]
    }
    
    with open("fitness_calendar_events.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n事件数据已保存到 fitness_calendar_events.json")
    print("可以通过飞书日历API批量导入这些事件")

if __name__ == "__main__":
    main()
