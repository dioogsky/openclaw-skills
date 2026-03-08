#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动创建飞书日历健身事件
使用用户已授权的权限
"""

import json
import requests
from datetime import datetime, timedelta

# 飞书API基础URL
BASE_URL = "https://open.feishu.cn/open-apis"

# 健身计划数据
fitness_plan = [
    {"day": "周一", "type": "有氧", "duration": 40, "intensity": "中", "time": "20:30-21:30", "day_offset": 0},
    {"day": "周二", "type": "力量", "duration": 45, "focus": "全身", "time": "20:30-21:30", "day_offset": 1},
    {"day": "周四", "type": "HIIT", "duration": 30, "intensity": "高", "time": "20:30-21:30", "day_offset": 3},
    {"day": "周五", "type": "有氧", "duration": 40, "intensity": "中", "time": "20:30-21:30", "day_offset": 4},
    {"day": "周六", "type": "力量", "duration": 45, "focus": "全身", "time": "16:00-18:00", "day_offset": 5},
]

def get_primary_calendar(access_token):
    """获取主日历ID"""
    url = f"{BASE_URL}/calendar/v4/calendars"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get("code") == 0:
            calendars = data.get("data", {}).get("calendar_list", [])
            for cal in calendars:
                if cal.get("is_primary"):
                    return cal.get("calendar_id")
            # 如果没有主日历，返回第一个
            if calendars:
                return calendars[0].get("calendar_id")
        return None
    except Exception as e:
        print(f"获取日历失败: {e}")
        return None

def create_event(access_token, calendar_id, workout, target_date):
    """创建日历事件"""
    url = f"{BASE_URL}/calendar/v4/calendars/{calendar_id}/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 解析时间
    start_time, end_time = workout["time"].split("-")
    start_datetime = target_date.strftime(f"%Y-%m-%dT{start_time}:00+08:00")
    end_datetime = target_date.strftime(f"%Y-%m-%dT{end_time}:00+08:00")
    
    # 构建描述
    if workout["type"] == "有氧":
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n强度：{workout['intensity']}"
    elif workout["type"] == "力量":
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n重点：{workout.get('focus', '全身')}"
    elif workout["type"] == "HIIT":
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n强度：{workout['intensity']}"
    else:
        description = f"{workout['type']}训练\n时长：{workout['duration']}分钟"
    
    event_data = {
        "summary": f"健身 - {workout['type']}",
        "description": description,
        "start": {
            "date_time": start_datetime,
            "time_zone": "Asia/Shanghai"
        },
        "end": {
            "date_time": end_datetime,
            "time_zone": "Asia/Shanghai"
        },
        "reminders": [
            {"minutes": 30}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=event_data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    """主函数"""
    print("=" * 60)
    print("飞书日历健身计划自动创建")
    print("=" * 60)
    
    # 从明天开始
    start_date = datetime.now().date() + timedelta(days=1)
    
    print("\n准备创建以下日程：")
    for workout in fitness_plan:
        target_date = start_date + timedelta(days=workout["day_offset"])
        print(f"\n{workout['day']} ({target_date})")
        print(f"  训练: {workout['type']}")
        print(f"  时间: {workout['time']}")
        print(f"  时长: {workout['duration']}分钟")
    
    print("\n" + "=" * 60)
    print("注意：需要通过飞书授权获取access_token")
    print("请确保已开通 calendar:calendar.event:create 权限")
    print("=" * 60)

if __name__ == "__main__":
    main()
