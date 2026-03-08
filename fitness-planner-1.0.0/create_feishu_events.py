#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书日历事件创建工具
"""

import json
import requests
from datetime import datetime, timedelta

class FeishuCalendar:
    def __init__(self, access_token=None):
        self.base_url = "https://open.feishu.cn/open-apis"
        self.access_token = access_token
        
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
    
    def get_calendars(self):
        """获取日历列表"""
        url = f"{self.base_url}/calendar/v4/calendars"
        try:
            response = requests.get(url, headers=self.get_headers())
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def create_event(self, calendar_id, event_data):
        """创建日历事件"""
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events"
        try:
            response = requests.post(url, headers=self.get_headers(), json=event_data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def create_fitness_events():
    """创建健身计划日历事件"""
    
    # 健身计划
    fitness_plan = [
        {"day": "周一", "type": "有氧", "duration": 40, "intensity": "中", "time": "20:30-21:30", "day_offset": 0},
        {"day": "周二", "type": "力量", "duration": 45, "focus": "全身", "time": "20:30-21:30", "day_offset": 1},
        {"day": "周四", "type": "HIIT", "duration": 30, "intensity": "高", "time": "20:30-21:30", "day_offset": 3},
        {"day": "周五", "type": "有氧", "duration": 40, "intensity": "中", "time": "20:30-21:30", "day_offset": 4},
        {"day": "周六", "type": "力量", "duration": 45, "focus": "全身", "time": "16:00-18:00", "day_offset": 5},
    ]
    
    # 从明天开始
    start_date = datetime.now().date() + timedelta(days=1)
    
    events = []
    for workout in fitness_plan:
        target_date = start_date + timedelta(days=workout["day_offset"])
        
        # 解析时间
        start_time, end_time = workout["time"].split("-")
        
        start_datetime = target_date.strftime(f"%Y-%m-%dT{start_time}:00+08:00")
        end_datetime = target_date.strftime(f"%Y-%m-%dT{end_time}:00+08:00")
        
        # 构建事件
        if workout["type"] == "有氧":
            description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n强度：{workout['intensity']}"
        elif workout["type"] == "力量":
            description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n重点：{workout.get('focus', '全身')}"
        elif workout["type"] == "HIIT":
            description = f"{workout['type']}训练\n时长：{workout['duration']}分钟\n强度：{workout['intensity']}"
        else:
            description = f"{workout['type']}训练\n时长：{workout['duration']}分钟"
        
        event = {
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
        
        events.append({
            "day": workout["day"],
            "date": target_date.isoformat(),
            "event": event
        })
    
    return events

if __name__ == "__main__":
    events = create_fitness_events()
    
    print("=" * 60)
    print("健身计划 - 飞书日历事件")
    print("=" * 60)
    
    for item in events:
        print(f"\n{item['day']} ({item['date']})")
        print(f"  标题: {item['event']['summary']}")
        print(f"  时间: {item['event']['start']['date_time']} - {item['event']['end']['date_time']}")
        print(f"  内容: {item['event']['description']}")
    
    # 保存到文件
    with open("fitness_events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("事件数据已保存到 fitness_events.json")
    print("=" * 60)
