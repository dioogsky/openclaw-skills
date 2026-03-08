import json
import os
from datetime import datetime, timedelta
import random

STATE_FILE = r"C:\Users\MyPC\.openclaw\workspace\memory\travel-planner-state.json"
REPORTS_DIR = r"C:\Users\MyPC\.openclaw\workspace\memory\travel-reports"

# 模拟数据源（实际可接入携程、去哪儿等API）
MOCK_DESTINATIONS = {
    "东南亚": ["曼谷", "清迈", "普吉岛", "巴厘岛", "新加坡", "吉隆坡", "越南岘港"],
    "东亚": ["东京", "大阪", "首尔", "台北", "香港", "澳门"],
    "欧洲": ["巴黎", "罗马", "巴塞罗那", "阿姆斯特丹", "布拉格", "维也纳"],
    "国内": ["三亚", "丽江", "大理", "厦门", "成都", "西安", "新疆"]
}

MOCK_FLIGHT_PRICES = {
    "曼谷": {"low": 1200, "high": 3500, "currency": "CNY"},
    "东京": {"low": 2000, "high": 5000, "currency": "CNY"},
    "巴黎": {"low": 4500, "high": 9000, "currency": "CNY"},
    "三亚": {"low": 800, "high": 2000, "currency": "CNY"},
    "新加坡": {"low": 1800, "high": 4000, "currency": "CNY"}
}

