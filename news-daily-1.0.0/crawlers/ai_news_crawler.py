#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻爬虫
爬取机器之心、量子位、TechCrunch等AI媒体
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class AINewsCrawler:
    """AI新闻爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_jiqizhixin_news(self, count=5):
        """爬取机器之心新闻"""
        url = "https://www.jiqizhixin.com/"
        news_list = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找文章列表
            articles = soup.select('.article-item')[:count]
            
            for article in articles:
                try:
                    title_elem = article.find('h3') or article.find('a', class_='title')
                    if title_elem:
                        title = title_elem.text.strip()
                        link_elem = title_elem.find('a') if title_elem.name != 'a' else title_elem
                        link = link_elem.get('href', '') if link_elem else ''
                        if link and not link.startswith('http'):
                            link = 'https://www.jiqizhixin.com' + link
                        
                        # 获取摘要
                        desc_elem = article.find('p', class_='desc') or article.find('p')
                        summary = desc_elem.text.strip()[:120] + '...' if desc_elem else '点击查看详情'
                        
                        news_list.append({
                            'title': title,
                            'source': '机器之心',
                            'url': link,
                            'summary': summary,
                            'fetched_at': datetime.now().isoformat()
                        })
                except Exception as e:
                    continue
            
            return news_list
            
        except Exception as e:
            print(f"Error fetching 机器之心: {e}")
            return []
    
    def fetch_qbitai_news(self, count=5):
        """爬取量子位新闻"""
        url = "https://www.qbitai.com/"
        news_list = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找文章列表
            articles = soup.select('article')[:count]
            
            for article in articles:
                try:
                    title_elem = article.find('h2') or article.find('h3')
                    if title_elem:
                        title = title_elem.text.strip()
                        link_elem = title_elem.find('a')
                        link = link_elem.get('href', '') if link_elem else ''
                        
                        # 获取摘要
                        desc_elem = article.find('div', class_='entry-summary') or article.find('p')
                        summary = desc_elem.text.strip()[:120] + '...' if desc_elem else '点击查看详情'
                        
                        news_list.append({
                            'title': title,
                            'source': '量子位',
                            'url': link,
                            'summary': summary,
                            'fetched_at': datetime.now().isoformat()
                        })
                except Exception as e:
                    continue
            
            return news_list
            
        except Exception as e:
            print(f"Error fetching 量子位: {e}")
            return []
    
    def fetch_techcrunch_ai_news(self, count=5):
        """爬取TechCrunch AI新闻"""
        url = "https://techcrunch.com/category/artificial-intelligence/"
        news_list = []
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找文章列表
            articles = soup.select('article')[:count]
            
            for article in articles:
                try:
                    title_elem = article.find('h2') or article.find('h3')
                    if title_elem:
                        title = title_elem.text.strip()
                        link_elem = title_elem.find('a')
                        link = link_elem.get('href', '') if link_elem else ''
                        
                        # 获取摘要
                        desc_elem = article.find('p')
                        summary = desc_elem.text.strip()[:150] + '...' if desc_elem else 'Click for details'
                        
                        news_list.append({
                            'title': title,
                            'source': 'TechCrunch',
                            'url': link,
                            'summary': summary,
                            'fetched_at': datetime.now().isoformat()
                        })
                except Exception as e:
                    continue
            
            return news_list
            
        except Exception as e:
            print(f"Error fetching TechCrunch: {e}")
            return []
    
    def fetch_zhihu_ai_hot(self, count=5):
        """爬取知乎AI相关热榜"""
        url = "https://www.zhihu.com/hot"
        news_list = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找热榜列表
            hot_items = soup.select('.HotList-item')[:count]
            
            for item in hot_items:
                try:
                    title_elem = item.find('h2') or item.find('.HotList-title')
                    if title_elem:
                        title = title_elem.text.strip()
                        link_elem = item.find('a', href=True)
                        link = link_elem.get('href', '') if link_elem else ''
                        if link and not link.startswith('http'):
                            link = 'https://www.zhihu.com' + link
                        
                        # 过滤AI相关内容
                        ai_keywords = ['AI', '人工智能', 'ChatGPT', '大模型', '算法', '深度学习', '机器学习']
                        if any(keyword in title for keyword in ai_keywords):
                            news_list.append({
                                'title': title,
                                'source': '知乎热榜',
                                'url': link,
                                'summary': '知乎热门话题',
                                'fetched_at': datetime.now().isoformat()
                            })
                except Exception as e:
                    continue
            
            return news_list
            
        except Exception as e:
            print(f"Error fetching 知乎: {e}")
            return []
    
    def fetch_all_ai_news(self, count_per_source=3):
        """获取所有AI新闻"""
        all_news = []
        
        # 国内AI新闻
        all_news.extend(self.fetch_jiqizhixin_news(count_per_source))
        all_news.extend(self.fetch_qbitai_news(count_per_source))
        all_news.extend(self.fetch_zhihu_ai_hot(count_per_source))
        
        # 海外AI新闻
        all_news.extend(self.fetch_techcrunch_ai_news(count_per_source))
        
        return all_news


def main():
    """测试爬虫"""
    crawler = AINewsCrawler()
    
    print("=" * 60)
    print(f"AI新闻爬虫测试 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 获取机器之心新闻
    print("\n[机器之心新闻]")
    print("-" * 60)
    jiqizhixin_news = crawler.fetch_jiqizhixin_news(3)
    for news in jiqizhixin_news:
        print(f"标题: {news['title']}")
        print(f"摘要: {news['summary']}")
        print()
    
    # 获取量子位新闻
    print("\n[量子位新闻]")
    print("-" * 60)
    qbitai_news = crawler.fetch_qbitai_news(3)
    for news in qbitai_news:
        print(f"标题: {news['title']}")
        print(f"链接: {news['url']}")
        print()


if __name__ == "__main__":
    main()
