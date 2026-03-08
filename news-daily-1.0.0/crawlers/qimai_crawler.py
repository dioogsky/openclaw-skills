#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七麦数据iOS榜单爬虫
使用七麦数据API获取大陆区iOS榜单
"""

import requests
import json
import time
import base64
from datetime import datetime
from urllib.parse import urlencode

class QimaiCrawler:
    """七麦数据爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.qimai.cn/rank',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.base_url = "https://api.qimai.cn"
    
    def _encrypt(self, params_str):
        """
        七麦数据加密函数
        根据腾讯云文章提供的加密方法
        """
        e = '00000008d78d46a'
        t = len(e)
        n = len(params_str)
        a = list(params_str)
        for s in range(n):
            a[s] = chr(ord(a[s]) ^ ord(e[(s + 10) % t]))
        return ''.join(a)
    
    def _get_analysis(self, params):
        """生成analysis参数"""
        # 将参数排序并转为字符串
        sorted_params = sorted(params.items())
        params_str = urlencode(sorted_params)
        
        # 加密
        encrypted = self._encrypt(params_str)
        
        # base64编码
        analysis = base64.b64encode(encrypted.encode()).decode()
        
        return analysis
    
    def fetch_rankings(self, rank_type='free', count=10):
        """
        获取iOS榜单
        
        rank_type: free(免费榜), paid(付费榜), grossing(畅销榜)
        """
        # 构建参数
        params = {
            'brand': 'all',
            'country': 'cn',  # 大陆区
            'date': datetime.now().strftime('%Y-%m-%d'),
            'device': 'iphone',
            'genre': '36',  # 所有类别
            'page': 1,
            'is_rank_index': 1
        }
        
        # 根据榜单类型设置不同参数
        if rank_type == 'free':
            params['rankType'] = 'free'
        elif rank_type == 'paid':
            params['rankType'] = 'paid'
        elif rank_type == 'grossing':
            params['rankType'] = 'grossing'
        
        try:
            # 生成analysis
            analysis = self._get_analysis(params)
            params['analysis'] = analysis
            
            # 发送请求
            url = f"{self.base_url}/rank/indexPlus/brand_id/1"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('code') == 200:
                apps = []
                rank_list = data.get('data', {}).get('list', [])[:count]
                
                for i, item in enumerate(rank_list, 1):
                    app = {
                        'rank': i,
                        'name': item.get('appInfo', {}).get('appName', 'Unknown'),
                        'app_id': item.get('appInfo', {}).get('appId', ''),
                        'developer': item.get('appInfo', {}).get('developerName', 'Unknown'),
                        'category': item.get('appInfo', {}).get('genre', 'Unknown'),
                        'icon': item.get('appInfo', {}).get('icon', ''),
                        'rating': item.get('appInfo', {}).get('rating', ''),
                        'comment_count': item.get('appInfo', {}).get('commentCount', ''),
                        'price': item.get('appInfo', {}).get('price', '免费'),
                        'change': item.get('change', 0),  # 排名变化
                    }
                    apps.append(app)
                
                return apps
            else:
                print(f"API Error: {data.get('msg', 'Unknown error')}")
                return []
                
        except Exception as e:
            print(f"Error fetching {rank_type} rankings: {e}")
            return []
    
    def fetch_free_rankings(self, count=10):
        """获取免费榜"""
        return self.fetch_rankings('free', count)
    
    def fetch_paid_rankings(self, count=10):
        """获取付费榜"""
        return self.fetch_rankings('paid', count)
    
    def fetch_grossing_rankings(self, count=10):
        """获取畅销榜"""
        return self.fetch_rankings('grossing', count)
    
    def fetch_game_rankings(self, count=10):
        """获取游戏榜单"""
        params = {
            'brand': 'all',
            'country': 'cn',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'device': 'iphone',
            'genre': '6014',  # 游戏类别
            'page': 1,
            'is_rank_index': 1,
            'rankType': 'free'
        }
        
        try:
            analysis = self._get_analysis(params)
            params['analysis'] = analysis
            
            url = f"{self.base_url}/rank/indexPlus/brand_id/1"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('code') == 200:
                apps = []
                rank_list = data.get('data', {}).get('list', [])[:count]
                
                for i, item in enumerate(rank_list, 1):
                    app = {
                        'rank': i,
                        'name': item.get('appInfo', {}).get('appName', 'Unknown'),
                        'app_id': item.get('appInfo', {}).get('appId', ''),
                        'developer': item.get('appInfo', {}).get('developerName', 'Unknown'),
                        'category': '游戏',
                        'icon': item.get('appInfo', {}).get('icon', ''),
                        'rating': item.get('appInfo', {}).get('rating', ''),
                        'change': item.get('change', 0),
                    }
                    apps.append(app)
                
                return apps
            else:
                return []
                
        except Exception as e:
            print(f"Error fetching game rankings: {e}")
            return []


def main():
    """测试爬虫"""
    crawler = QimaiCrawler()
    
    print("=" * 60)
    print(f"七麦数据iOS榜单 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 免费榜
    print("\n[大陆区免费榜 TOP10]")
    print("-" * 60)
    apps = crawler.fetch_free_rankings(10)
    for app in apps:
        change_str = ""
        if app['change'] > 0:
            change_str = f" [+{app['change']}]"
        elif app['change'] < 0:
            change_str = f" [{app['change']}]"
        else:
            change_str = " [=]"
        
        print(f"{app['rank']:2d}. {app['name']}")
        print(f"    开发商: {app['developer']} | 评分: {app['rating']}{change_str}")
    
    # 付费榜
    print("\n[大陆区付费榜 TOP10]")
    print("-" * 60)
    apps = crawler.fetch_paid_rankings(10)
    for app in apps:
        change_str = ""
        if app['change'] > 0:
            change_str = f" [+{app['change']}]"
        elif app['change'] < 0:
            change_str = f" [{app['change']}]"
        else:
            change_str = " [=]"
        
        print(f"{app['rank']:2d}. {app['name']}")
        print(f"    价格: {app['price']} | 评分: {app['rating']}{change_str}")
    
    # 游戏榜
    print("\n[游戏免费榜 TOP10]")
    print("-" * 60)
    apps = crawler.fetch_game_rankings(10)
    for app in apps:
        change_str = ""
        if app['change'] > 0:
            change_str = f" [+{app['change']}]"
        elif app['change'] < 0:
            change_str = f" [{app['change']}]"
        else:
            change_str = " [=]"
        
        print(f"{app['rank']:2d}. {app['name']}")
        print(f"    开发商: {app['developer']} | 评分: {app['rating']}{change_str}")


if __name__ == "__main__":
    main()
