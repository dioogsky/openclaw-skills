# Schedule Manager 通用日程管理

## 描述

通用的日程管理工具，支持创建、管理和提醒各类日程（健身、工作、学习等），并可同步到飞书日历。

## 版本

1.0.0

## 功能

- 创建和管理各类日程
- 支持重复日程（每天、每周、每月）
- 设置提醒时间
- 日程统计和追踪
- 导出飞书日历格式
- 支持多种日程类型：健身、工作、学习、会议、个人事务

## 安装

无需安装，直接复制到 skills 目录即可使用。

## 使用方法

### 命令行

```bash
# 创建日程
python schedule_manager.py create --name "健身" --type workout --date "2026-03-11" --time "20:30-21:30" --repeat weekly

# 列出所有日程
python schedule_manager.py list

# 查看今日日程
python schedule_manager.py today

# 查看统计
python schedule_manager.py stats

# 标记完成
python schedule_manager.py complete --id "xxx"

# 删除日程
python schedule_manager.py delete --id "xxx"

# 导出飞书格式
python schedule_manager.py export
```

### 支持的日程类型

- `workout` - 健身/运动
- `work` - 工作
- `study` - 学习
- `meeting` - 会议
- `personal` - 个人事务
- `other` - 其他

### 重复选项

- `none` - 不重复
- `daily` - 每天
- `weekly` - 每周
- `monthly` - 每月

## 数据存储

日程数据存储在 `data/schedule.json` 中。

## 示例

### 创建健身计划

```bash
# 周二力量训练
python schedule_manager.py create --name "力量训练" --type workout --date 2026-03-11 --time "20:30-21:30" --desc "全身力量训练" --repeat weekly

# 周三有氧训练
python schedule_manager.py create --name "有氧训练" --type workout --date 2026-03-12 --time "20:30-21:30" --desc "40分钟中等强度有氧" --repeat weekly

# 周五力量训练
python schedule_manager.py create --name "力量训练" --type workout --date 2026-03-14 --time "20:30-21:30" --desc "全身力量训练" --repeat weekly

# 周六有氧训练
python schedule_manager.py create --name "有氧训练" --type workout --date 2026-03-15 --time "16:00-18:00" --desc "周末有氧" --repeat weekly

# 周日HIIT训练
python schedule_manager.py create --name "HIIT训练" --type workout --date 2026-03-16 --time "16:00-18:00" --desc "高强度间歇训练" --repeat weekly
```

### 创建工作安排

```bash
# 每日早会
python schedule_manager.py create --name "早会" --type meeting --date 2026-03-10 --time "09:00-09:30" --repeat daily

# 周会
python schedule_manager.py create --name "周会" --type meeting --date 2026-03-14 --time "14:00-15:00" --repeat weekly
```

## 自动化集成

### 添加到 HEARTBEAT.md

```markdown
## 日程提醒检查

```bash
python C:/Users/MyPC/.openclaw/workspace/skills/schedule-manager-1.0.0/schedule_manager.py today
```
```

### 飞书日历同步

1. 导出飞书格式：`python schedule_manager.py export`
2. 使用 fitness_planner 的 calendar 功能同步到飞书

## 作者

OpenClaw Community

## 许可证

MIT
