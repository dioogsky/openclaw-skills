#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schedule Manager - 通用日程管理工具
支持健身、工作、学习等各类日程的管理和提醒
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid

# 配置
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SKILL_DIR, "data")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
SCHEDULE_FILE = os.path.join(DATA_DIR, "schedule.json")

# 默认配置
DEFAULT_CONFIG = {
    "default_reminder": 30,
    "feishu_calendar_id": "",
    "categories": {
        "workout": {"name": "健身", "color": "blue", "icon": "[W]"},
        "work": {"name": "工作", "color": "red", "icon": "[Wo]"},
        "study": {"name": "学习", "color": "green", "icon": "[S]"},
        "meeting": {"name": "会议", "color": "orange", "icon": "[M]"},
        "personal": {"name": "个人", "color": "purple", "icon": "[P]"},
        "other": {"name": "其他", "color": "gray", "icon": "[O]"}
    }
}

class ScheduleManager:
    """日程管理器"""
    
    def __init__(self):
        self._ensure_dirs()
        self.config = self._load_config()
        self.schedule = self._load_schedule()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        os.makedirs(DATA_DIR, exist_ok=True)
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return DEFAULT_CONFIG.copy()
    
    def _save_config(self):
        """保存配置"""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def _load_schedule(self) -> List[Dict]:
        """加载日程数据"""
        if os.path.exists(SCHEDULE_FILE):
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _save_schedule(self):
        """保存日程数据"""
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.schedule, f, ensure_ascii=False, indent=2)
    
    def create_event(self, name: str, event_type: str, date: str, 
                     time_slot: str, description: str = "",
                     repeat: str = "none", reminder: int = None) -> Dict:
        """创建日程"""
        if reminder is None:
            reminder = self.config.get("default_reminder", 30)
        
        event = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "type": event_type,
            "date": date,
            "time": time_slot,
            "description": description,
            "repeat": repeat,
            "reminder": reminder,
            "created_at": datetime.now().isoformat(),
            "completed": False
        }
        
        self.schedule.append(event)
        self._save_schedule()
        
        return event
    
    def list_events(self, event_type: str = None, date: str = None) -> List[Dict]:
        """列出日程"""
        events = self.schedule
        
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        
        if date:
            events = [e for e in events if e["date"] == date]
        
        # 按日期排序
        events.sort(key=lambda x: x["date"])
        
        return events
    
    def get_today_events(self) -> List[Dict]:
        """获取今日日程"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.list_events(date=today)
    
    def delete_event(self, event_id: str) -> bool:
        """删除日程"""
        for i, event in enumerate(self.schedule):
            if event["id"] == event_id:
                self.schedule.pop(i)
                self._save_schedule()
                return True
        return False
    
    def complete_event(self, event_id: str) -> bool:
        """标记日程完成"""
        for event in self.schedule:
            if event["id"] == event_id:
                event["completed"] = True
                event["completed_at"] = datetime.now().isoformat()
                self._save_schedule()
                return True
        return False
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = len(self.schedule)
        completed = len([e for e in self.schedule if e.get("completed")])
        
        # 按类型统计
        type_stats = {}
        for event in self.schedule:
            t = event["type"]
            if t not in type_stats:
                type_stats[t] = {"total": 0, "completed": 0}
            type_stats[t]["total"] += 1
            if event.get("completed"):
                type_stats[t]["completed"] += 1
        
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
            "by_type": type_stats
        }
    
    def export_to_feishu_format(self) -> List[Dict]:
        """导出为飞书日历格式"""
        events = []
        
        for event in self.schedule:
            start_time, end_time = event["time"].split("-")
            date = event["date"]
            
            feishu_event = {
                "summary": event["name"],
                "description": event["description"],
                "start_time": {
                    "timestamp": str(int(datetime.strptime(f"{date}T{start_time}:00", "%Y-%m-%dT%H:%M:%S").timestamp())),
                    "timezone": "Asia/Shanghai"
                },
                "end_time": {
                    "timestamp": str(int(datetime.strptime(f"{date}T{end_time}:00", "%Y-%m-%dT%H:%M:%S").timestamp())),
                    "timezone": "Asia/Shanghai"
                },
                "reminders": [{"minutes": event["reminder"]}],
                "recurrence": f"FREQ={event['repeat'].upper()};INTERVAL=1" if event["repeat"] != "none" else None
            }
            
            events.append(feishu_event)
        
        return events


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Schedule Manager - 通用日程管理")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    manager = ScheduleManager()
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建日程")
    create_parser.add_argument("--name", required=True, help="日程名称")
    create_parser.add_argument("--type", required=True, 
                              choices=["workout", "work", "study", "meeting", "personal", "other"],
                              help="日程类型")
    create_parser.add_argument("--date", required=True, help="日期 (YYYY-MM-DD)")
    create_parser.add_argument("--time", required=True, help="时间 (HH:MM-HH:MM)")
    create_parser.add_argument("--desc", default="", help="描述")
    create_parser.add_argument("--repeat", default="none", 
                              choices=["none", "daily", "weekly", "monthly"],
                              help="重复选项")
    create_parser.add_argument("--reminder", type=int, help="提醒时间（分钟）")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出日程")
    list_parser.add_argument("--type", help="按类型筛选")
    list_parser.add_argument("--date", help="按日期筛选")
    
    # today 命令
    subparsers.add_parser("today", help="查看今日日程")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除日程")
    delete_parser.add_argument("--id", required=True, help="日程ID")
    
    # complete 命令
    complete_parser = subparsers.add_parser("complete", help="标记完成")
    complete_parser.add_argument("--id", required=True, help="日程ID")
    
    # stats 命令
    subparsers.add_parser("stats", help="查看统计")
    
    # export 命令
    subparsers.add_parser("export", help="导出飞书格式")
    
    args = parser.parse_args()
    
    if args.command == "create":
        event = manager.create_event(
            name=args.name,
            event_type=args.type,
            date=args.date,
            time_slot=args.time,
            description=args.desc,
            repeat=args.repeat,
            reminder=args.reminder
        )
        print(f"[OK] Created: {event['name']} (ID: {event['id']})")
    
    elif args.command == "list":
        events = manager.list_events(event_type=args.type, date=args.date)
        if events:
            print(f"[Schedule List] {len(events)} events")
            print("-" * 60)
            for e in events:
                status = "[x]" if e.get("completed") else "[ ]"
                cat = manager.config["categories"].get(e["type"], {})
                icon = cat.get("icon", "📌")
                print(f"{status} {icon} {e['name']}")
                print(f"    Date: {e['date']} | Time: {e['time']}")
                print(f"    ID: {e['id']} | Repeat: {e['repeat']}")
                print()
        else:
            print("[INFO] No events found")
    
    elif args.command == "today":
        events = manager.get_today_events()
        if events:
            print(f"[Today] {len(events)} events")
            print("-" * 60)
            for e in events:
                status = "[x]" if e.get("completed") else "[ ]"
                cat = manager.config["categories"].get(e["type"], {})
                icon = cat.get("icon", "📌")
                print(f"{status} {icon} {e['name']} ({e['time']})")
        else:
            print("[INFO] No events today")
    
    elif args.command == "delete":
        if manager.delete_event(args.id):
            print(f"[OK] Deleted: {args.id}")
        else:
            print(f"[ERROR] Event not found: {args.id}")
    
    elif args.command == "complete":
        if manager.complete_event(args.id):
            print(f"[OK] Completed: {args.id}")
        else:
            print(f"[ERROR] Event not found: {args.id}")
    
    elif args.command == "stats":
        stats = manager.get_stats()
        print("[Statistics]")
        print("-" * 60)
        print(f"Total: {stats['total']}")
        print(f"Completed: {stats['completed']}")
        print(f"Pending: {stats['pending']}")
        print(f"Completion Rate: {stats['completion_rate']}%")
        print("\nBy Type:")
        for t, s in stats['by_type'].items():
            cat = manager.config["categories"].get(t, {})
            name = cat.get("name", t)
            print(f"  {name}: {s['completed']}/{s['total']}")
    
    elif args.command == "export":
        events = manager.export_to_feishu_format()
        output_file = os.path.join(DATA_DIR, "feishu_export.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        print(f"[OK] Exported to {output_file}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
