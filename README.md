# OpenClaw Skills Collection

这是一个OpenClaw Agent Skills集合，包含多个实用的自动化工具。

## 📦 包含的技能

### 1. news-daily (每日AI新闻)
- **功能**: 自动生成每日AI新闻简报
- **特点**: 
  - 支持中国AI和美国AI分开推送
  - 定时任务（早8点、晚8点）
  - 包含游戏行业动态
- **安装**: `npx skills add [your-github]/openclaw-skills@news-daily`

### 2. travel-planner (旅行规划)
- **功能**: 年度旅行计划管理
- **特点**:
  - 预算管理（15万年度预算）
  - 低价航班监控
  - 每日/每周自动报告
- **安装**: `npx skills add [your-github]/openclaw-skills@travel-planner`

### 3. fitness-planner (健身计划)
- **功能**: 个人健身计划制定和跟踪
- **特点**:
  - 减脂/增肌/塑形/维持 四种模式
  - 训练提醒（早9点、晚8点）
  - 进度记录和统计
- **安装**: `npx skills add [your-github]/openclaw-skills@fitness-planner`

### 4. find-skills (技能搜索)
- **功能**: 搜索和安装ClawHub技能
- **特点**:
  - 关键词搜索
  - 自动安装
  - 安全风险评估
- **安装**: `npx skills add [your-github]/openclaw-skills@find-skills`

### 5. agent-browser (浏览器控制)
- **功能**: 浏览器自动化操作
- **特点**:
  - 网页浏览
  - 截图/PDF生成
  - 自动化点击、输入
- **安装**: `npx skills add [your-github]/openclaw-skills@agent-browser`

## 🚀 快速开始

### 安装所有技能
```bash
# 使用 skills CLI
npx skills add [your-github]/openclaw-skills@news-daily
npx skills add [your-github]/openclaw-skills@travel-planner
npx skills add [your-github]/openclaw-skills@fitness-planner
npx skills add [your-github]/openclaw-skills@find-skills
npx skills add [your-github]/openclaw-skills@agent-browser
```

### 手动安装
1. 克隆仓库
```bash
git clone https://github.com/[your-github]/openclaw-skills.git
```

2. 复制技能到OpenClaw目录
```bash
cp -r openclaw-skills/news-daily-1.0.0 ~/.openclaw/workspace/skills/
cp -r openclaw-skills/travel-planner-1.0.0 ~/.openclaw/workspace/skills/
# ... 其他技能
```

## 📖 使用说明

每个技能文件夹内都有详细的SKILL.md文档，包含：
- 功能说明
- 使用方法
- 配置参数
- 示例命令

## 🔧 系统要求

- OpenClaw >= 2026.3.0
- Python >= 3.10
- Windows / macOS / Linux

## 📝 配置说明

### HEARTBEAT.md 配置示例
```markdown
## 每日AI新闻推送
python C:/Users/MyPC/.openclaw/workspace/skills/news-daily-1.0.0/heartbeat_check.py

## 旅行规划监控
python C:/Users/MyPC/.openclaw/workspace/skills/travel-planner-1.0.0/heartbeat_check.py

## 健身计划提醒
python C:/Users/MyPC/.openclaw/workspace/skills/fitness-planner-1.0.0/heartbeat_check.py
```

## 🤝 贡献

欢迎提交Issue和PR！

## 📄 许可证

MIT License

## 🙏 致谢

- OpenClaw Team
- ClawHub Community