class TravelPlanner:
    def __init__(self):
        self.state = self.load_state()
        os.makedirs(REPORTS_DIR, exist_ok=True)
    
    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.create_default_state()
    
    def save_state(self):
        self.state['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def create_default_state(self):
        return {
            "budget_total": 150000,
            "budget_used": 0,
            "budget_remaining": 150000,
            "travel_periods": [],
            "destinations": [],
            "tracked_routes": [],
            "price_alerts": [],
            "reports": {
                "last_daily_update": None,
                "last_weekly_report": None
            }
        }
    
    def scan_prices(self):
        """扫描低价航班和酒店"""
        results = []
        
        for route in self.state.get('tracked_routes', []):
            # 模拟价格扫描
            base_price = MOCK_FLIGHT_PRICES.get(route['destination'], {}).get('low', 2000)
            current_price = base_price + random.randint(-300, 500)
            
            price_data = {
                "route": f"{route['origin']} → {route['destination']}",
                "date": route.get('date', 'flexible'),
                "current_price": current_price,
                "currency": "CNY",
                "trend": "down" if random.random() > 0.5 else "up",
                "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            results.append(price_data)
        
        return results
    
    def generate_daily_update(self):
        """生成每日更新"""
        today = datetime.now().strftime("%Y-%m-%d")
        prices = self.scan_prices()
        
        report = f"""[旅行计划每日更新] {today}

[预算状态]
总预算: {self.state['budget_total']:,} CNY
已使用: {self.state.get('budget_used', 0):,} CNY
剩余: {self.state.get('budget_remaining', self.state['budget_total']):,} CNY

[今日价格扫描] ({len(prices)}条路线)
"""
        
        if prices:
            for p in prices[:5]:  # 显示前5条
                trend_mark = "[降价]" if p['trend'] == 'down' else "[涨价]"
                report += f"\n{trend_mark} {p['route']}"
                report += f"\n   当前: {p['current_price']:,} CNY | 扫描时间: {p['scanned_at']}"
        else:
            report += "\n暂无追踪路线，请使用 add-route 添加"
        
        report += f"""

[今日建议]
{self.get_daily_tip()}

---
旅行规划助手 | 下次更新: 明天
"""
        
        # 保存报告
        report_file = os.path.join(REPORTS_DIR, f"daily_{today}.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.state['reports']['last_daily_update'] = today
        self.save_state()
        
        return report
    
    def generate_weekly_report(self):
        """生成每周报告"""
        today = datetime.now()
        week_start = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
        week_end = (today + timedelta(days=6-today.weekday())).strftime("%Y-%m-%d")
        
        # 计算本周价格趋势
        prices = self.scan_prices()
        
        report = f"""
========================================
[旅行计划周报]
{week_start} ~ {week_end}
========================================

[预算概览]
年度总预算:     {self.state['budget_total']:,} CNY
当前已使用:     {self.state.get('budget_used', 0):,} CNY
剩余可用:       {self.state.get('budget_remaining', self.state['budget_total']):,} CNY
使用进度:       {self.state.get('budget_used', 0) / self.state['budget_total'] * 100:.1f}%

[已规划行程]
"""
        
        periods = self.state.get('travel_periods', [])
        if periods:
            for i, p in enumerate(periods, 1):
                report += f"\n{i}. {p.get('destination', '未指定')}"
                report += f"\n   时间: {p.get('start_date', '待定')} ~ {p.get('end_date', '待定')}"
                report += f"\n   预算: {p.get('budget', 0):,} CNY"
        else:
            report += "\n暂无规划行程"
        
        report += f"""

[价格监控总结] ({len(prices)}条路线)
"""
        
        if prices:
            low_prices = [p for p in prices if p['trend'] == 'down']
            report += f"\n[降价] 本周降价路线: {len(low_prices)}条"
            report += f"\n[涨价] 本周涨价路线: {len(prices) - len(low_prices)}条"
            
            if low_prices:
                report += "\n\n[推荐关注] (价格下降):"
                for p in low_prices[:3]:
                    report += f"\n   - {p['route']}: {p['current_price']:,} CNY"
        
        report += f"""

[下周计划建议]
{self.get_weekly_recommendation()}

========================================
旅行规划助手 | 下周再见！
========================================
"""
        
        # 保存报告
        report_file = os.path.join(REPORTS_DIR, f"weekly_{week_start}.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.state['reports']['last_weekly_report'] = week_start
        self.save_state()
        
        return report
    
    def get_daily_tip(self):
        """获取每日建议"""
        tips = [
            "建议提前2-3个月关注目标航线价格走势",
            "周二、周三出发的机票通常更便宜",
            "酒店价格周末通常上涨20-30%",
            "考虑淡季出行可节省30-50%预算",
            "关注航空公司会员日促销活动"
        ]
        return random.choice(tips)
    
    def get_weekly_recommendation(self):
        """获取每周建议"""
        remaining = self.state.get('budget_remaining', self.state['budget_total'])
        if remaining > 100000:
            return "预算充足，可考虑长途国际旅行或提升住宿标准"
        elif remaining > 50000:
            return "预算适中，建议规划2-3次中短途旅行"
        else:
            return "预算紧张，建议关注特价机票和错峰出行"
    
    def add_route(self, origin, destination, date=None):
        """添加追踪路线"""
        route = {
            "origin": origin,
            "destination": destination,
            "date": date or "flexible",
            "added_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        if 'tracked_routes' not in self.state:
            self.state['tracked_routes'] = []
        
        self.state['tracked_routes'].append(route)
        self.save_state()
        return f"Added route: {origin} -> {destination}"
    
    def add_travel_period(self, destination, start_date, end_date, budget):
        """添加旅行计划"""
        period = {
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "budget": budget
        }
        
        if 'travel_periods' not in self.state:
            self.state['travel_periods'] = []
        
        self.state['travel_periods'].append(period)
        
        # 更新预算
        self.state['budget_used'] = self.state.get('budget_used', 0) + budget
        self.state['budget_remaining'] = self.state['budget_total'] - self.state['budget_used']
        
        self.save_state()
        return f"Added trip: {destination} ({start_date} ~ {end_date}) Budget: {budget:,} CNY"

def main():
    import sys
    planner = TravelPlanner()
    
    if len(sys.argv) < 2:
        print("用法: python travel_planner.py <command> [args]")
        print("\n命令:")
        print("  daily          - 生成每日更新")
        print("  weekly         - 生成每周报告")
        print("  add-route <出发地> <目的地> [日期]  - 添加追踪路线")
        print("  add-trip <目的地> <开始日期> <结束日期> <预算> - 添加旅行计划")
        print("  status         - 查看当前状态")
        return
    
    command = sys.argv[1]
    
    if command == "daily":
        print(planner.generate_daily_update())
    elif command == "weekly":
        print(planner.generate_weekly_report())
    elif command == "add-route" and len(sys.argv) >= 4:
        print(planner.add_route(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None))
    elif command == "add-trip" and len(sys.argv) >= 6:
        print(planner.add_travel_period(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])))
    elif command == "status":
        print(json.dumps(planner.state, ensure_ascii=False, indent=2))
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
