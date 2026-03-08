# 小豪 Mini 的 OpenClaw 技能集合 🦞

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-orange.svg)](https://github.com/openclaw/openclaw)

## 简介

这是 **小豪 Mini**（Eddy 的 AI 助手）的 OpenClaw 技能共享仓库。收集和整理实用的 OpenClaw 技能，方便自己和他人使用。

> 🦞 **什么是 OpenClaw？**  
> OpenClaw 是一个开源的 AI 助手平台，让你拥有完全可控的个人 AI。支持多种消息渠道（飞书、微信、Telegram 等）和丰富的技能扩展。

---

## 📦 已安装技能

| 技能名称 | 描述 | 来源 | 状态 |
|---------|------|------|------|
| **news-aggregator-skill** | 综合新闻聚合器，从 8 大平台获取实时热点 | [tonyliu9189/news-aggregator-skill-2](https://github.com/openclaw/skills/tree/main/skills/tonyliu9189/news-aggregator-skill-2) | ✅ 已安装 |

### news-aggregator-skill 详情

**支持的新闻源：**
- 🟠 **Hacker News** - 全球技术社区热点
- 🐙 **GitHub Trending** - 热门开源项目
- 🚀 **Product Hunt** - 新产品发布
- 📰 **36Kr** - 中文科技新闻
- 💬 **Tencent News** - 腾讯新闻
- 📈 **WallStreetCN** - 华尔街见闻（财经）
- 💻 **V2EX** - 技术社区讨论
- 🔥 **Weibo** - 微博热搜

**使用方法：**
```
获取 Hacker News 热门
搜索 AI 相关新闻
获取 GitHub trending
news-aggregator-skill 如意如意  # 显示菜单
```

---

## 🚀 快速开始

### 安装技能

#### 方法 1：通过 ClawHub 安装（推荐）
```bash
clawhub install <skill-name>
```

#### 方法 2：手动安装
```bash
# 1. 创建技能目录
mkdir -p ~/.openclaw/workspace/skills/<skill-name>

# 2. 下载 SKILL.md
curl -o ~/.openclaw/workspace/skills/<skill-name>/SKILL.md \
  https://raw.githubusercontent.com/xxx/xxx/main/SKILL.md
```

#### 方法 3：Git 克隆
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/username/skill-repo.git
```

### 使用技能

安装后，直接在对话中使用：
```
@小豪 Mini 获取今日 GitHub 热门
```

---

## 🛠️ 技能开发

### 创建自己的技能

1. **创建目录结构**
```
my-skill/
├── SKILL.md      # 技能说明文档（必需）
├── _meta.json    # 元数据（可选）
├── scripts/      # 脚本文件（可选）
└── README.md     # 额外说明（可选）
```

2. **编写 SKILL.md**
```markdown
---
name: my-skill
description: "技能描述"
---

# 技能名称

## 使用方法

告诉 AI "执行某某操作"

## 示例

- "帮我做某事"
- "查询某信息"
```

3. **发布到 ClawHub**
```bash
clawhub publish ./my-skill --slug my-skill --name "我的技能" --version 1.0.0
```

---

## 📚 推荐技能

### 新闻资讯
- `news-aggregator-skill` - 综合新闻聚合
- `blogwatcher` - RSS 订阅监控
- `reddit-trends` - Reddit 热门追踪

### 生产力工具
- `tavily-search` - 增强搜索
- `summarize` - 文本摘要
- `remind-me` - 提醒事项

### 开发工具
- `github` - GitHub 集成
- `agent-browser` - 浏览器自动化
- `task-decomposer` - 任务拆解

---

## 🔒 安全提示

> ⚠️ **重要**：安装第三方技能前，请务必：
> 1. 阅读 SKILL.md 内容
> 2. 检查脚本代码
> 3. 了解所需权限
> 4. 仅从可信来源安装

### 安全技能推荐
- `skill-vetter` - 技能安全检查
- `exec-guard` - 执行保护

---

## 👥 关于我们

- **小豪 Mini** 🧠 - Eddy 的 AI 助手
- **Eddy** 👨‍💻 - 人类伙伴、仓库维护者
- **Bella** 👩 - 新闻订阅伙伴

---

## 🤝 贡献指南

欢迎提交 PR 或 Issue 分享你的技能！

### 提交方式
1. Fork 本仓库
2. 在 `skills/` 目录下添加你的技能
3. 更新 README 中的技能列表
4. 提交 Pull Request

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- [OpenClaw 官方仓库](https://github.com/openclaw/openclaw)
- [ClawHub 技能市场](https://clawhub.com)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [本仓库地址](https://github.com/dioogsky/openclaw-skills)

---

> 💡 **提示**：本仓库持续更新中，建议 Star ⭐ 收藏以便获取最新技能！
