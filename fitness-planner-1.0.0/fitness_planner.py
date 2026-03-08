#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fitness-planner: 个人健身计划制定和跟踪工具
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta

# 配置文件路径
CONFIG_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(CONFIG_DIR, "fitness_data.json")

# 预设训练计划
WORKOUT_PLANS = {
    "fat-loss": {
        "name": "减脂计划",
        "description": "以有氧运动为主，配合适量力量训练",
        "weekly_schedule": [
            {"day": "周一", "type": "有氧", "duration": 40, "intensity": "中"},
            {"day": "周二", "type": "力量", "duration": 45, "focus": "全身"},
            {"day": "周三", "type": "休息", "duration": 0},
            {"day": "周四", "type": "HIIT", "duration": 30, "intensity": "高"},
            {"day": "周五", "type": "有氧", "duration": 40, "intensity": "中"},
            {"day": "周六", "type": "力量", "duration": 45, "focus": "全身"},
            {"day": "周日", "type": "休息", "duration": 0},
        ],
        "diet_tips": [
            "控制总热量摄入，制造热量缺口",
            "增加蛋白质摄入，保护肌肉",
            "减少精制碳水，选择粗粮",
            "多喝水，每天至少2L",
        ]
    },
    "muscle-gain": {
        "name": "增肌计划",
        "description": "以力量训练为主，注重渐进式负荷",
        "weekly_schedule": [
            {"day": "周一", "type": "力量", "duration": 60, "focus": "胸+三头"},
            {"day": "周二", "type": "力量", "duration": 60, "focus": "背+二头"},
            {"day": "周三", "type": "休息", "duration": 0},
            {"day": "周四", "type": "力量", "duration": 60, "focus": "腿部"},
            {"day": "周五", "type": "力量", "duration": 60, "focus": "肩部"},
            {"day": "周六", "type": "力量", "duration": 60, "focus": "全身"},
            {"day": "周日", "type": "休息", "duration": 0},
        ],
        "diet_tips": [
            "增加热量摄入，制造热量盈余",
            "蛋白质每公斤体重1.6-2.2g",
            "训练后补充快碳和蛋白质",
            "保证充足睡眠，促进肌肉恢复",
        ]
    },
    "shape": {
        "name": "塑形计划",
        "description": "综合训练，注重身体线条塑造",
        "weekly_schedule": [
            {"day": "周一", "type": "综合", "duration": 50, "focus": "上肢"},
            {"day": "周二", "type": "有氧", "duration": 35, "intensity": "中"},
            {"day": "周三", "type": "休息", "duration": 0},
            {"day": "周四", "type": "综合", "duration": 50, "focus": "下肢"},
            {"day": "周五", "type": "瑜伽", "duration": 45, "focus": "拉伸"},
            {"day": "周六", "type": "综合", "duration": 50, "focus": "核心"},
            {"day": "周日", "type": "休息", "duration": 0},
        ],
        "diet_tips": [
            "保持均衡饮食，控制热量",
            "增加蔬菜摄入，补充纤维",
            "适量蛋白质，维持肌肉",
            "少食多餐，稳定血糖",
        ]
    },
    "maintain": {
        "name": "维持计划",
        "description": "保持当前状态，灵活安排",
        "weekly_schedule": [
            {"day": "周一", "type": "综合", "duration": 40},
            {"day": "周二", "type": "休息", "duration": 0},
            {"day": "周三", "type": "有氧", "duration": 35},
            {"day": "周四", "type": "休息", "duration": 0},
            {"day": "周五", "type": "力量", "duration": 45},
            {"day": "周六", "type": "休息", "duration": 0},
            {"day": "周日", "type": "瑜伽", "duration": 40},
        ],
        "diet_tips": [
            "保持当前饮食习惯",
            "注意营养均衡",
            "适量运动，保持活力",
        ]
    }
}

