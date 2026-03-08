#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试iOS大陆区榜单
"""

from ios_rank_crawler import IOSRankCrawler
from datetime import datetime

crawler = IOSRankCrawler()

print("=" * 60)
print(f"iOS App Store 大陆区榜单 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
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
    print(f"    分类: {app['category']} | 价格: {app['price']}")

# 畅销榜
print("\n[畅销榜 TOP10]")
print("-" * 60)
apps = crawler.fetch_grossing_rankings(10)
for app in apps:
    print(f"{app['rank']:2d}. {app['name']}")
    print(f"    分类: {app['category']} | 开发商: {app['developer']}")
