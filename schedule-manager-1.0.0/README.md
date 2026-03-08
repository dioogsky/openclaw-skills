# Schedule Manager - 通用日程管理技能

一个通用的日程管理工具，支持创建、管理和提醒各类日程（健身、工作、学习等）。

## 功能特性

- 📅 创建和管理日程
- 🔄 支持重复日程（每天、每周、每月）
- ⏰ 设置提醒时间
- 📊 日程统计和追踪
- 🔗 支持飞书日历集成
- 📝 支持多种日程类型

## 安装

```bash
# 复制到OpenClaw skills目录
cp -r schedule-manager ~/.openclaw/workspace/skills/
```

## 使用方法

### 命令行使用

```bash
# 创建日程
python schedule_manager.py create --name "健身" --type "workout" --date "2026-03-10" --time "20:30-21:30" --repeat "weekly"

# 列出所有日程
python schedule_manager.py list

# 查看今日日程
python schedule_manager.py today

# 删除日程
python schedule_manager.py delete --id "event_id"

# 同步到飞书日历
python schedule_manager.py sync-feishu --token "your_token"

# 查看统计
python schedule_manager.py stats
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

## 配置文件

`config.json`:
```json
{
  "default_reminder": 30,
  "feishu_calendar_id": "",
  "categories": {
    "workout": {"color": "blue", "icon": "💪"},
    "work": {"color": "red", "icon": "💼"},
    "study": {"color": "green", "icon": "📚"},
    "meeting": {"color": "orange", "icon": "🤝"},
    "personal": {"color": "purple", "icon": "🏠"},
    "other": {"color": "gray", "icon": "📌"}
  }
}
```

## 数据存储

日程数据存储在 `data/schedule.json` 中。

## 自动化集成

### 添加到HEARTBEAT.md

```bash
# 每日日程提醒
python ~/.openclaw/workspace/skills/schedule-manager-1.0.0/schedule_manager.py check-today
```

### 飞书自动同步

设置环境变量后，日程会自动同步到飞书日历：
```bash
export FEISHU_ACCESS_TOKEN="your_token"
export FEISHU_CALENDAR_ID="your_calendar_id"
```

## 开发计划

- [ ] Web界面管理
- [ ] 语音添加日程
- [ ] AI智能建议
- [ ] 多平台同步（Google Calendar, Outlook）

## 版本历史

### v1.0.0 (2026-03-08)
- 基础功能实现
- 飞书日历集成
- 命令行工具

## 作者

OpenClaw Community

## 许可证

MIT
