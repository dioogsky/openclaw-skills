#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七麦数据网页爬虫（使用Playwright）
爬取七麦数据的iOS榜单
"""

import json
import asyncio
from datetime import datetime

class QimaiPlaywrightCrawler:
    """使用Playwright爬取七麦数据"""
    
    def __init__(self):
        self.base_url = "https://www.qimai.cn/rank"
    
    async def fetch_rankings(self, rank_type='free', count=10):
        """
        获取iOS榜单
        
        rank_type: free(免费榜), paid(付费榜), grossing(畅销榜)
        """
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()
                
                # 访问页面
                await page.goto(self.base_url, wait_until='networkidle')
                await asyncio.sleep(2)  # 等待页面加载
                
                # 根据榜单类型点击对应标签
                if rank_type == 'paid':
                    await page.click('text=付费榜')
                elif rank_type == 'grossing':
                    await page.click('text=畅销榜')
                
                await asyncio.sleep(1)  # 等待数据加载
                
                # 提取榜单数据
                apps = await page.evaluate('''(count) => {
                    const rows = document.querySelectorAll('.rank-list tr, .app-list .app-item, [class*="rank"] tr');
                    const data = [];
                    
                    rows.forEach((row, index) => {
                        if (index >= count) return;
                        
                        // 尝试多种选择器
                        const nameElem = row.querySelector('.app-name, .name, [class*="name"], h3, h4');
                        const devElem = row.querySelector('.developer, .company, [class*="developer"]');
                        const catElem = row.querySelector('.category, .genre, [class*="category"]');
                        const rankElem = row.querySelector('.rank, .rank-num, [class*="rank"]');
                        
                        if (nameElem) {
                            data.push({
                                rank: rankElem ? rankElem.innerText.trim() : (index + 1),
                                name: nameElem.innerText.trim(),
                                developer: devElem ? devElem.innerText.trim() : '',
                                category: catElem ? catElem.innerText.trim() : ''
                            });
                        }
                    });
                    
                    return data;
                }''', count)
                
                await browser.close()
                
                # 格式化数据
                formatted_apps = []
                for i, app in enumerate(apps[:count], 1):
                    formatted_apps.append({
                        'rank': i,
                        'name': app.get('name', 'Unknown'),
                        'developer': app.get('developer', 'Unknown'),
                        'category': app.get('category', 'Unknown'),
                    })
                
                return formatted_apps
                
        except ImportError:
            print("[ERROR] 请先安装Playwright: pip install playwright")
            print("[ERROR] 然后运行: playwright install chromium")
            return []
        except Exception as e:
            print(f"[ERROR] 爬取失败: {e}")
            return []
    
    async def fetch_free_rankings(self, count=10):
        """获取免费榜"""
        return await self.fetch_rankings('free', count)
    
    async def fetch_paid_rankings(self, count=10):
        """获取付费榜"""
        return await self.fetch_rankings('paid', count)
    
    async def fetch_grossing_rankings(self, count=10):
        """获取畅销榜"""
        return await self.fetch_rankings('grossing', count)


class QimaiAPIAlternative:
    """
    使用替代API获取七麦数据
    通过分析网页请求找到的数据接口
    """
    
    def __init__(self):
        import requests
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://www.qimai.cn',
            'Referer': 'https://www.qimai.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_rankings_simple(self, count=10):
        """
        尝试使用简化的方式获取数据
        有些网站会提供未加密的CDN数据
        """
        import requests
        
        # 尝试多个可能的API端点
        endpoints = [
            "https://api.qimai.cn/rank/index",
            "https://www.qimai.cn/api/rank/list",
        ]
        
        for url in endpoints:
            try:
                params = {
                    'brand': 'all',
                    'country': 'cn',
                    'device': 'iphone',
                    'genre': '36',
                    'page': 1,
                    'date': datetime.now().strftime('%Y-%m-%d')
                }
                
                response = self.session.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == 200 or data.get('status') == 0:
                        # 解析数据
                        apps = []
                        rank_list = data.get('data', {}).get('list', [])[:count]
                        
                        for i, item in enumerate(rank_list, 1):
                            app = {
                                'rank': i,
                                'name': item.get('appName') or item.get('appInfo', {}).get('appName', 'Unknown'),
                                'developer': item.get('developer') or item.get('appInfo', {}).get('developerName', 'Unknown'),
                                'category': item.get('genre') or item.get('appInfo', {}).get('genre', 'Unknown'),
                            }
                            apps.append(app)
                        
                        if apps:
                            return apps
                            
            except Exception as e:
                continue
        
        return []


async def main():
    """测试爬虫"""
    print("=" * 60)
    print(f"七麦数据iOS榜单爬虫 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 首先尝试API方式
    print("\n[方法1] 尝试直接API获取...")
    api_crawler = QimaiAPIAlternative()
    apps = api_crawler.fetch_rankings_simple(10)
    
    if apps:
        print(f"✅ API方式成功！获取到{len(apps)}条数据\n")
        for app in apps:
            print(f"{app['rank']:2d}. {app['name']}")
            print(f"    开发商: {app['developer']}")
    else:
        print("❌ API方式失败，尝试Playwright...")
        
        # 使用Playwright
        crawler = QimaiPlaywrightCrawler()
        apps = await crawler.fetch_free_rankings(10)
        
        if apps:
            print(f"✅ Playwright方式成功！获取到{len(apps)}条数据\n")
            for app in apps:
                print(f"{app['rank']:2d}. {app['name']}")
                print(f"    开发商: {app['developer']}")
        else:
            print("❌ 所有方式都失败")
            print("\n建议：")
            print("1. 安装Playwright: pip install playwright")
            print("2. 运行: playwright install chromium")
            print("3. 或者使用App Store官方RSS（香港区）")


if __name__ == "__main__":
    asyncio.run(main())
