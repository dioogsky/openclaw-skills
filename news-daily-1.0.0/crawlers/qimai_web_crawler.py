#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七麦数据网页爬虫
通过爬取七麦数据网页获取iOS榜单
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

class QimaiWebCrawler:
    """七麦数据网页爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.qimai.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.base_url = "https://www.qimai.cn"
    
    def fetch_free_rankings(self, count=10):
        """获取免费榜"""
        url = f"{self.base_url}/rank"
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            # 从页面中提取数据
            # 七麦数据使用JavaScript渲染，我们需要从script标签中提取
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找包含榜单数据的script
            scripts = soup.find_all('script')
            rank_data = []
            
            for script in scripts:
                if script.string and 'rankList' in script.string:
                    # 提取JSON数据
                    match = re.search(r'rankList\s*:\s*(\[.*?\])', script.string, re.DOTALL)
                    if match:
                        try:
                            rank_data = json.loads(match.group(1))
                            break
                        except:
                            pass
            
            # 如果无法从script提取，尝试解析HTML
            if not rank_data:
                rank_data = self._parse_html_rankings(soup, count)
            
            return rank_data[:count]
            
        except Exception as e:
            print(f"Error fetching free rankings: {e}")
            return []
    
    def _parse_html_rankings(self, soup, count):
        """从HTML解析榜单数据"""
        apps = []
        
        # 查找榜单表格或列表
        rows = soup.select('.rank-list tr') or soup.select('.app-list .app-item')
        
        for i, row in enumerate(rows[:count], 1):
            try:
                # 提取应用名称
                name_elem = row.select_one('.app-name') or row.select_one('.name')
                name = name_elem.text.strip() if name_elem else 'Unknown'
                
                # 提取开发商
                dev_elem = row.select_one('.developer') or row.select_one('.company')
                developer = dev_elem.text.strip() if dev_elem else 'Unknown'
                
                # 提取类别
                cat_elem = row.select_one('.category') or row.select_one('.genre')
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
        
        return apps
    
    def fetch_rankings_from_api_direct(self, count=10):
        """
        直接调用七麦数据API（简化版）
        不需要复杂的加密
        """
        # 尝试使用公开的CDN数据
        url = "https://static.qimai.cn/rank/data/iphone_free_cn.json"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                apps = []
                for i, item in enumerate(data[:count], 1):
                    app = {
                        'rank': i,
                        'name': item.get('appName', 'Unknown'),
                        'developer': item.get('developer', 'Unknown'),
                        'category': item.get('genre', 'Unknown'),
                        'app_id': item.get('appId', ''),
                    }
                    apps.append(app)
                return apps
        except:
            pass
        
        return []


def main():
    """测试爬虫"""
    crawler = QimaiWebCrawler()
    
    print("=" * 60)
    print(f"七麦数据iOS榜单 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 尝试获取免费榜
    print("\n[尝试获取榜单数据...]")
    apps = crawler.fetch_free_rankings(10)
    
    if apps:
        print(f"\n[免费榜 TOP{len(apps)}]")
        print("-" * 60)
        for app in apps:
            print(f"{app['rank']:2d}. {app['name']}")
            if 'developer' in app:
                print(f"    开发商: {app['developer']}")
    else:
        print("\n[提示] 网页爬虫受限，建议使用以下替代方案：")
        print("1. 使用App Store官方RSS（香港区/美国区）")
        print("2. 申请七麦数据官方API")
        print("3. 使用其他第三方数据源")


if __name__ == "__main__":
    main()
