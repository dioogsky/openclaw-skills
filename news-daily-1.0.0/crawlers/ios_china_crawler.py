#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS大陆区榜单爬虫 - 使用Playwright
爬取七麦数据或蝉大师的大陆区iOS榜单
"""

import asyncio
import json
from datetime import datetime

class IOSChinaRankCrawler:
    """iOS大陆区榜单爬虫"""
    
    def __init__(self):
        self.data = []
    
    async def fetch_from_qimai(self, count=10):
        """从七麦数据获取"""
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                # 访问七麦数据榜单页
                await page.goto('https://www.qimai.cn/rank', wait_until='networkidle')
                await asyncio.sleep(3)
                
                # 等待榜单数据加载
                await page.wait_for_selector('.rank-list, .app-list, [class*="rank"]', timeout=10000)
                
                # 提取数据
                apps = await page.evaluate('''(count) => {
                    const results = [];
                    const rows = document.querySelectorAll('.rank-list tr, .app-item, [class*="rank-item"]');
                    
                    rows.forEach((row, index) => {
                        if (index >= count) return;
                        
                        const nameElem = row.querySelector('.app-name, .name, h3, h4, [class*="name"]');
                        const devElem = row.querySelector('.developer, .company, [class*="developer"]');
                        const catElem = row.querySelector('.category, .genre, [class*="category"]');
                        const rankElem = row.querySelector('.rank-num, .rank, [class*="rank"]');
                        
                        if (nameElem) {
                            results.push({
                                rank: rankElem ? parseInt(rankElem.innerText) || (index + 1) : (index + 1),
                                name: nameElem.innerText.trim(),
                                developer: devElem ? devElem.innerText.trim() : '',
                                category: catElem ? catElem.innerText.trim() : ''
                            });
                        }
                    });
                    
                    return results;
                }''', count)
                
                await browser.close()
                return apps
                
        except Exception as e:
            print(f"七麦数据爬取失败: {e}")
            return []
    
    async def fetch_from_chandashi(self, count=10):
        """从蝉大师获取"""
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                # 访问蝉大师榜单页
                await page.goto('https://www.chandashi.com/ranking/index.html', wait_until='networkidle')
                await asyncio.sleep(3)
                
                # 尝试提取数据
                apps = await page.evaluate('''(count) => {
                    const results = [];
                    
                    // 尝试多种选择器
                    const selectors = [
                        '.rank-list tr',
                        '.app-rank-item',
                        '.ranking-item',
                        '[data-rank]',
                        '.app-item',
                        'table tr'
                    ];
                    
                    let rows = [];
                    for (const selector of selectors) {
                        rows = document.querySelectorAll(selector);
                        if (rows.length > 0) break;
                    }
                    
                    rows.forEach((row, index) => {
                        if (index >= count) return;
                        
                        const nameElem = row.querySelector('.app-name, .name, h3, h4, .title, td:nth-child(2)');
                        const devElem = row.querySelector('.developer, .publisher, .company');
                        const catElem = row.querySelector('.category, .genre');
                        
                        if (nameElem) {
                            results.push({
                                rank: index + 1,
                                name: nameElem.innerText.trim(),
                                developer: devElem ? devElem.innerText.trim() : '',
                                category: catElem ? catElem.innerText.trim() : ''
                            });
                        }
                    });
                    
                    return results;
                }''', count)
                
                await browser.close()
                return apps
                
        except Exception as e:
            print(f"蝉大师爬取失败: {e}")
            return []
    
    async def fetch_all(self, count=10):
        """尝试从多个源获取数据"""
        print("[INFO] 正在尝试从七麦数据获取大陆区iOS榜单...")
        apps = await self.fetch_from_qimai(count)
        
        if not apps:
            print("[INFO] 七麦数据失败，尝试蝉大师...")
            apps = await self.fetch_from_chandashi(count)
        
        return apps


async def main():
    """主函数"""
    print("=" * 60)
    print(f"iOS大陆区榜单爬虫 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    crawler = IOSChinaRankCrawler()
    apps = await crawler.fetch_all(10)
    
    if apps:
        print(f"\n[大陆区iOS免费榜 TOP{len(apps)}]")
        print("-" * 60)
        for app in apps:
            print(f"{app['rank']:2d}. {app['name']}")
            if app.get('developer'):
                print(f"    开发商: {app['developer']}")
            if app.get('category'):
                print(f"    分类: {app['category']}")
    else:
        print("\n[ERROR] 无法获取大陆区iOS榜单数据")
        print("\n可能原因：")
        print("1. 七麦数据和蝉大师都需要登录")
        print("2. 反爬机制升级")
        print("3. 网站结构变更")
        print("\n建议：")
        print("- 购买官方API服务")
        print("- 使用App Store其他区域数据作为参考")


if __name__ == "__main__":
    asyncio.run(main())
