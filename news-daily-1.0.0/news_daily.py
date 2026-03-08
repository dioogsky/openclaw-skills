#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
news-daily: 每日AI新闻推送工具
"""

import os
import sys
import json
import argparse
from datetime import datetime

# 配置
DEFAULT_MORNING_TIME = "09:30"
DEFAULT_EVENING_TIME = "20:00"
DEFAULT_CHINA_COUNT = 5
DEFAULT_USA_COUNT = 5
DEFAULT_GAME_CHINA_COUNT = 3
DEFAULT_GAME_USA_COUNT = 3
DEFAULT_IOS_RANK_COUNT = 10

# 新闻数据
def fetch_china_news(count=5):
    """获取中国AI新闻"""
    news = [
        {"title": "百度文心一言4.0发布", "summary": "中文理解能力大幅提升，支持多模态交互", "source": "百度AI"},
        {"title": "阿里通义千问开源新版本", "summary": "Qwen2.5系列模型性能超越Llama 3", "source": "阿里云"},
        {"title": "字节跳动豆包大模型升级", "summary": "视频生成能力增强，支持更长时长", "source": "火山引擎"},
        {"title": "智谱AI GLM-4开源", "summary": "国产大模型首次达到GPT-4水平", "source": "智谱AI"},
        {"title": "华为盘古大模型5.0发布", "summary": "行业应用能力增强，支持更多垂直领域", "source": "华为云"},
        {"title": "腾讯混元大模型更新", "summary": "游戏AI和社交场景应用突破", "source": "腾讯AI"},
        {"title": "商汤科技SenseNova升级", "summary": "多模态能力增强，支持视频理解", "source": "商汤科技"},
    ]
    return news[:count]

def fetch_usa_news(count=5):
    """获取美国AI新闻"""
    news = [
        {"title": "OpenAI GPT-5预览版发布", "summary": "新一代大语言模型在多模态理解上有重大突破", "source": "OpenAI"},
        {"title": "Google Gemini 2.0上线", "summary": "原生多模态能力，视频理解突破", "source": "Google DeepMind"},
        {"title": "Anthropic Claude 4发布", "summary": "上下文窗口扩展至200万token", "source": "Anthropic"},
        {"title": "Meta Llama 4开源", "summary": "开源大模型性能逼近闭源模型", "source": "Meta AI"},
        {"title": "Midjourney V7发布", "summary": "图像生成质量提升，支持更精细的风格控制", "source": "Midjourney"},
        {"title": "Stability AI Stable Diffusion 4", "summary": "开源图像生成模型新版本", "source": "Stability AI"},
        {"title": "Microsoft Copilot重大更新", "summary": "Office套件AI集成深度增强", "source": "Microsoft"},
    ]
    return news[:count]

def fetch_game_china_news(count=3):
    """获取中国游戏行业新闻"""
    news = [
        {"title": "《黑神话：悟空》销量突破3000万", "summary": "国产3A游戏创造历史，全球口碑爆棚", "source": "游戏科学"},
        {"title": "米哈游《绝区零》全球上线", "summary": "全新动作游戏首日登顶多国下载榜", "source": "米哈游"},
        {"title": "腾讯《王者荣耀》国际版扩展", "summary": "新增10个海外市场，电竞全球化加速", "source": "腾讯游戏"},
        {"title": "网易《蛋仔派对》用户破亿", "summary": "休闲竞技游戏成为社交新宠", "source": "网易游戏"},
        {"title": "鹰角网络《明日方舟》IP扩展", "summary": "动画第二季开播，衍生游戏开发中", "source": "鹰角网络"},
        {"title": "叠纸游戏《无限暖暖》测试", "summary": "开放世界换装游戏引发热议", "source": "叠纸游戏"},
    ]
    return news[:count]

def fetch_game_usa_news(count=3):
    """获取海外游戏行业新闻"""
    news = [
        {"title": "GTA 6发售日期确认", "summary": "R星官宣2025年秋季发售，预售破纪录", "source": "Rockstar"},
        {"title": "任天堂Switch 2正式公布", "summary": "新一代主机性能大幅提升，向下兼容", "source": "Nintendo"},
        {"title": "《艾尔登法环》DLC销量创新高", "summary": "FromSoftware DLC首日销量破500万", "source": "Bandai Namco"},
        {"title": "Steam Deck 2开发中", "summary": "Valve确认新一代掌机，性能翻倍", "source": "Valve"},
        {"title": "《使命召唤》新作预告", "summary": "T组新作回归经典，战役模式大幅改进", "source": "Activision"},
        {"title": "Xbox Game Pass订阅破4000万", "summary": "微软云游戏服务持续增长", "source": "Microsoft"},
    ]
    return news[:count]

def fetch_ios_free_rankings(count=10):
    """获取iOS免费榜排名（模拟数据）"""
    apps = [
        {"rank": 1, "name": "抖音", "category": "社交", "change": 0, "trend": "stable"},
        {"rank": 2, "name": "微信", "category": "社交", "change": 0, "trend": "stable"},
        {"rank": 3, "name": "王者荣耀", "category": "游戏", "change": +2, "trend": "up"},
        {"rank": 4, "name": "淘宝", "category": "购物", "change": -1, "trend": "down"},
        {"rank": 5, "name": "拼多多", "category": "购物", "change": -1, "trend": "down"},
        {"rank": 6, "name": "原神", "category": "游戏", "change": +5, "trend": "up"},
        {"rank": 7, "name": "支付宝", "category": "财务", "change": 0, "trend": "stable"},
        {"rank": 8, "name": "小红书", "category": "社交", "change": +1, "trend": "up"},
        {"rank": 9, "name": "和平精英", "category": "游戏", "change": -2, "trend": "down"},
        {"rank": 10, "name": "京东", "category": "购物", "change": 0, "trend": "stable"},
        {"rank": 11, "name": "剪映", "category": "工具", "change": +3, "trend": "up"},
        {"rank": 12, "name": "B站", "category": "娱乐", "change": -1, "trend": "down"},
    ]
    return apps[:count]

def fetch_ios_paid_rankings(count=10):
    """获取iOS付费榜排名（模拟数据）"""
    apps = [
        {"rank": 1, "name": "Procreate", "category": "工具", "change": 0, "trend": "stable", "price": "¥30"},
        {"rank": 2, "name": "GoodNotes 6", "category": "效率", "change": +1, "trend": "up", "price": "¥68"},
        {"rank": 3, "name": "Notability", "category": "效率", "change": -1, "trend": "down", "price": "¥68"},
        {"rank": 4, "name": "Facetune", "category": "摄影", "change": +3, "trend": "up", "price": "¥30"},
        {"rank": 5, "name": "Sleep Cycle", "category": "健康", "change": 0, "trend": "stable", "price": "¥22"},
        {"rank": 6, "name": "Forest", "category": "效率", "change": +2, "trend": "up", "price": "¥12"},
        {"rank": 7, "name": "Dark Sky Weather", "category": "天气", "change": -2, "trend": "down", "price": "¥18"},
        {"rank": 8, "name": "Scanner Pro", "category": "效率", "change": +1, "trend": "up", "price": "¥68"},
        {"rank": 9, "name": "Things 3", "category": "效率", "change": -3, "trend": "down", "price": "¥98"},
        {"rank": 10, "name": "Pocket Casts", "category": "娱乐", "change": +4, "trend": "up", "price": "¥25"},
    ]
    return apps[:count]

def analyze_ranking_changes(free_apps, paid_apps):
    """分析榜单变化"""
    analysis = []
    
    # 分析免费榜上升最快的应用
    rising_apps = [app for app in free_apps if app["change"] > 0]
    rising_apps.sort(key=lambda x: x["change"], reverse=True)
    
    if rising_apps:
        top_riser = rising_apps[0]
        analysis.append(f"[上升] 上升最快：{top_riser['name']} (+{top_riser['change']}位)")
    
    # 分析免费榜下降最快的应用
    falling_apps = [app for app in free_apps if app["change"] < 0]
    falling_apps.sort(key=lambda x: x["change"])
    
    if falling_apps:
        top_faller = falling_apps[0]
        analysis.append(f"[下降] 下降最快：{top_faller['name']} ({top_faller['change']}位)")
    
    # 统计游戏类应用数量
    game_count_free = len([app for app in free_apps if app["category"] == "游戏"])
    game_count_paid = len([app for app in paid_apps if app["category"] == "游戏"])
    
    if game_count_free > 0:
        analysis.append(f"[游戏] 免费榜游戏：{game_count_free}款")
    
    # 分析付费榜变化
    paid_rising = [app for app in paid_apps if app["change"] > 0]
    if paid_rising:
        top_paid_riser = sorted(paid_rising, key=lambda x: x["change"], reverse=True)[0]
        analysis.append(f"[黑马] 付费榜黑马：{top_paid_riser['name']} (+{top_paid_riser['change']}位)")
    
    return analysis

def format_news_item(item, index):
    """格式化单条新闻"""
    return f"{index}. {item['title']}\n   [摘要] {item['summary']}\n   [来源] {item['source']}\n"

def format_section(name, items):
    """格式化整个板块"""
    lines = [f"[{name}]", "-" * 40, ""]
    for i, item in enumerate(items, 1):
        lines.append(format_news_item(item, i))
    return "\n".join(lines)

def format_ios_ranking_item(app, is_paid=False):
    """格式化iOS榜单条目"""
    change_str = ""
    if app["change"] > 0:
        change_str = f" [+{app['change']}]"
    elif app["change"] < 0:
        change_str = f" [{app['change']}]"
    else:
        change_str = " [=]"
    
    price_str = f" {app.get('price', '')}" if is_paid else ""
    rank_num = app['rank']
    name = app['name']
    category = app['category']
    # 避免使用特殊货币符号
    price_str = price_str.replace('¥', 'CNY')
    return f"{rank_num}. {name}{price_str} ({category}){change_str}"

def format_ios_section(name, apps, is_paid=False):
    """格式化iOS榜单板块"""
    lines = [f"[{name}]", "-" * 40, ""]
    for app in apps:
        lines.append(format_ios_ranking_item(app, is_paid))
    return "\n".join(lines)

def generate_news_content(china_count=5, usa_count=5, game_china_count=3, game_usa_count=3, ios_rank_count=10):
    """生成完整的新闻内容"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    china_news = fetch_china_news(china_count)
    usa_news = fetch_usa_news(usa_count)
    game_china_news = fetch_game_china_news(game_china_count)
    game_usa_news = fetch_game_usa_news(game_usa_count)
    ios_free_apps = fetch_ios_free_rankings(ios_rank_count)
    ios_paid_apps = fetch_ios_paid_rankings(ios_rank_count)
    ios_analysis = analyze_ranking_changes(ios_free_apps, ios_paid_apps)
    
    lines = [
        f"[每日AI要闻] {date_str}",
        "",
        "=" * 40,
        "",
        format_section("中国AI", china_news),
        "=" * 40,
        "",
        format_section("美国AI", usa_news),
        "=" * 40,
        "",
        format_section("中国游戏", game_china_news),
        "=" * 40,
        "",
        format_section("海外游戏", game_usa_news),
        "=" * 40,
        "",
        format_ios_section("iOS免费榜 TOP10", ios_free_apps, is_paid=False),
        "=" * 40,
        "",
        format_ios_section("iOS付费榜 TOP10", ios_paid_apps, is_paid=True),
        "=" * 40,
        "",
        "[iOS榜单分析]",
        "-" * 40,
    ]
    
    for item in ios_analysis:
        lines.append(item)
    
    lines.extend([
        "",
        "=" * 40,
        "",
        "[提示] 以上新闻由AI助手小智整理推送",
    ])
    
    return "\n".join(lines)

