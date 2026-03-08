---
name: jimeng-image
description: 即梦AI图片生成工具，支持 Seedream 5.0/4.0/3.0 模型，可生成高质量AI图片。
version: 1.0.0
author: 小智
---

# jimeng-image Skill v1.0

即梦AI（Dreamina）图片生成工具

## 功能特性

- **文生图**: 输入文字描述，自动生成图片
- **多模型支持**: 支持 Seedream 5.0/4.0/3.0 等模型
- **多种尺寸**: 支持 2K、3K 等分辨率
- **格式选择**: 支持 JPEG、PNG 格式（仅5.0模型）
- **水印控制**: 可选择是否添加水印

## 支持的模型

| 别名 | 模型ID | 特点 |
|-----|--------|------|
| `seedream-5.0-lite` | `doubao-seedream-5-0-lite-260128` | 轻量版，速度快 ⭐推荐 |
| `seedream-5.0` | `doubao-seedream-5-0-260128` | 标准版，质量高 |
| `seedream-4.0` | `doubao-seedream-4-0` | 4.0版本 |
| `seedream-3.0` | `doubao-seedream-3-0-t2i` | 3.0版本 |

## 使用方法

### 命令行方式

```bash
# 基本用法
python jimeng_image.py "一只可爱的猫咪" -o cat.jpg

# 指定模型和尺寸
python jimeng_image.py "夕阳下的海滩" -m seedream-5.0 -s 3K

# PNG格式，无水印
python jimeng_image.py "山水画" -f png --no-watermark

# 只获取URL，不下载
python jimeng_image.py "风景图" --no-download

# 列出支持的模型
python jimeng_image.py --list-models
```

### 参数说明

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `-o, --output` | 输出文件名 | 自动生成 |
| `-m, --model` | 模型别名或ID | seedream-5.0-lite |
| `-s, --size` | 图片尺寸 (2K, 3K) | 2K |
| `-f, --format` | 输出格式 (jpeg, png) | jpeg |
| `--no-watermark` | 不添加水印 | 添加水印 |
| `--no-download` | 只返回URL | 下载图片 |

## API 调用示例

```python
from jimeng_image import generate

# 生成图片
result = generate(
    prompt="一只可爱的猫咪，水墨画风格",
    output="cat.png",
    model="seedream-5.0-lite",
    size="2K",
    format="png",
    watermark=False
)
```

## 配置说明

### 环境变量

在 `~/.openclaw/.credentials/volcengine-dreamina.env` 中配置：

```bash
ARK_API_KEY=your-ark-api-key
```

### 获取API Key

1. 登录火山引擎 Ark 控制台：https://console.volcengine.com/ark
2. 进入「API Key 管理」
3. 创建新的 API Key

## 提示词技巧

### 有效的提示词结构

```
[主体] + [风格] + [光线] + [背景] + [质量词]
```

**示例：**
- ✅ "一只橘猫在阳光下打盹，写实风格，温暖的光线，柔和的背景，高画质"
- ✅ "山水画，水墨风格，远山近水，云雾缭绕，4K高清"
- ✅ "未来城市夜景，赛博朋克风格，霓虹灯，雨夜，电影级画质"

### 质量提升关键词

- **画质**: 4K高清、超精细、 masterpiece、best quality
- **风格**: 写实、油画、水彩、水墨、赛博朋克
- **光线**: 自然光、柔和光、逆光、电影级打光

## 注意事项

1. **图片尺寸**: 2K = 2048x2048, 3K = 3072x3072
2. **生成时间**: 通常需要 10-30 秒
3. **链接有效期**: 生成的图片URL 24小时内有效
4. **格式支持**: PNG 格式仅 Seedream 5.0 模型支持

## 故障排查

### 模型未开通

**错误：** `ModelNotOpen`
**解决：** 在 Ark 控制台开通相应的图片生成模型

### API Key 无效

**错误：** `Unauthorized`
**解决：** 检查 API Key 是否正确配置

### 尺寸不支持

**错误：** `Invalid size`
**解决：** 使用支持的尺寸 (2K, 3K)

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持 Seedream 5.0/4.0/3.0 模型
- 支持 2K/3K 尺寸
- 支持 JPEG/PNG 格式
