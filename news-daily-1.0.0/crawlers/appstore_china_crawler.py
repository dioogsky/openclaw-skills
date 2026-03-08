#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Store大陆区榜单爬虫
通过爬取App Store网页获取大陆区iOS榜单
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class AppStoreChinaCrawler:
    """App Store大陆区爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_free_rankings(self, count=10):
        """获取大陆区免费榜"""
        url = "https://apps.apple.com/cn/charts/iphone"
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            apps = []
            # 查找App排行列表
            app_list = soup.select('section:has(h1:-soup-contains("App 排行")) ul li')[:count]
            
            for i, item in enumerate(app_list, 1):
                try:
                    # 提取应用名称
                    name_elem = item.find('h3')
                    name = name_elem.text.strip() if name_elem else 'Unknown'
                    
                    # 提取描述
                    desc_elem = item.find('p')
                    description = desc_elem.text.strip() if desc_elem else ''
                    
                    # 提取链接
                    link_elem = item.find('a', href=True)
                    url = link_elem['href'] if link_elem else ''
                    
                    apps.append({
                        'rank': i,
                        'name': name,
                        'description': description,
                        'url': url
                    })
                except:
                    continue
            
            return apps
            
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def fetch_game_rankings(self, count=10):
        """获取大陆区游戏榜"""
        url = "https://apps.apple.com/cn/charts/iphone"
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            apps = []
            # 查找游戏排行列表
            game_list = soup.select('section:has(h1:-soup-contains("游戏排行")) ul li')[:count]
            
            for i, item in enumerate(game_list, 1):
                try:
                    name_elem = item.find('h3')
                    name = name_elem.text.strip() if name_elem else 'Unknown'
                    
                    desc_elem = item.find('p')
                    description = desc_elem.text.strip() if desc_elem else ''
                    
                    link_elem = item.find('a', href=True)
                    url = link_elem['href'] if link_elem else ''
                    
                    apps.append({
                        'rank': i,
                        'name': name,
                        'description': description,
                        'url': url
                    })
                except:
                    continue
            
            return apps
            
        except Exception as e:
            print(f"Error: {e}")
            return []


def main():
    crawler = AppStoreChinaCrawler()
    
    print("=" * 60)
    print(f"App Store大陆区榜单 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 免费榜
    print("\n[免费榜 TOP10]")
    print("-" * 60)
    apps = crawler.fetch_free_rankings(10)
    for app in apps:
        print(f"{app['rank']:2d}. {app['name']}")
        print(f"    {app['description']}")


if __name__ == "__main__":
    main()