def load_data():
    """加载数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "plan": None,
        "logs": [],
        "stats": {
            "total_workouts": 0,
            "total_duration": 0,
            "current_streak": 0,
            "max_streak": 0
        },
        "created_at": datetime.now().isoformat()
    }

def save_data(data):
    """保存数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_plan(goal, level="beginner", workout_time=None, weekend_time=None):
    """创建健身计划"""
    if goal not in WORKOUT_PLANS:
        print(f"错误：未知的目标 '{goal}'")
        print(f"可选值: {', '.join(WORKOUT_PLANS.keys())}")
        return
    
    plan = WORKOUT_PLANS[goal].copy()
    plan["goal"] = goal
    plan["level"] = level
    if workout_time:
        plan["workout_time"] = workout_time
    if weekend_time:
        plan["weekend_time"] = weekend_time
    plan["created_at"] = datetime.now().isoformat()
    
    data = load_data()
    data["plan"] = plan
    save_data(data)
    
    print(f"[OK] 已创建健身计划：{plan['name']}")
    print(f"   目标：{goal}")
    print(f"   水平：{level}")
    print(f"   描述：{plan['description']}")
    if workout_time:
        print(f"   工作日时间：{workout_time}")
    if weekend_time:
        print(f"   周末时间：{weekend_time}")
    print(f"\n[每周训练安排]")
    for item in plan["weekly_schedule"]:
        if item["duration"] > 0:
            print(f"   {item['day']}: {item['type']} - {item['duration']}分钟")
        else:
            print(f"   {item['day']}: 休息日")
    
    print(f"\n[饮食建议]")
    for tip in plan["diet_tips"]:
        print(f"   - {tip}")

def log_workout(date_str, workout_type, duration, notes=""):
    """记录训练"""
    data = load_data()
    
    log = {
        "date": date_str,
        "type": workout_type,
        "duration": duration,
        "notes": notes,
        "logged_at": datetime.now().isoformat()
    }
    
    data["logs"].append(log)
    
    # 更新统计
    data["stats"]["total_workouts"] += 1
    data["stats"]["total_duration"] += duration
    
    # 计算连续训练天数
    dates = sorted(set([l["date"] for l in data["logs"]]))
    current_streak = 0
    check_date = datetime.now().date()
    
    for d in reversed(dates):
        log_date = datetime.strptime(d, "%Y-%m-%d").date()
        if (check_date - log_date).days <= 1:
            current_streak += 1
            check_date = log_date
        else:
            break
    
    data["stats"]["current_streak"] = current_streak
    if current_streak > data["stats"]["max_streak"]:
        data["stats"]["max_streak"] = current_streak
    
    save_data(data)
    
    print(f"[OK] 已记录训练")
    print(f"   日期：{date_str}")
    print(f"   类型：{workout_type}")
    print(f"   时长：{duration}分钟")
    if notes:
        print(f"   备注：{notes}")
    print(f"\n[统计] 当前连续训练：{current_streak}天")

def show_today():
    """显示今日计划"""
    data = load_data()
    
    if not data["plan"]:
        print("❌ 还没有创建健身计划")
        print("   使用：python fitness_planner.py create-plan --goal <目标>")
        return
    
    weekday = datetime.now().weekday()
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    today_name = days[weekday]
    
    today_plan = None
    for item in data["plan"]["weekly_schedule"]:
        if item["day"] == today_name:
            today_plan = item
            break
    
    # 获取时间安排
    plan = data["plan"]
    workout_time = plan.get("workout_time", "未设置")
    weekend_time = plan.get("weekend_time", "未设置")
    
    # 判断今天是否是周末
    is_weekend = weekday >= 5  # 周六=5, 周日=6
    time_slot = weekend_time if is_weekend else workout_time
    
    if today_plan:
        if today_plan["duration"] > 0:
            print(f"[今日计划] ({today_name})")
            print(f"   类型：{today_plan['type']}")
            print(f"   时长：{today_plan['duration']}分钟")
            if "focus" in today_plan:
                print(f"   重点：{today_plan['focus']}")
            if "intensity" in today_plan:
                print(f"   强度：{today_plan['intensity']}")
            print(f"   时间：{time_slot}")
            print(f"   =================================")
            print(f"   [提醒] 记得在 {time_slot} 完成训练！")
            print(f"   =================================")
        else:
            print(f"[今日计划] ({today_name})")
            print("   今天是休息日！")
            print("   建议：适当拉伸放松，保证充足睡眠")
    
    # 检查今日是否已记录
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_logs = [l for l in data["logs"] if l["date"] == today_str]
    
    if today_logs:
        print(f"\n[已完成] 今日训练：")
        for log in today_logs:
            print(f"   - {log['type']} - {log['duration']}分钟")
    else:
        print(f"\n[待完成] 今日还未记录训练")

