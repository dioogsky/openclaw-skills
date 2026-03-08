---
name: news-daily
description: 每日AI新闻自动收集和推送工具，支持分板块（中国/美国）推送，可定时执行。
version: 1.0.0
author: 小智
---

# news-daily Skill v1.0

每日AI新闻自动收集和推送工具

## 功能特性

- **分板块推送**: 中国AI、美国AI两大板块
- **定时推送**: 支持自定义推送时间（默认早9:30、晚20:00）
- **多平台**: 支持飞书、微信等消息平台
- **自动收集**: 自动整理最新AI动态

## 使用方法

### 命令行方式

```bash
# 立即推送一次
python news_daily.py push

# 设置定时任务（需要管理员权限）
python news_daily.py schedule --morning 09:30 --evening 20:00

# 查看定时任务状态
python news_daily.py status

# 移除定时任务
python news_daily.py unschedule
```

### 参数说明

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `--morning` | 早上推送时间 | 09:30 |
| `--evening` | 晚上推送时间 | 20:00 |
| `--china-count` | 中国AI新闻条数 | 5 |
| `--usa-count` | 美国AI新闻条数 | 5 |

## 配置说明

### 环境变量

在 `~/.openclaw/.credentials/news-daily.env` 中配置：

```bash
# 推送目标（可选）
FEISHU_CHAT_ID=your_chat_id
```

## 新闻来源

### 中国AI
- 百度AI
- 阿里云
- 字节跳动/火山引擎
- 智谱AI
- 华为云
- 腾讯AI
- 商汤科技

### 美国AI
- OpenAI
- Google DeepMind
- Anthropic
- Meta AI
- Midjourney
- Stability AI
- Microsoft AI

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持中国/美国分板块推送
- 支持定时任务设置
- 支持飞书消息推送
