# 飞书日历自动化配置指南

## 步骤1：创建飞书应用

1. 访问 https://open.feishu.cn/app
2. 点击"创建企业自建应用"
3. 填写应用名称：健身计划助手
4. 选择应用类型：企业自建应用

## 步骤2：配置权限

在应用管理后台，进入"权限管理"，添加以下权限：

- `calendar:calendar:read` - 读取日历
- `calendar:calendar.event:create` - 创建日历事件
- `calendar:calendar.event:read` - 读取日历事件
- `calendar:calendar.event:update` - 更新日历事件

## 步骤3：获取应用凭证

在"凭证与基础信息"页面，获取：
- App ID
- App Secret

## 步骤4：发布应用

1. 进入"版本管理与发布"
2. 点击"创建版本"
3. 填写版本信息
4. 点击"申请发布"
5. 让管理员审核通过

## 步骤5：获取用户授权

访问以下URL进行授权（将{APP_ID}替换为你的App ID）：

```
https://open.feishu.cn/open-apis/authen/v1/index?app_id={APP_ID}&redirect_uri=https://www.example.com/callback
```

授权后，你会获得一个`code`，用于换取`access_token`。

## 步骤6：使用API创建日历事件

使用获取到的`access_token`，调用以下API创建事件：

```bash
curl -X POST \
  https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events \
  -H 'Authorization: Bearer {access_token}' \
  -H 'Content-Type: application/json' \
  -d '{
    "summary": "健身 - 有氧",
    "description": "有氧训练\\n时长：40分钟\\n强度：中",
    "start": {
      "date_time": "2026-03-09T20:30:00+08:00",
      "time_zone": "Asia/Shanghai"
    },
    "end": {
      "date_time": "2026-03-09T21:30:00+08:00",
      "time_zone": "Asia/Shanghai"
    },
    "reminders": [
      {"minutes": 30}
    ]
  }'
```

## 简化方案

如果你希望我来帮你完成配置，请提供：
1. 你的飞书邮箱/手机号
2. 我可以通过飞书机器人直接给你发送配置好的链接

或者，你可以：
1. 直接在飞书日历中搜索"健身计划"
2. 订阅公开的健身日历模板
