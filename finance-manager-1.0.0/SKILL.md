# Finance Manager - 理财助手

## 描述

个人理财管理工具，支持记账、预算管理、投资追踪和财务分析。

## 版本

1.0.0

## 功能

- 💰 快速记账（语音/文字）
- 📊 收支统计与分析
- 🎯 预算设置与提醒
- 📈 投资收益追踪
- 💹 资产分布可视化
- 📱 飞书报表推送

## 使用方法

### 命令行

```bash
# 快速记账
python finance_manager.py add --amount 100 --category food --note "午餐"

# 语音记账
python finance_manager.py voice "今天花了50块买咖啡"

# 查看今日收支
python finance_manager.py today

# 查看月度报表
python finance_manager.py report --month 2026-03

# 设置预算
python finance_manager.py budget --category food --amount 3000

# 查看预算执行情况
python finance_manager.py budget-status

# 添加投资记录
python finance_manager.py invest --name "股票A" --amount 10000 --type stock

# 查看投资收益
python finance_manager.py invest-status
```

### 支持的支出分类

- `food` - 餐饮
- `transport` - 交通
- `shopping` - 购物
- `entertainment` - 娱乐
- `housing` - 居住
- `medical` - 医疗
- `education` - 教育
- `investment` - 投资
- `other` - 其他

### 支持的预算周期

- `daily` - 每日
- `weekly` - 每周
- `monthly` - 每月（默认）
- `yearly` - 每年

## 数据存储

财务数据存储在 `data/finance.json` 中，本地安全保存。

## 自动化集成

### 添加到 HEARTBEAT.md

```bash
# 每日财务提醒
python ~/.openclaw/workspace/skills/finance-manager-1.0.0/finance_manager.py daily-check
```

### 飞书推送

设置环境变量后，每日/每周自动推送财务报告：
```bash
export FEISHU_WEBHOOK="your_webhook_url"
```

## 示例

### 日常记账

```bash
# 早餐
python finance_manager.py add -a 15 -c food -n "早餐"

# 地铁
python finance_manager.py add -a 5 -c transport -n "地铁"

# 超市购物
python finance_manager.py add -a 200 -c shopping -n "超市采购"
```

### 月度预算设置

```bash
# 餐饮预算 3000/月
python finance_manager.py budget -c food -a 3000 -p monthly

# 交通预算 500/月
python finance_manager.py budget -c transport -a 500

# 娱乐预算 1000/月
python finance_manager.py budget -c entertainment -a 1000
```

### 投资追踪

```bash
# 买入股票
python finance_manager.py invest -n "腾讯控股" -a 50000 -t stock -p 400

# 买入基金
python finance_manager.py invest -n "沪深300ETF" -a 10000 -t fund

# 查看投资收益
python finance_manager.py invest-status
```

## 作者

OpenClaw Community

## 许可证

MIT
