# news-daily

每日AI新闻自动收集和推送工具

## 功能

- 📰 自动收集最新AI动态
- 🇨🇳 中国AI板块 - 百度、阿里、字节、智谱、华为等
- 🇺🇸 美国AI板块 - OpenAI、Google、Anthropic、Meta等
- ⏰ 定时推送 - 支持自定义推送时间
- 📱 多平台支持 - 飞书、微信等

## 安装

```bash
# 克隆到 skills 目录
cd ~/.openclaw/workspace/skills
git clone <repo-url> news-daily-1.0.0
```

## 使用方法

### 立即推送

```bash
python news_daily.py push
```

### 设置定时任务

```bash
# 默认时间（早9:30，晚20:00）
python news_daily.py schedule

# 自定义时间
python news_daily.py schedule --morning 08:00 --evening 21:00
```

### 查看状态

```bash
python news_daily.py status
```

### 移除定时任务

```bash
python news_daily.py unschedule
```

## 配置

编辑 `news_daily.py` 中的新闻源，添加或修改新闻条目。

## 定时任务说明

定时任务使用 Windows 任务计划程序（Windows）或 cron（Linux/macOS）。

### Windows

以管理员身份运行 PowerShell：

```powershell
python news_daily.py schedule
# 然后运行生成的脚本
.\schedule_tasks.ps1
```

### Linux/macOS

```bash
# 添加到 crontab
crontab -e

# 添加以下行（早上9:30）
30 9 * * * /usr/bin/python3 /path/to/news_daily.py push

# 添加以下行（晚上20:00）
0 20 * * * /usr/bin/python3 /path/to/news_daily.py push
```

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持中国/美国分板块推送
- 支持定时任务设置

## 作者

小智
