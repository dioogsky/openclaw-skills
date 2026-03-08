#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS App Store 榜单爬虫
使用公开API获取免费榜、付费榜数据
"""

import requests
import json
import re
from datetime import datetime

class IOSRankCrawler:
    """iOS榜单爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_free_rankings(self, count=10):
        """获取iOS免费榜（使用香港区，包含大陆热门应用）"""
        # App Store RSS feed for top free apps (香港区，数据包含大陆应用)
        url = f"https://itunes.apple.com/hk/rss/topfreeapplications/limit={count}/json"
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            response.raise_for_status()
            data = response.json()
            
            apps = []
            entries = data.get('feed', {}).get('entry', [])
            
            for i, entry in enumerate(entries, 1):
                # 安全获取字段
                name = entry.get('im:name', {}).get('label', 'Unknown')
                category = entry.get('category', {}).get('attributes', {}).get('label', 'Unknown')
                developer = entry.get('im:artist', {}).get('label', 'Unknown')
                app_id = entry.get('id', {}).get('attributes', {}).get('im:id', '')
                price = entry.get('im:price', {}).get('label', '免费')
                summary = entry.get('summary', {}).get('label', '')
                
                # 确保是字符串
                name = str(name) if name else 'Unknown'
                category = str(category) if category else 'Unknown'
                developer = str(developer) if developer else 'Unknown'
                price = str(price) if price else '免费'
                summary = str(summary)[:100] + '...' if summary else ''
                
                app = {
                    'rank': i,
                    'name': name,
                    'category': category,
                    'developer': developer,
                    'app_id': app_id,
                    'price': price,
                    'summary': summary
                }
                apps.append(app)
            
            return apps
            
        except Exception as e:
            print(f"Error fetching free rankings: {e}")
            return []
    
    def fetch_paid_rankings(self, count=10):
        """获取iOS付费榜（使用香港区，包含大陆热门应用）"""
        # App Store RSS feed for top paid apps (香港区，数据包含大陆应用)
        url = f"https://itunes.apple.com/hk/rss/toppaidapplications/limit={count}/json"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            apps = []
            entries = data.get('feed', {}).get('entry', [])
            
            for i, entry in enumerate(entries, 1):
                app = {
                    'rank': i,
                    'name': entry.get('im:name', {}).get('label', 'Unknown'),
                    'category': entry.get('category', {}).get('attributes', {}).get('label', 'Unknown'),
                    'developer': entry.get('im:artist', {}).get('label', 'Unknown'),
                    'app_id': entry.get('id', {}).get('attributes', {}).get('im:id', ''),
                    'price': entry.get('im:price', {}).get('label', '¥6.00'),
                    'summary': entry.get('summary', {}).get('label', '')[:100] + '...' if entry.get('summary', {}).get('label', '') else ''
                }
                apps.append(app)
            
            return apps
            
        except Exception as e:
            print(f"Error fetching paid rankings: {e}")
            return []
    
    def fetch_grossing_rankings(self, count=10):
        """获取iOS畅销榜（使用香港区，包含大陆热门应用）"""
        # App Store RSS feed for top grossing apps (香港区，数据包含大陆应用)
        url = f"https://itunes.apple.com/hk/rss/topgrossingapplications/limit={count}/json"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            apps = []
            entries = data.get('feed', {}).get('entry', [])
            
            for i, entry in enumerate(entries, 1):
                app = {
                    'rank': i,
                    'name': entry.get('im:name', {}).get('label', 'Unknown'),
                    'category': entry.get('category', {}).get('attributes', {}).get('label', 'Unknown'),
                    'developer': entry.get('im:artist', {}).get('label', 'Unknown'),
                    'app_id': entry.get('id', {}).get('attributes', {}).get('im:id', ''),
                    'price': entry.get('im:price', {}).get('label', '免费'),
                    'summary': entry.get('summary', {}).get('label', '')[:100] + '...' if entry.get('summary', {}).get('label', '') else ''
                }
                apps.append(app)
            
            return apps
            
        except Exception as e:
            print(f"Error fetching grossing rankings: {e}")
            return []
    
    def analyze_trends(self, current_data, previous_data=None):
        """分析榜单趋势"""
        analysis = {
            'total_apps': len(current_data),
            'categories': {},
            'top_developers': {},
            'price_distribution': {'free': 0, 'paid': 0}
        }
        
        for app in current_data:
            # 统计分类
            cat = app.get('category', 'Unknown')
            analysis['categories'][cat] = analysis['categories'].get(cat, 0) + 1
            
            # 统计开发商
            dev = app.get('developer', 'Unknown')
            analysis['top_developers'][dev] = analysis['top_developers'].get(dev, 0) + 1
            
            # 统计价格
            price = app.get('price', '免费')
            if '免费' in price or price == '免费':
                analysis['price_distribution']['free'] += 1
            else:
                analysis['price_distribution']['paid'] += 1
        
        return analysis


def main():
    """测试爬虫"""
    crawler = IOSRankCrawler()
    
    print("=" * 60)
    print(f"iOS App Store 榜单 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 获取免费榜
    print("\n[免费榜 TOP10]")
    print("-" * 60)
    free_apps = crawler.fetch_free_rankings(10)
    for app in free_apps:
        print(f"{app['rank']:2d}. {app['name']}")
        print(f"    分类: {app['category']} | 开发商: {app['developer']}")
    
    # 获取付费榜
    print("\n[付费榜 TOP10]")
    print("-" * 60)
    paid_apps = crawler.fetch_paid_rankings(10)
    for app in paid_apps:
        print(f"{app['rank']:2d}. {app['name']}")
        print(f"    分类: {app['category']} | 价格: {app['price']}")
    
    # 获取畅销榜
    print("\n[畅销榜 TOP10]")
    print("-" * 60)
    grossing_apps = crawler.fetch_grossing_rankings(10)
    for app in grossing_apps:
        print(f"{app['rank']:2d}. {app['name']}")
        print(f"    分类: {app['category']} | 开发商: {app['developer']}")
    
    # 分析趋势
    print("\n[榜单分析]")
    print("-" * 60)
    analysis = crawler.analyze_trends(free_apps)
    print(f"免费榜应用总数: {analysis['total_apps']}")
    print(f"分类分布: {dict(sorted(analysis['categories'].items(), key=lambda x: x[1], reverse=True)[:5])}")


if __name__ == "__main__":
    main()
