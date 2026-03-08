#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即梦AI图片生成工具
支持 Seedream 5.0/4.0/3.0 模型
"""

import os
import sys
import json
import base64
from datetime import datetime
import requests

# 设置UTF-8编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# API配置
ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
ENDPOINT_CONTENT = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"

# 默认模型
DEFAULT_MODEL = "doubao-seedream-5-0-lite-260128"

# 支持的模型列表
SUPPORTED_MODELS = {
    "seedream-5.0-lite": "doubao-seedream-5-0-lite-260128",
    "seedream-5.0": "doubao-seedream-5-0-260128",
    "seedream-4.0": "doubao-seedream-4-0",
    "seedream-3.0": "doubao-seedream-3-0-t2i",
}


def load_credentials():
    """加载API凭证"""
    # 尝试多个可能的路径
    possible_paths = [
        os.path.expanduser("~/.openclaw/.credentials/volcengine-dreamina.env"),
        os.path.expanduser("~/.openclaw/.credentials/ark-api-key.env"),
        os.path.join(os.path.dirname(__file__), ".credentials.env"),
    ]
    
    for env_file in possible_paths:
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
    
    # 优先使用 ARK_API_KEY，如果没有则尝试 VOLCENGINE_ACCESS_KEY_ID
    api_key = os.environ.get('ARK_API_KEY') or os.environ.get('VOLCENGINE_ACCESS_KEY_ID')
    
    if not api_key:
        print("❌ 错误：未找到 API Key")
        print("请确保以下文件之一存在并包含 ARK_API_KEY:")
        for path in possible_paths:
            print(f"  - {path}")
        sys.exit(1)
    
    return api_key


def resolve_model(model_alias):
    """解析模型别名"""
    if not model_alias:
        return DEFAULT_MODEL
    
    # 如果是完整模型ID，直接使用
    if model_alias.startswith("doubao-seedream"):
        return model_alias
    
    # 如果是别名，查找对应模型
    if model_alias in SUPPORTED_MODELS:
        return SUPPORTED_MODELS[model_alias]
    
    return DEFAULT_MODEL


def generate_image(api_key, prompt, model=None, size="2K", output_format="jpeg", watermark=True, reference_image=None):
    """生成图片"""
    model_id = resolve_model(model)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 如果有参考图，使用 content API
    use_content_api = reference_image and os.path.exists(reference_image)
    
    if use_content_api:
        print(f"📎 使用参考图: {reference_image}")
        
        # 读取参考图并转为 base64
        with open(reference_image, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # 使用 content 数组格式
        payload = {
            "model": model_id,
            "content": [
                {
                    "type": "image",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_data}"
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ],
        }
        endpoint = ENDPOINT_CONTENT
    else:
        # 纯文本生成
        payload = {
            "model": model_id,
            "prompt": prompt,
            "size": size,
            "response_format": "url",
            "watermark": watermark,
        }
        # 只有 5.0 模型支持 output_format
        if "5-0" in model_id:
            payload["output_format"] = output_format
        endpoint = ENDPOINT
    
    # 只有 5.0 模型支持 output_format
    if "5-0" in model_id:
        payload["output_format"] = output_format
    
    print(f"🎨 正在生成图片...")
    print(f"   模型: {model_id}")
    print(f"   提示词: {prompt}")
    print(f"   尺寸: {size}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', '未知错误')
            print(f"❌ 生成失败: {error_msg}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return None


def download_image(url, output_path):
    """下载图片"""
    print(f"📥 正在下载图片...")
    
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(output_path)
        print(f"✅ 图片已保存: {output_path}")
        print(f"   文件大小: {file_size / 1024:.2f} KB")
        return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False


def generate(prompt, output=None, model=None, size="2K", format="jpeg", watermark=True, no_download=False, reference_image=None):
    """生成图片的主函数"""
    api_key = load_credentials()
    
    # 生成图片
    result = generate_image(api_key, prompt, model, size, format, watermark, reference_image)
    
    if not result:
        sys.exit(1)
    
    # 获取图片信息
    image_data = result.get('data', [{}])[0]
    
    if 'error' in image_data:
        print(f"❌ 图片生成错误: {image_data['error']}")
        sys.exit(1)
    
    image_url = image_data.get('url')
    image_size = image_data.get('size', 'unknown')
    
    if not image_url:
        print("❌ 未找到图片URL")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    print(f"✅ 图片生成成功!")
    print(f"   尺寸: {image_size}")
    
    if no_download:
        print(f"\n📎 图片URL: {image_url}")
        return result
    
    # 保存图片
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = "png" if format == "png" else "jpg"
        output = f"jimeng_image_{timestamp}.{ext}"
    
    download_image(image_url, output)
    
    # 显示用量信息
    usage = result.get('usage', {})
    print(f"\n📊 用量信息:")
    print(f"   生成图片数: {usage.get('generated_images', 0)}")
    print(f"   输出tokens: {usage.get('output_tokens', 0)}")
    
    return result


def list_models():
    """列出支持的模型"""
    print("支持的图片生成模型:")
    print()
    print("🌟 推荐模型:")
    print(f"  seedream-5.0-lite  ->  {SUPPORTED_MODELS['seedream-5.0-lite']}")
    print(f"  seedream-5.0       ->  {SUPPORTED_MODELS['seedream-5.0']}")
    print()
    print("其他模型:")
    for alias, model_id in SUPPORTED_MODELS.items():
        if alias not in ['seedream-5.0-lite', 'seedream-5.0']:
            print(f"  {alias}  ->  {model_id}")
    print()
    print("支持的尺寸:")
    print("  2K  - 2048x2048 (默认)")
    print("  3K  - 3072x3072")
    print()
    print("支持的格式 (仅5.0模型):")
    print("  jpeg  (默认)")
    print("  png")


def main():
    if len(sys.argv) < 2:
        print("即梦AI图片生成工具 v1.0")
        print()
        print("用法:")
        print(f"  {sys.argv[0]} <提示词> [选项]")
        print()
        print("选项:")
        print("  -o, --output <文件名>    输出文件名")
        print("  -m, --model <模型>       模型别名或ID")
        print("  -s, --size <尺寸>        图片尺寸 (2K, 3K)")
        print("  -f, --format <格式>      输出格式 (jpeg, png)")
        print("  -r, --reference <图片>   参考图片路径")
        print("  --no-watermark           不添加水印")
        print("  --no-download            只返回URL，不下载")
        print("  --list-models            列出支持的模型")
        print()
        print("示例:")
        print(f'  {sys.argv[0]} "一只可爱的猫咪" -o cat.jpg')
        print(f'  {sys.argv[0]} "夕阳下的海滩" -m seedream-5.0 -s 3K')
        print(f'  {sys.argv[0]} "参考图风格" -r reference.png -o output.jpg')
        print()
        sys.exit(1)
    
    # 检查是否是列出模型命令
    if sys.argv[1] == "--list-models":
        list_models()
        sys.exit(0)
    
    prompt = sys.argv[1]
    output = None
    model = None
    size = "2K"
    format_type = "jpeg"
    watermark = True
    no_download = False
    reference_image = None
    
    # 解析参数
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "-o" or sys.argv[i] == "--output":
            output = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "-m" or sys.argv[i] == "--model":
            model = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "-s" or sys.argv[i] == "--size":
            size = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "-f" or sys.argv[i] == "--format":
            format_type = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "-r" or sys.argv[i] == "--reference":
            reference_image = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--no-watermark":
            watermark = False
            i += 1
        elif sys.argv[i] == "--no-download":
            no_download = True
            i += 1
        else:
            i += 1
    
    generate(prompt, output, model, size, format_type, watermark, no_download, reference_image)


if __name__ == "__main__":
    main()
