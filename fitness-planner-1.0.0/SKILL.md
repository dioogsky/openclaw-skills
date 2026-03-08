---
name: fitness-planner
description: 个人健身计划制定和跟踪工具，支持训练计划生成、进度记录和提醒。
version: 1.0.0
author: 小智
---

# fitness-planner Skill v1.0

个人健身计划制定和跟踪工具

## 功能特性

- **训练计划生成**: 根据目标（减脂/增肌/塑形）生成个性化计划
- **进度跟踪**: 记录每次训练数据，可视化进度
- **定时提醒**: 支持训练提醒和休息提醒
- **多维度统计**: 体重、体脂、训练量等数据统计

## 使用方法

### 命令行方式

```bash
# 创建新计划
python fitness_planner.py create-plan --goal fat-loss --level beginner

# 记录训练
python fitness_planner.py log --date 2026-03-08 --type cardio --duration 30

# 查看今日计划
python fitness_planner.py today

# 查看进度统计
python fitness_planner.py stats

# 设置提醒
python fitness_planner.py remind --time 18:00
```

### 参数说明

| 参数 | 说明 | 可选值 |
|-----|------|--------|
| `--goal` | 健身目标 | fat-loss, muscle-gain, shape, maintain |
| `--level` | 健身水平 | beginner, intermediate, advanced |
| `--type` | 训练类型 | cardio, strength, hiit, yoga, rest |

## 计划类型

### 减脂计划 (fat-loss)
- 有氧运动为主
- 每周4-5次训练
- 配合饮食建议

### 增肌计划 (muscle-gain)
- 力量训练为主
- 每周4-6次训练
- 渐进式负荷增加

### 塑形计划 (shape)
- 综合训练
- 每周3-4次训练
- 注重线条塑造

### 维持计划 (maintain)
- 保持当前状态
- 每周3次训练
- 灵活安排

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持4种健身目标
- 支持训练记录和统计