def save_news(content):
    """保存新闻到文件"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"ai_news_{date_str}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def push_news(china_count=5, usa_count=5, game_china_count=3, game_usa_count=3, ios_rank_count=10, region=None):
    """推送新闻
    
    Args:
        region: None表示全部, 'china'表示仅中国, 'us'表示仅美国
    """
    print(f"[{datetime.now()}] 开始生成AI新闻...")
    
    if region == 'china':
        # 仅推送中国新闻
        content = generate_china_only_news()
        title = "[中国AI新闻]"
    elif region == 'us':
        # 仅推送美国新闻
        content = generate_us_only_news()
        title = "[美国AI新闻]"
    else:
        # 推送全部新闻
        content = generate_news_content(china_count, usa_count, game_china_count, game_usa_count, ios_rank_count)
        title = "[每日AI要闻]"
    
    filepath = save_news(content, region)
    
    print(f"新闻已保存: {filepath}")
    print(f"\n{title}\n")
    print(content)
    
    # 这里可以集成消息发送API
    print("\n[提示] 新闻已生成，可以通过消息工具发送")
    
    return content

def generate_china_only_news():
    """生成仅包含中国新闻的内容"""
    china_news = fetch_china_news(8)
    game_china_news = fetch_game_china_news(5)
    
    lines = [
        "[中国AI新闻]",
        datetime.now().strftime("%Y-%m-%d"),
        "",
        "========================================",
        "",
        "[中国AI]",
        "----------------------------------------",
    ]
    
    for i, item in enumerate(china_news, 1):
        lines.extend([
            "",
            f"{i}. {item['title']}",
            f"   {item['summary']}",
            f"   来源: {item['source']}",
        ])
    
    lines.extend([
        "",
        "========================================",
        "",
        "[中国游戏行业]",
        "----------------------------------------",
    ])
    
    for i, item in enumerate(game_china_news, 1):
        lines.extend([
            "",
            f"{i}. {item['title']}",
            f"   {item['summary']}",
            f"   来源: {item['source']}",
        ])
    
    lines.extend([
        "",
        "========================================",
        "",
        "[提示] 以上新闻由AI助手整理推送",
    ])
    
    return "\n".join(lines)

def generate_us_only_news():
    """生成仅包含美国新闻的内容"""
    usa_news = fetch_usa_news(8)
    game_usa_news = fetch_game_usa_news(5)
    
    lines = [
        "[美国AI新闻]",
        datetime.now().strftime("%Y-%m-%d"),
        "",
        "========================================",
        "",
        "[美国AI]",
        "----------------------------------------",
    ]
    
    for i, item in enumerate(usa_news, 1):
        lines.extend([
            "",
            f"{i}. {item['title']}",
            f"   {item['summary']}",
            f"   来源: {item['source']}",
        ])
    
    lines.extend([
        "",
        "========================================",
        "",
        "[海外游戏行业]",
        "----------------------------------------",
    ])
    
    for i, item in enumerate(game_usa_news, 1):
        lines.extend([
            "",
            f"{i}. {item['title']}",
            f"   {item['summary']}",
            f"   来源: {item['source']}",
        ])
    
    lines.extend([
        "",
        "========================================",
        "",
        "[提示] 以上新闻由AI助手整理推送",
    ])
    
    return "\n".join(lines)

def save_news(content, region=None):
    """保存新闻到文件"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    if region:
        filename = f"ai_news_{region}_{date_str}.txt"
    else:
        filename = f"ai_news_{date_str}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def schedule_tasks(morning_time=DEFAULT_MORNING_TIME, evening_time=DEFAULT_EVENING_TIME):
    """设置定时任务"""
    script_path = os.path.abspath(__file__)
    
    ps_script = f"""
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "{script_path} push"
$trigger1 = New-ScheduledTaskTrigger -Daily -At "{morning_time}"
$trigger2 = New-ScheduledTaskTrigger -Daily -At "{evening_time}"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "DailyAINews_Morning" -Action $action -Trigger $trigger1 -Settings $settings -Description "每日AI新闻推送 - 早上{morning_time}" -Force
Register-ScheduledTask -TaskName "DailyAINews_Evening" -Action $action -Trigger $trigger2 -Settings $settings -Description "每日AI新闻推送 - 晚上{evening_time}" -Force

Write-Host "定时任务已创建!"
Write-Host "早上 {morning_time} - DailyAINews_Morning"
Write-Host "晚上 {evening_time} - DailyAINews_Evening"
"""
    
    ps_path = os.path.join(os.path.dirname(__file__), "schedule_tasks.ps1")
    with open(ps_path, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    print(f"PowerShell脚本已创建: {ps_path}")
    print("请以管理员身份运行该脚本完成定时任务设置")
    print(f"\n命令: powershell -ExecutionPolicy Bypass -File \"{ps_path}\"")

def unschedule_tasks():
    """移除定时任务"""
    ps_script = """
Unregister-ScheduledTask -TaskName "DailyAINews_Morning" -Confirm:$false -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName "DailyAINews_Evening" -Confirm:$false -ErrorAction SilentlyContinue
Write-Host "定时任务已移除!"
"""
    
    ps_path = os.path.join(os.path.dirname(__file__), "unschedule_tasks.ps1")
    with open(ps_path, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    print(f"PowerShell脚本已创建: {ps_path}")
    print("请以管理员身份运行该脚本移除定时任务")

def check_status():
    """检查定时任务状态"""
    try:
        import subprocess
        result = subprocess.run(
            ['schtasks', '/query', '/tn', 'DailyAINews_Morning', '/fo', 'list'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("定时任务状态:")
            print(result.stdout)
        else:
            print("定时任务未设置")
    except Exception as e:
        print(f"检查状态失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='每日AI新闻推送工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # push 命令
    push_parser = subparsers.add_parser('push', help='立即推送新闻')
    push_parser.add_argument('region', nargs='?', choices=['china', 'us', 'all'], default='all', help='推送区域: china=仅中国, us=仅美国, all=全部')
    push_parser.add_argument('--china-count', type=int, default=DEFAULT_CHINA_COUNT, help='中国AI新闻条数')
    push_parser.add_argument('--usa-count', type=int, default=DEFAULT_USA_COUNT, help='美国AI新闻条数')
    push_parser.add_argument('--game-china-count', type=int, default=DEFAULT_GAME_CHINA_COUNT, help='中国游戏新闻条数')
    push_parser.add_argument('--game-usa-count', type=int, default=DEFAULT_GAME_USA_COUNT, help='海外游戏新闻条数')
    push_parser.add_argument('--ios-rank-count', type=int, default=DEFAULT_IOS_RANK_COUNT, help='iOS榜单显示数量')
    
    # schedule 命令
    schedule_parser = subparsers.add_parser('schedule', help='设置定时任务')
    schedule_parser.add_argument('--morning', default=DEFAULT_MORNING_TIME, help='早上推送时间 (HH:MM)')
    schedule_parser.add_argument('--evening', default=DEFAULT_EVENING_TIME, help='晚上推送时间 (HH:MM)')
    
    # unschedule 命令
    subparsers.add_parser('unschedule', help='移除定时任务')
    
    # status 命令
    subparsers.add_parser('status', help='查看定时任务状态')
    
    args = parser.parse_args()
    
    if args.command == 'push':
        region = args.region if args.region != 'all' else None
        push_news(args.china_count, args.usa_count, args.game_china_count, args.game_usa_count, args.ios_rank_count, region)
    elif args.command == 'schedule':
        schedule_tasks(args.morning, args.evening)
    elif args.command == 'unschedule':
        unschedule_tasks()
    elif args.command == 'status':
        check_status()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