def show_stats():
    """显示统计信息"""
    data = load_data()
    stats = data["stats"]
    
    print("[健身统计]")
    print("=" * 40)
    print(f"总训练次数：{stats['total_workouts']}次")
    print(f"总训练时长：{stats['total_duration']}分钟 ({stats['total_duration']//60}小时)")
    print(f"当前连续：{stats['current_streak']}天")
    print(f"最长连续：{stats['max_streak']}天")
    
    if data["logs"]:
        # 最近7天训练
        print(f"\n[最近7天训练]")
        recent_logs = data["logs"][-7:]
        for log in recent_logs:
            print(f"   {log['date']}: {log['type']} - {log['duration']}分钟")

def create_calendar_events(access_token=None):
    """创建飞书日历事件"""
    import requests
    
    data = load_data()
    if not data.get("plan"):
        print("❌ 还没有创建健身计划")
        return
    
    plan = data["plan"]
    workout_time = plan.get("workout_time", "20:30-21:30")
    weekend_time = plan.get("weekend_time", "16:00-18:00")
    
    # 准备事件数据
    start_date = datetime.now().date() + timedelta(days=1)
    events = []
    
    for i, item in enumerate(plan["weekly_schedule"]):
        if item["duration"] == 0:
            continue
        
        target_date = start_date + timedelta(days=i)
        is_weekend = target_date.weekday() >= 5
        time_slot = weekend_time if is_weekend else workout_time
        
        start_time, end_time = time_slot.split("-")
        start_datetime = target_date.strftime(f"%Y-%m-%dT{start_time}:00+08:00")
        end_datetime = target_date.strftime(f"%Y-%m-%dT{end_time}:00+08:00")
        
        if item["type"] == "有氧":
            description = f"{item['type']}训练\n时长：{item['duration']}分钟\n强度：{item.get('intensity', '中')}"
        elif item["type"] == "力量":
            description = f"{item['type']}训练\n时长：{item['duration']}分钟\n重点：{item.get('focus', '全身')}"
        elif item["type"] == "HIIT":
            description = f"{item['type']}训练\n时长：{item['duration']}分钟\n强度：{item.get('intensity', '高')}"
        else:
            description = f"{item['type']}训练\n时长：{item['duration']}分钟"
        
        event = {
            "day": item["day"],
            "date": target_date.isoformat(),
            "summary": f"健身 - {item['type']}",
            "description": description,
            "start_time": start_datetime,
            "end_time": end_datetime,
        }
        events.append(event)
    
    # 保存事件数据
    calendar_file = os.path.join(CONFIG_DIR, "calendar_events.json")
    with open(calendar_file, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 已生成 {len(events)} 个日历事件")
    print(f"[FILE] 数据保存到: {calendar_file}")
    
    # 显示事件列表
    print("\n[健身日程]")
    print("=" * 60)
    for event in events:
        print(f"\n{event['day']} ({event['date']})")
        print(f"  标题: {event['summary']}")
        print(f"  时间: {event['start_time']} - {event['end_time']}")
        print(f"  内容: {event['description']}")
    
    # 如果有access_token，自动创建
    if access_token:
        print("\n[INFO] 正在创建飞书日历事件...")
        base_url = "https://open.feishu.cn/open-apis"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 获取主日历
        try:
            response = requests.get(f"{base_url}/calendar/v4/calendars", headers=headers)
            cal_data = response.json()
            
            if cal_data.get("code") == 0:
                calendars = cal_data.get("data", {}).get("calendar_list", [])
                calendar_id = None
                for cal in calendars:
                    if cal.get("is_primary"):
                        calendar_id = cal.get("calendar_id")
                        break
                if not calendar_id and calendars:
                    calendar_id = calendars[0].get("calendar_id")
                
                if calendar_id:
                    success_count = 0
                    for event in events:
                        event_data = {
                            "summary": event["summary"],
                            "description": event["description"],
                            "start": {
                                "date_time": event["start_time"],
                                "timezone": "Asia/Shanghai"
                            },
                            "end": {
                                "date_time": event["end_time"],
                                "timezone": "Asia/Shanghai"
                            },
                            "reminders": [
                                {
                                    "method": "app",
                                    "minutes": 30
                                }
                            ]
                        }
                        
                        resp = requests.post(
                            f"{base_url}/calendar/v4/calendars/{calendar_id}/events",
                            headers=headers,
                            json=event_data
                        )
                        resp_data = resp.json()
                        if resp_data.get("code") == 0:
                            success_count += 1
                        else:
                            print(f"[DEBUG] 创建失败: {resp_data.get('msg', '未知错误')}")
                    
                    print(f"[OK] 成功创建 {success_count}/{len(events)} 个事件")
                    if success_count < len(events):
                        print(f"[WARNING] {len(events) - success_count} 个事件创建失败")
                else:
                    print("[ERROR] 未找到日历")
                    print("[TIP] 请检查token是否有calendar权限")
            else:
                print(f"[ERROR] 获取日历失败: {cal_data.get('msg', '未知错误')}")
        except Exception as e:
            print(f"[ERROR] 创建事件失败: {e}")
    else:
        print("\n[TIP] 提示：提供access_token可自动创建事件")
        print("      或使用生成的JSON文件手动导入")

def main():
    parser = argparse.ArgumentParser(description='健身计划制定和跟踪工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # create-plan 命令
    create_parser = subparsers.add_parser('create-plan', help='创建健身计划')
    create_parser.add_argument('--goal', required=True, 
                              choices=['fat-loss', 'muscle-gain', 'shape', 'maintain'],
                              help='健身目标')
    create_parser.add_argument('--level', default='beginner',
                              choices=['beginner', 'intermediate', 'advanced'],
                              help='健身水平')
    create_parser.add_argument('--workout-time', default=None,
                              help='工作日训练时间 (如: 08:30-09:30)')
    create_parser.add_argument('--weekend-time', default=None,
                              help='周末训练时间 (如: 16:00-18:00)')
    
    # log 命令
    log_parser = subparsers.add_parser('log', help='记录训练')
    log_parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'),
                           help='训练日期 (YYYY-MM-DD)')
    log_parser.add_argument('--type', required=True,
                           choices=['有氧', '力量', 'HIIT', '瑜伽', '综合', '其他'],
                           help='训练类型')
    log_parser.add_argument('--duration', type=int, required=True,
                           help='训练时长（分钟）')
    log_parser.add_argument('--notes', default='', help='备注')
    
    # today 命令
    subparsers.add_parser('today', help='查看今日计划')
    
    # stats 命令
    subparsers.add_parser('stats', help='查看统计信息')
    
    # calendar 命令
    calendar_parser = subparsers.add_parser('calendar', help='创建飞书日历事件')
    calendar_parser.add_argument('--token', default=None, help='飞书access_token')
    
    args = parser.parse_args()
    
    if args.command == 'create-plan':
        create_plan(args.goal, args.level, args.workout_time, args.weekend_time)
    elif args.command == 'log':
        log_workout(args.date, args.type, args.duration, args.notes)
    elif args.command == 'today':
        show_today()
    elif args.command == 'stats':
        show_stats()
    elif args.command == 'calendar':
        create_calendar_events(args.token)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
