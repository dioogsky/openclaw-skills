#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量创建飞书日历健身事件
"""

import requests
import json
from datetime import datetime, timedelta

# 配置
BASE_URL = "https://open.feishu.cn/open-apis"
ACCESS_TOKEN = "u-eUEHImT9p018JK2U9WhprHk4nRx4khWXN8ayURE00alR"
CALENDAR_ID = "feishu.cn_oGM38d2ST4Uk9Lk8ep6Ezb@group.calendar.feishu.cn"

# 健身计划（周一周四休息）
fitness_plan = [
    {"day": "周二", "type": "力量", "duration": 45, "focus": "全身", "time": "20:30-21:30", "day_offset": 1},
    {"day": "周三", "type": "有氧", "duration": 40, "intensity": "中", "time": "20:30-21:30", "day_offset": 2},
    {"day": "周五", "type": "力量", "duration": 45, "focus": "全身", "time": "20:30-21:30", "day_offset": 4},
    {"day": "周六", "type": "有氧", "duration": 40, "intensity": "中", "time": "16:00-18:00", "day_offset": 5},
    {"day": "周日", "type": "HIIT", "duration": 30, "intensity": "高", "time": "16:00-18:00", "day_offset": 6},
]

def create_event(workout, target_date):
    """创建单个日历事件"""
    url = f"{BASE_URL}/calendar/v4/calendars/{CALENDAR_ID}/events"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 解析时间
    start_time, end_time = workout["time"].split("-")
    
    # 构建时间字符串
    start_datetime = target_date.strftime(f"%Y-%m-%dT{start_time}:00")
    end_datetime = target_date.strftime(f"%Y-%m-%dT{end_time}:00")
    
    # 构建描述
    if workout["type"] == "有氧":
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n强度：{workout['intensity']}"
    elif workout["type"] == "力量":
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n重点：{workout.get('focus', '全身')}"
    elif workout["type"] == "HIIT":
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n强度：{workout['intensity']}"
    else:
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟"
    
    # 构建请求体
    event_data = {
        "summary": f"健身 - {workout['type']}",
        "description": description,
        "start_time": {
            "timestamp": str(int(datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S").timestamp())),
            "timezone": "Asia/Shanghai"
        },
        "end_time": {
            "timestamp": str(int(datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S").timestamp())),
            "timezone": "Asia/Shanghai"
        },
        "reminders": [
            {
                "minutes": 30
            }
        ],
        "recurrence": "FREQ=WEEKLY;INTERVAL=1"  # 每周重复
    }
    
    try:
        response = requests.post(url, headers=headers, json=event_data)
        result = response.json()
        
        if result.get("code") == 0:
            return True, "创建成功"
        else:
            return False, result.get("msg", "未知错误")
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    print("=" * 60)
    print("Batch Create Fitness Events")
    print("=" * 60)
    
    # 从明天开始
    start_date = datetime.now().date() + timedelta(days=1)
    
    success_count = 0
    results = []
    
    for workout in fitness_plan:
        target_date = start_date + timedelta(days=workout["day_offset"])
        
        print(f"\nCreating {workout['day']} ({target_date}) event...")
        print(f"  Workout: {workout['type']}")
        print(f"  Time: {workout['time']}")
        
        success, msg = create_event(workout, target_date)
        
        if success:
            print(f"  [OK] {msg}")
            success_count += 1
        else:
            print(f"  [ERROR] {msg}")
        
        results.append({
            "day": workout["day"],
            "date": target_date.isoformat(),
            "type": workout["type"],
            "success": success,
            "message": msg
        })
    
    print("\n" + "=" * 60)
    print(f"创建完成: {success_count}/{len(fitness_plan)} 个事件")
    print("=" * 60)
    
    # 保存结果
    with open("calendar_create_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n详细结果已保存到 calendar_create_results.json")

if __name__ == "__main__":
    main()
