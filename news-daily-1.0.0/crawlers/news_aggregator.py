#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一新闻收集器
整合iOS榜单、游戏新闻、AI新闻爬虫
"""

import os
import sys
import json
from datetime import datetime

# 添加爬虫目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from ios_rank_crawler import IOSRankCrawler
from game_news_crawler import GameNewsCrawler
from ai_news_crawler import AINewsCrawler

class NewsAggregator:
    """新闻聚合器"""
    
    def __init__(self):
        self.ios_crawler = IOSRankCrawler()
        self.game_crawler = GameNewsCrawler()
        self.ai_crawler = AINewsCrawler()
        
        # 数据保存目录
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def collect_ios_rankings(self, count=10):
        """收集iOS榜单数据"""
        print("[INFO] 正在收集iOS榜单数据...")
        
        data = {
            'free': self.ios_crawler.fetch_free_rankings(count),
            'paid': self.ios_crawler.fetch_paid_rankings(count),
            'grossing': self.ios_crawler.fetch_grossing_rankings(count),
            'collected_at': datetime.now().isoformat()
        }
        
        # 保存数据
        self._save_data('ios_rankings', data)
        
        print(f"[OK] iOS榜单数据收集完成: {len(data['free'])}个免费应用, {len(data['paid'])}个付费应用")
        return data
    
    def collect_game_news(self, count_per_source=3):
        """收集游戏新闻"""
        print("[INFO] 正在收集游戏新闻...")
        
        news = self.game_crawler.fetch_all_gaming_news(count_per_source)
        
        # 分离国内和海外新闻
        china_news = [n for n in news if n['source'] in ['游民星空', '3DM', '17173']]
        usa_news = [n for n in news if n['source'] in ['IGN']]
        
        data = {
            'china': china_news,
            'usa': usa_news,
            'all': news,
            'collected_at': datetime.now().isoformat()
        }
        
        # 保存数据
        self._save_data('game_news', data)
        
        print(f"[OK] 游戏新闻收集完成: {len(china_news)}条国内, {len(usa_news)}条海外")
        return data
    
    def collect_ai_news(self, count_per_source=3):
        """收集AI新闻"""
        print("[INFO] 正在收集AI新闻...")
        
        news = self.ai_crawler.fetch_all_ai_news(count_per_source)
        
        # 分离国内和海外新闻
        china_news = [n for n in news if n['source'] in ['机器之心', '量子位', '知乎热榜']]
        usa_news = [n for n in news if n['source'] in ['TechCrunch']]
        
        data = {
            'china': china_news,
            'usa': usa_news,
            'all': news,
            'collected_at': datetime.now().isoformat()
        }
        
        # 保存数据
        self._save_data('ai_news', data)
        
        print(f"[OK] AI新闻收集完成: {len(china_news)}条国内, {len(usa_news)}条海外")
        return data
    
    def collect_all(self, ios_count=10, news_count=3):
        """收集所有数据"""
        print("=" * 60)
        print(f"[开始收集] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        result = {
            'ios_rankings': self.collect_ios_rankings(ios_count),
            'game_news': self.collect_game_news(news_count),
            'ai_news': self.collect_ai_news(news_count),
            'collected_at': datetime.now().isoformat()
        }
        
        # 保存完整数据
        self._save_data('all_news', result)
        
        print("=" * 60)
        print("[完成] 所有数据收集完成")
        print("=" * 60)
        
        return result
    
    def _save_data(self, name, data):
        """保存数据到文件"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{name}_{date_str}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[SAVE] 数据已保存: {filepath}")
    
    def generate_daily_report(self):
        """生成每日新闻报告"""
        # 收集数据
        data = self.collect_all(ios_count=10, news_count=3)
        
        # 生成报告
        report_lines = [
            f"[每日科技要闻] {datetime.now().strftime('%Y-%m-%d')}",
            "",
            "=" * 50,
            "",
        ]
        
        # iOS榜单
        report_lines.extend([
            "[iOS免费榜 TOP10]",
            "-" * 50,
        ])
        for app in data['ios_rankings']['free'][:10]:
            report_lines.append(f"{app['rank']:2d}. {app['name']} ({app['category']})")
        
        report_lines.extend([
            "",
            "[iOS付费榜 TOP10]",
            "-" * 50,
        ])
        for app in data['ios_rankings']['paid'][:10]:
            report_lines.append(f"{app['rank']:2d}. {app['name']} ({app['price']})")
        
        # AI新闻
        report_lines.extend([
            "",
            "=" * 50,
            "",
            "[中国AI新闻]",
            "-" * 50,
        ])
        for news in data['ai_news']['china'][:5]:
            report_lines.append(f"• {news['title']}")
            report_lines.append(f"  来源: {news['source']}")
            report_lines.append("")
        
        report_lines.extend([
            "[海外AI新闻]",
            "-" * 50,
        ])
        for news in data['ai_news']['usa'][:5]:
            report_lines.append(f"• {news['title']}")
            report_lines.append(f"  来源: {news['source']}")
            report_lines.append("")
        
        # 游戏新闻
        report_lines.extend([
            "=" * 50,
            "",
            "[中国游戏新闻]",
            "-" * 50,
        ])
        for news in data['game_news']['china'][:3]:
            report_lines.append(f"• {news['title']}")
            report_lines.append(f"  来源: {news['source']}")
            report_lines.append("")
        
        report_lines.extend([
            "[海外游戏新闻]",
            "-" * 50,
        ])
        for news in data['game_news']['usa'][:3]:
            report_lines.append(f"• {news['title']}")
            report_lines.append(f"  来源: {news['source']}")
            report_lines.append("")
        
        report_lines.extend([
            "=" * 50,
            "",
            "[提示] 以上数据由AI助手小智实时爬取整理",
        ])
        
        report = "\n".join(report_lines)
        
        # 保存报告
        date_str = datetime.now().strftime('%Y-%m-%d')
        report_file = os.path.join(self.data_dir, f'daily_report_{date_str}.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n[REPORT] 报告已生成: {report_file}")
        
        return report


def main():
    """主函数"""
    aggregator = NewsAggregator()
    
    # 生成每日报告
    report = aggregator.generate_daily_report()
    
    print("\n" + "=" * 60)
    print("每日新闻报告")
    print("=" * 60)
    print(report)


if __name__ == "__main__":
    main()
