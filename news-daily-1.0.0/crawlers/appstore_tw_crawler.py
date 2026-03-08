#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Store iOS榜单爬虫（台湾区）
台湾区数据包含大陆热门应用，且应用名称为简体中文
"""

import requests
import json
from datetime import datetime

class AppStoreTWCrawler:
    """App Store台湾区爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_free_rankings(self, count=10):
        """获取iOS免费榜（台湾区）"""
        url = f"https://itunes.apple.com/tw/rss/topfreeapplications/limit={count}/json"
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            response.raise_for_status()
            data = response.json()
            
            apps = []
            entries = data.get('feed', {}).get('entry', [])
            
            for i, entry in enumerate(entries, 1):
                name = entry.get('im:name', {}).get('label', 'Unknown')
                category = entry.get('category', {}).get('attributes', {}).get('label', 'Unknown')
                developer = entry.get('im:artist', {}).get('label', 'Unknown')
                app_id = entry.get('id', {}).get('attributes', {}).get('im:id', '')
                price = entry.get('im:price', {}).get('label', '免費')
                
                app = {
                    'rank': i,
                    'name': str(name),
                    'category': str(category),
                    'developer': str(developer),
                    'app_id': app_id,
                    'price': str(price),
                }
                apps.append(app)
            
            return apps
            
        except Exception as e:
            print(f"Error fetching free rankings: {e}")
            return []
    
    def fetch_paid_rankings(self, count=10):
        """获取iOS付费榜（台湾区）"""
        url = f"https://itunes.apple.com/tw/rss/toppaidapplications/limit={count}/json"
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            response.raise_for_status()
            data = response.json()
            
            apps = []
            entries = data.get('feed', {}).get('entry', [])
            
            for i, entry in enumerate(entries, 1):
                name = entry.get('im:name', {}).get('label', 'Unknown')
                category = entry.get('category', {}).get('attributes', {}).get('label', 'Unknown')
                developer = entry.get('im:artist', {}).get('label', 'Unknown')
                app_id = entry.get('id', {}).get('attributes', {}).get('im:id', '')
                price = entry.get('im:price', {}).get('label', 'NT$30.00')
                
                app = {
                    'rank': i,
                    'name': str(name),
                    'category': str(category),
                    'developer': str(developer),
                    'app_id': app_id,
                    'price': str(price),
                }
                apps.append(app)
            
            return apps
            
        except Exception as e:
            print(f"Error fetching paid rankings: {e}")
            return []
    
    def fetch_grossing_rankings(self, count=10):
        """获取iOS畅销榜（台湾区）"""
        url = f"https://itunes.apple.com/tw/rss/topgrossingapplications/limit={count}/json"
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            response.raise_for_status()
            data = response.json()
            
            apps = []
            entries = data.get('feed', {}).get('entry', [])
            
            for i, entry in enumerate(entries, 1):
                name = entry.get('im:name', {}).get('label', 'Unknown')
                category = entry.get('category', {}).get('attributes', {}).get('label', 'Unknown')
                developer = entry.get('im:artist', {}).get('label', 'Unknown')
                app_id = entry.get('id', {}).get('attributes', {}).get('im:id', '')
                
                app = {
                    'rank': i,
                    'name': str(name),
                    'category': str(category),
                    'developer': str(developer),
                    'app_id': app_id,
                    'price': '免費',
                }
                apps.append(app)
            
            return apps
            
        except Exception as e:
            print(f"Error fetching grossing rankings: {e}")
            return []


def main():
    """测试爬虫"""
    crawler = AppStoreTWCrawler()
    
    print("=" * 60)
    print(f"App Store iOS榜单（台湾区）- {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 免费榜
    print("\n[免费榜 TOP10]")
    print("-" * 60)
    apps = crawler.fetch_free_rankings(10)
    for app in apps:
        print(f"{app['rank']:2d}. {app['name']}")
        print(f"    分类: {app['category']} | 开发商: {app['developer']}")
    
    # 付费榜
    print("\n[付费榜 TOP10]")
    print("-" * 60)
    apps = crawler.fetch_paid_rankings(10)
    for app in apps:
        print(f"{app['rank']:2d}. {app['name']}")
        print(f"    价格: {app['price']} | 开发商: {app['developer']}")


if __name__ == "__main__":
    main()
