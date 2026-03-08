#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除之前创建的健身日程
"""

import requests
import json

# 配置
BASE_URL = "https://open.feishu.cn/open-apis"
ACCESS_TOKEN = "u-eUEHImT9p018JK2U9WhprHk4nRx4khWXN8ayURE00alR"
CALENDAR_ID = "feishu.cn_oGM38d2ST4Uk9Lk8ep6Ezb@group.calendar.feishu.cn"

def list_events():
    """获取日历中的事件列表"""
    url = f"{BASE_URL}/calendar/v4/calendars/{CALENDAR_ID}/events"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    params = {
        "page_size": 100
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("items", [])
        else:
            print(f"[ERROR] Failed to list events: {result.get('msg')}")
            return []
    except Exception as e:
        print(f"[ERROR] {e}")
        return []

def delete_event(event_id):
    """删除单个事件"""
    url = f"{BASE_URL}/calendar/v4/calendars/{CALENDAR_ID}/events/{event_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(url, headers=headers)
        result = response.json()
        
        if result.get("code") == 0:
            return True, "Deleted"
        else:
            return False, result.get("msg", "Unknown error")
    except Exception as e:
        return False, str(e)

def main():
    """主函数"""
    print("=" * 60)
    print("Delete Fitness Events")
    print("=" * 60)
    
    # 获取事件列表
    print("\nFetching events...")
    events = list_events()
    
    # 过滤出健身相关的事件
    fitness_events = [e for e in events if "健身" in e.get("summary", "")]
    
    print(f"Found {len(fitness_events)} fitness events")
    
    # 删除事件
    success_count = 0
    for event in fitness_events:
        event_id = event.get("event_id")
        summary = event.get("summary", "Unknown")
        
        print(f"\nDeleting: {summary}...")
        success, msg = delete_event(event_id)
        
        if success:
            print(f"  [OK] Deleted")
            success_count += 1
        else:
            print(f"  [ERROR] {msg}")
    
    print("\n" + "=" * 60)
    print(f"Deleted: {success_count}/{len(fitness_events)} events")
    print("=" * 60)

if __name__ == "__main__":
    main()
