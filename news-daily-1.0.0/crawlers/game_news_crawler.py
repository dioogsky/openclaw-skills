#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏新闻爬虫
爬取游民星空、3DM、17173等游戏网站新闻
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

class GameNewsCrawler:
    """游戏新闻爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_ymxk_news(self, count=5):
        """爬取游民星空新闻"""
        url = "https://www.gamersky.com/news/"
        news_list = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻列表
            news_items = soup.select('.tit')[:count]
            
            for item in news_items:
                try:
                    title_elem = item.find('a')
                    if title_elem:
                        title = title_elem.get('title') or title_elem.text.strip()
                        link = title_elem.get('href', '')
                        if link and not link.startswith('http'):
                            link = 'https://www.gamersky.com' + link
                        
                        news_list.append({
                            'title': title,
                            'source': '游民星空',
                            'url': link,
                            'summary': '点击查看详情',
                            'fetched_at': datetime.now().isoformat()
                        })
                except Exception as e:
                    continue
            
            return news_list
            
        except Exception as e:
            print(f"Error fetching 游民星空: {e}")
            return []
    
    def fetch_3dm_news(self, count=5):
        """爬取3DM新闻"""
        url = "https://www.3dmgame.com/news/"
        news_list = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻列表
            news_items = soup.select('.news_list li')[:count]
            
            for item in news_items:
                try:
                    title_elem = item.find('a')
                    if title_elem:
                        title = title_elem.get('title') or title_elem.text.strip()
                        link = title_elem.get('href', '')
                        
                        # 获取摘要
                        desc_elem = item.find('p')
                        summary = desc_elem.text.strip()[:100] + '...' if desc_elem else '点击查看详情'
                        
                        news_list.append({
                            'title': title,
                            'source': '3DM',
                            'url': link,
                            'summary': summary,
                            'fetched_at': datetime.now().isoformat()
                        })
                except Exception as e:
                    continue
            
            return news_list
            
        except Exception as e:
            print(f"Error fetching 3DM: {e}")
            return []
    
    def fetch_17173_news(self, count=5):
        """爬取17173新闻"""
        url = "https://news.17173.com/"
        news_list = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻列表
            news_items = soup.select('.news-list-item')[:count]
            
            for item in news_items:
                try:
                    title_elem = item.find('a', class_='title') or item.find('a')
                    if title_elem:
                        title = title_elem.get('title') or title_elem.text.strip()
                        link = title_elem.get('href', '')
                        
                        news_list.append({
                            'title': title,
                            'source': '17173',
                            'url': link,
                            'summary': '点击查看详情',
                            'fetched_at': datetime.now().isoformat()
                        })
                except Exception as e:
                    continue
            
            return news_list
            
        except Exception as e:
            print(f"Error fetching 17173: {e}")
            return []
    
    def fetch_ign_news(self, count=5):
        """爬取IGN新闻（英文）"""
        url = "https://www.ign.com/news"
        news_list = []
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻列表
            news_items = soup.select('[data-cy="card"]')[:count]
            
            for item in news_items:
                try:
                    title_elem = item.find('h3') or item.find('a', class_='title')
                    if title_elem:
                        title = title_elem.text.strip()
                        link_elem = item.find('a', href=True)
                        link = link_elem.get('href', '') if link_elem else ''
                        if link and not link.startswith('http'):
                            link = 'https://www.ign.com' + link
                        
                        # 获取摘要
                        desc_elem = item.find('p')
                        summary = desc_elem.text.strip()[:150] + '...' if desc_elem else '点击查看详情'
                        
                        news_list.append({
                            'title': title,
                            'source': 'IGN',
                            'url': link,
                            'summary': summary,
                            'fetched_at': datetime.now().isoformat()
                        })
                except Exception as e:
                    continue
            
            return news_list
            
        except Exception as e:
            print(f"Error fetching IGN: {e}")
            return []
    
    def fetch_all_gaming_news(self, count_per_source=3):
        """获取所有游戏新闻"""
        all_news = []
        
        # 国内游戏新闻
        all_news.extend(self.fetch_ymxk_news(count_per_source))
        all_news.extend(self.fetch_3dm_news(count_per_source))
        all_news.extend(self.fetch_17173_news(count_per_source))
        
        # 海外游戏新闻
        all_news.extend(self.fetch_ign_news(count_per_source))
        
        return all_news


def main():
    """测试爬虫"""
    crawler = GameNewsCrawler()
    
    print("=" * 60)
    print(f"游戏新闻爬虫测试 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 获取游民星空新闻
    print("\n[游民星空新闻]")
    print("-" * 60)
    ymxk_news = crawler.fetch_ymxk_news(3)
    for news in ymxk_news:
        print(f"标题: {news['title']}")
        print(f"链接: {news['url']}")
        print()
    
    # 获取3DM新闻
    print("\n[3DM新闻]")
    print("-" * 60)
    dm_news = crawler.fetch_3dm_news(3)
    for news in dm_news:
        print(f"标题: {news['title']}")
        print(f"摘要: {news['summary']}")
        print()
    
    # 获取17173新闻
    print("\n[17173新闻]")
    print("-" * 60)
    news_17173 = crawler.fetch_17173_news(3)
    for news in news_17173:
        print(f"标题: {news['title']}")
        print(f"链接: {news['url']}")
        print()


if __name__ == "__main__":
    main()
