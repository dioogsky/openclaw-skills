#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finance Manager - 理财助手
支持记账、预算管理、投资追踪和财务分析
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid
import re

# 配置
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SKILL_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "finance.json")

# 默认配置
CATEGORIES = {
    "food": {"name": "餐饮", "icon": "[F]", "color": "orange"},
    "transport": {"name": "交通", "icon": "[T]", "color": "blue"},
    "shopping": {"name": "购物", "icon": "[S]", "color": "pink"},
    "entertainment": {"name": "娱乐", "icon": "[E]", "color": "purple"},
    "housing": {"name": "居住", "icon": "[H]", "color": "brown"},
    "medical": {"name": "医疗", "icon": "[M]", "color": "red"},
    "education": {"name": "教育", "icon": "[Ed]", "color": "green"},
    "investment": {"name": "投资", "icon": "[I]", "color": "gold"},
    "salary": {"name": "工资", "icon": "[$]", "color": "green"},
    "other": {"name": "其他", "icon": "[O]", "color": "gray"}
}

class FinanceManager:
    """理财管理器"""
    
    def __init__(self):
        self._ensure_dirs()
        self.data = self._load_data()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        os.makedirs(DATA_DIR, exist_ok=True)
    
    def _load_data(self) -> Dict:
        """加载数据"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "transactions": [],
            "budgets": {},
            "investments": [],
            "created_at": datetime.now().isoformat()
        }
    
    def _save_data(self):
        """保存数据"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_transaction(self, amount: float, category: str, 
                       note: str = "", transaction_type: str = "expense") -> Dict:
        """添加交易记录"""
        transaction = {
            "id": str(uuid.uuid4())[:8],
            "amount": amount,
            "category": category,
            "note": note,
            "type": transaction_type,  # expense 或 income
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "created_at": datetime.now().isoformat()
        }
        
        self.data["transactions"].append(transaction)
        self._save_data()
        
        return transaction
    
    def parse_voice_input(self, text: str) -> Optional[Dict]:
        """解析语音输入"""
        # 简单的正则匹配
        # 匹配 "花了XX元/块买XX" 或 "收入XX元/块"
        expense_pattern = r'(?:花|用|消费)了?(\d+(?:\.\d+)?)(?:元|块|块钱)(?:买|用于)?(.+)?'
        income_pattern = r'(?:收入|收到|入账)(\d+(?:\.\d+)?)(?:元|块|块钱)(?:来自)?(.+)?'
        
        expense_match = re.search(expense_pattern, text)
        income_match = re.search(income_pattern, text)
        
        if expense_match:
            amount = float(expense_match.group(1))
            note = expense_match.group(2) if expense_match.group(2) else ""
            # 根据关键词判断分类
            category = self._guess_category(note)
            return {"amount": amount, "category": category, "note": note, "transaction_type": "expense"}
        
        if income_match:
            amount = float(income_match.group(1))
            note = income_match.group(2) if income_match.group(2) else ""
            return {"amount": amount, "category": "salary", "note": note, "transaction_type": "income"}
        
        return None
    
    def _guess_category(self, note: str) -> str:
        """根据备注猜测分类"""
        keywords = {
            "food": ["饭", "餐", "吃", "菜", "肉", "水果", "零食", "奶茶", "咖啡"],
            "transport": ["车", "地铁", "公交", "打车", "油费", "停车", "高铁", "飞机"],
            "shopping": ["买", "购物", "衣服", "鞋", "包", "化妆品", "超市", "淘宝", "京东"],
            "entertainment": ["电影", "游戏", "KTV", "聚会", "玩", "娱乐"],
            "housing": ["房租", "水电", "物业", "装修", "家"],
            "medical": ["药", "医院", "看病", "体检", "医疗"],
            "education": ["书", "课程", "学习", "培训", "学费"]
        }
        
        for category, words in keywords.items():
            for word in words:
                if word in note:
                    return category
        
        return "other"
    
    def get_today_summary(self) -> Dict:
        """获取今日收支汇总"""
        today = datetime.now().strftime("%Y-%m-%d")
        transactions = [t for t in self.data["transactions"] if t["date"] == today]
        
        expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        income = sum(t["amount"] for t in transactions if t["type"] == "income")
        
        return {
            "date": today,
            "expense": expense,
            "income": income,
            "balance": income - expense,
            "count": len(transactions)
        }
    
    def get_monthly_report(self, year_month: str) -> Dict:
        """获取月度报表"""
        transactions = [t for t in self.data["transactions"] if t["date"].startswith(year_month)]
        
        expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        income = sum(t["amount"] for t in transactions if t["type"] == "income")
        
        # 按分类统计
        category_stats = {}
        for t in transactions:
            cat = t["category"]
            if cat not in category_stats:
                category_stats[cat] = {"expense": 0, "income": 0, "count": 0}
            category_stats[cat][t["type"]] += t["amount"]
            category_stats[cat]["count"] += 1
        
        return {
            "month": year_month,
            "expense": expense,
            "income": income,
            "balance": income - expense,
            "transaction_count": len(transactions),
            "by_category": category_stats
        }
    
    def set_budget(self, category: str, amount: float, period: str = "monthly"):
        """设置预算"""
        self.data["budgets"][category] = {
            "amount": amount,
            "period": period,
            "set_at": datetime.now().isoformat()
        }
        self._save_data()
    
    def get_budget_status(self) -> List[Dict]:
        """获取预算执行情况"""
        today = datetime.now()
        year_month = today.strftime("%Y-%m-%d")[:7]  # YYYY-MM
        
        results = []
        for category, budget in self.data["budgets"].items():
            # 计算本月该分类支出
            spent = sum(t["amount"] for t in self.data["transactions"] 
                       if t["category"] == category 
                       and t["type"] == "expense"
                       and t["date"].startswith(year_month))
            
            remaining = budget["amount"] - spent
            percentage = (spent / budget["amount"] * 100) if budget["amount"] > 0 else 0
            
            results.append({
                "category": category,
                "budget": budget["amount"],
                "spent": spent,
                "remaining": remaining,
                "percentage": round(percentage, 1)
            })
        
        return results
    
    def add_investment(self, name: str, amount: float, invest_type: str, 
                      price: float = 0, note: str = "") -> Dict:
        """添加投资记录"""
        investment = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "amount": amount,
            "type": invest_type,
            "price": price,
            "note": note,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "created_at": datetime.now().isoformat()
        }
        
        self.data["investments"].append(investment)
        self._save_data()
        
        return investment
    
    def get_investment_summary(self) -> Dict:
        """获取投资汇总"""
        total = sum(i["amount"] for i in self.data["investments"])
        
        by_type = {}
        for i in self.data["investments"]:
            t = i["type"]
            if t not in by_type:
                by_type[t] = {"count": 0, "amount": 0}
            by_type[t]["count"] += 1
            by_type[t]["amount"] += i["amount"]
        
        return {
            "total_investment": total,
            "count": len(self.data["investments"]),
            "by_type": by_type
        }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Finance Manager - 理财助手")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    manager = FinanceManager()
    
    # add 命令 - 添加支出
    add_parser = subparsers.add_parser("add", help="添加支出")
    add_parser.add_argument("-a", "--amount", type=float, required=True, help="金额")
    add_parser.add_argument("-c", "--category", required=True, help="分类")
    add_parser.add_argument("-n", "--note", default="", help="备注")
    add_parser.add_argument("-t", "--type", default="expense", choices=["expense", "income"], help="类型")
    
    # voice 命令 - 语音记账
    voice_parser = subparsers.add_parser("voice", help="语音记账")
    voice_parser.add_argument("text", help="语音文本")
    
    # today 命令
    subparsers.add_parser("today", help="今日收支")
    
    # report 命令
    report_parser = subparsers.add_parser("report", help="月度报表")
    report_parser.add_argument("--month", default=datetime.now().strftime("%Y-%m"), help="月份 (YYYY-MM)")
    
    # budget 命令
    budget_parser = subparsers.add_parser("budget", help="设置预算")
    budget_parser.add_argument("-c", "--category", required=True, help="分类")
    budget_parser.add_argument("-a", "--amount", type=float, required=True, help="金额")
    budget_parser.add_argument("-p", "--period", default="monthly", help="周期")
    
    # budget-status 命令
    subparsers.add_parser("budget-status", help="预算执行情况")
    
    # invest 命令
    invest_parser = subparsers.add_parser("invest", help="添加投资")
    invest_parser.add_argument("-n", "--name", required=True, help="名称")
    invest_parser.add_argument("-a", "--amount", type=float, required=True, help="金额")
    invest_parser.add_argument("-t", "--type", required=True, help="类型 (stock/fund/crypto等)")
    invest_parser.add_argument("-p", "--price", type=float, default=0, help="单价")
    invest_parser.add_argument("--note", default="", help="备注")
    
    # invest-status 命令
    subparsers.add_parser("invest-status", help="投资汇总")
    
    args = parser.parse_args()
    
    if args.command == "add":
        t = manager.add_transaction(args.amount, args.category, args.note, args.type)
        cat_info = CATEGORIES.get(args.category, {})
        icon = cat_info.get("icon", "💰")
        print(f"[OK] {icon} {t['category']}: {t['amount']}元 - {t['note']}")
    
    elif args.command == "voice":
        result = manager.parse_voice_input(args.text)
        if result:
            t = manager.add_transaction(**result)
            print(f"[OK] 已记录: {t['category']} {t['amount']}元 - {t['note']}")
        else:
            print("[ERROR] 无法识别语音内容")
    
    elif args.command == "today":
        summary = manager.get_today_summary()
        print(f"[今日收支] {summary['date']}")
        print(f"  支出: {summary['expense']:.2f}元")
        print(f"  收入: {summary['income']:.2f}元")
        print(f"  结余: {summary['balance']:.2f}元")
        print(f"  笔数: {summary['count']}")
    
    elif args.command == "report":
        report = manager.get_monthly_report(args.month)
        print(f"[月度报表] {report['month']}")
        print(f"  支出: {report['expense']:.2f}元")
        print(f"  收入: {report['income']:.2f}元")
        print(f"  结余: {report['balance']:.2f}元")
        print(f"  交易: {report['transaction_count']}笔")
        print("\n[分类统计]")
        for cat, stats in report['by_category'].items():
            cat_info = CATEGORIES.get(cat, {})
            name = cat_info.get("name", cat)
            if stats['expense'] > 0:
                print(f"  {name}: {stats['expense']:.2f}元 ({stats['count']}笔)")
    
    elif args.command == "budget":
        manager.set_budget(args.category, args.amount, args.period)
        cat_info = CATEGORIES.get(args.category, {})
        name = cat_info.get("name", args.category)
        print(f"[OK] 设置预算: {name} {args.amount}元/{args.period}")
    
    elif args.command == "budget-status":
        status = manager.get_budget_status()
        print("[预算执行情况]")
        for s in status:
            cat_info = CATEGORIES.get(s["category"], {})
            name = cat_info.get("name", s["category"])
            bar = "█" * int(s["percentage"] / 10) + "░" * (10 - int(s["percentage"] / 10))
            print(f"  {name}: {bar} {s['percentage']:.1f}%")
            print(f"    预算: {s['budget']:.0f}元 | 已用: {s['spent']:.0f}元 | 剩余: {s['remaining']:.0f}元")
    
    elif args.command == "invest":
        i = manager.add_investment(args.name, args.amount, args.type, args.price, args.note)
        print(f"[OK] 添加投资: {i['name']} {i['amount']}元 ({i['type']})")
    
    elif args.command == "invest-status":
        summary = manager.get_investment_summary()
        print("[投资汇总]")
        print(f"  总投资: {summary['total_investment']:.2f}元")
        print(f"  投资数: {summary['count']}笔")
        print("\n[按类型]")
        for t, s in summary['by_type'].items():
            print(f"  {t}: {s['amount']:.2f}元 ({s['count']}笔)")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
