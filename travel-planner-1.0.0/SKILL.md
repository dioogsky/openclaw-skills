---
name: travel-planner
description: 年度旅行规划工具，支持预算管理、低价航班/酒店监控、每日更新和每周报告。
version: 1.0.0
author: 小智
---

# Travel Planner Skill v1.0

年度旅行规划与价格监控工具

## 功能特性

- **预算管理**: 年度预算跟踪，支持多行程分配
- **价格监控**: 自动扫描低价航班和酒店
- **每日更新**: 价格变动、预算状态日报
- **每周报告**: 行程规划、价格趋势、建议汇总
- **多目的地**: 支持国内外热门目的地

## 使用方法

### 命令行

```bash
# 生成每日更新
python travel_planner.py daily

# 生成每周报告
python travel_planner.py weekly

# 添加追踪路线
python travel_planner.py add-route 上海 曼谷 2026-05-01

# 添加旅行计划
python travel_planner.py add-trip 东京 2026-04-01 2026-04-07 25000

# 查看状态
python travel_planner.py status
```

### Heartbeat 自动运行

已配置自动定时任务：
- **每日更新**: 每天自动扫描价格并推送
- **每周报告**: 每周一早上推送周报

## 预算设置

默认年度预算: **15万 CNY**

可在 `memory/travel-planner-state.json` 中修改

## 数据文件

- 状态文件: `memory/travel-planner-state.json`
- 日报目录: `memory/travel-reports/daily_*.txt`
- 周报目录: `memory/travel-reports/weekly_*.txt`

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持预算管理
- 支持价格监控
- 支持定时报告
