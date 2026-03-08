#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蝉大师iOS榜单爬虫
爬取蝉大师网站的大陆区iOS榜单数据
"""

import requests
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

class ChandashiCrawler:
    """蝉大师爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.base_url = "https://www.chandashi.com"
    
    def fetch_free_rankings(self, count=10):
        """
        获取iOS免费榜（大陆区）
        """
        url = f"{self.base_url}/ranking/index.html"
        
        try:
            # 首先访问页面获取初始数据
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            print(f"[DEBUG] 页面状态码: {response.status_code}")
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尝试从页面中提取榜单数据
            # 蝉大师通常会将数据嵌入到JavaScript或特定的HTML结构中
            
            # 方法1: 查找包含榜单数据的script标签
            scripts = soup.find_all('script')
            rank_data = []
            
            for script in scripts:
                if script.string:
                    # 查找包含rankingData或appList的脚本
                    if 'rankingData' in script.string or 'appList' in script.string:
                        # 尝试提取JSON数据
                        json_match = re.search(r'var\s+\w+\s*=\s*(\[.*?\]);', script.string, re.DOTALL)
                        if json_match:
                            try:
                                data = json.loads(json_match.group(1))
                                rank_data = self._parse_rank_data(data, count)
                                if rank_data:
                                    return rank_data
                            except:
                                pass
            
            # 方法2: 从HTML表格中提取
            rank_data = self._extract_from_html(soup, count)
            if rank_data:
                return rank_data
            
            # 方法3: 尝试调用API接口
            rank_data = self._fetch_from_api('free', count)
            if rank_data:
                return rank_data
            
            return []
            
        except Exception as e:
            print(f"[ERROR] 爬取免费榜失败: {e}")
            return []
    
    def fetch_paid_rankings(self, count=10):
        """
        获取iOS付费榜（大陆区）
        """
        return self._fetch_from_api('paid', count)
    
    def fetch_grossing_rankings(self, count=10):
        """
        获取iOS畅销榜（大陆区）
        """
        return self._fetch_from_api('grossing', count)
    
    def _parse_rank_data(self, data, count):
        """解析榜单数据"""
        apps = []
        
        for i, item in enumerate(data[:count], 1):
            try:
                app = {
                    'rank': i,
                    'name': item.get('appName') or item.get('name', 'Unknown'),
                    'app_id': item.get('appId') or item.get('id', ''),
                    'developer': item.get('developer') or item.get('publisher', 'Unknown'),
                    'category': item.get('category') or item.get('genre', 'Unknown'),
                    'icon': item.get('icon', ''),
                }
                apps.append(app)
            except:
                continue
        
        return apps
    
    def _extract_from_html(self, soup, count):
        """从HTML中提取榜单数据"""
        apps = []
        
        # 尝试多种可能的选择器
        selectors = [
            '.rank-list tr',
            '.app-rank-item',
            '.ranking-item',
            '[data-rank]',
            '.app-item'
        ]
        
        for selector in selectors:
            items = soup.select(selector)[:count]
            if items:
                for i, item in enumerate(items, 1):
                    try:
                        # 尝试提取应用名称
                        name_elem = item.select_one('.app-name, .name, h3, h4, .title')
                        name = name_elem.text.strip() if name_elem else 'Unknown'
                        
                        # 尝试提取开发商
                        dev_elem = item.select_one('.developer, .publisher, .company')
                        developer = dev_elem.text.strip() if dev_elem else 'Unknown'
                        
                        # 尝试提取类别
                        cat_elem = item.select_one('.category, .genre')
                        category = cat_elem.text.strip() if cat_elem else 'Unknown'
                        
                        app = {
                            'rank': i,
                            'name': name,
                            'developer': developer,
                            'category': category,
                        }
                        apps.append(app)
                    except:
                        continue
                
                if apps:
                    break
        
        return apps
    
    def _fetch_from_api(self, rank_type='free', count=10):
        """
        尝试从API获取数据
        蝉大师可能有未公开的API端点
        """
        # 尝试可能的API端点
        api_urls = [
            f"{self.base_url}/api/rank/list",
            f"{self.base_url}/api/ranking",
            f"{self.base_url}/data/rank",
        ]
        
        for url in api_urls:
            try:
                params = {
                    'type': rank_type,
                    'country': 'cn',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'limit': count
                }
                
                response = self.session.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == 200 or data.get('status') == 'ok':
                        apps = []
                        rank_list = data.get('data', {}).get('list', [])[:count]
                        
                        for i, item in enumerate(rank_list, 1):
                            app = {
                                'rank': i,
                                'name': item.get('appName', 'Unknown'),
                                'developer': item.get('developer', 'Unknown'),
                                'category': item.get('category', 'Unknown'),
                            }
                            apps.append(app)
                        
                        if apps:
                            return apps
                            
            except:
                continue
        
        return []


def main():
    """测试爬虫"""
    print("=" * 60)
    print(f"蝉大师iOS榜单爬虫 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    crawler = ChandashiCrawler()
    
    # 获取免费榜
    print("\n[正在爬取大陆区免费榜...]")
    free_apps = crawler.fetch_free_rankings(10)
    
    if free_apps:
        print(f"\n[大陆区免费榜 TOP{len(free_apps)}]")
        print("-" * 60)
        for app in free_apps:
            print(f"{app['rank']:2d}. {app['name']}")
            print(f"    开发商: {app['developer']} | 分类: {app['category']}")
    else:
        print("\n[WARNING] 未能从蝉大师获取数据")
        print("可能原因：")
        print("1. 网站结构已更新")
        print("2. 需要登录才能查看")
        print("3. 反爬机制拦截")
        print("\n建议：使用App Store官方RSS（台湾区/美国区）作为替代")


if __name__ == "__main__":
    main()
