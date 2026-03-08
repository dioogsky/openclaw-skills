#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即梦AI图片生成工具
"""

import os
import sys
import json
import time
import base64
from datetime import datetime
import requests

# 设置UTF-8编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# API配置
ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

# 默认模型
DEFAULT_MODEL = "doubao-vision-image-1.0-pro"


def load_credentials():
    """加载API凭证"""
    env_file = os.path.expanduser("~/.openclaw/.credentials/volcengine-dreamina.env")
    
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    return os.environ.get('ARK_API_KEY')


def generate_image(api_key, prompt, model=None, size="1024x1024"):
    """生成图片"""
    if model is None:
        model = DEFAULT_MODEL
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size
    }
    
    print(f"正在生成图片...")
    print(f"   模型: {model}")
    print(f"   提示词: {prompt}")
    print(f"   尺寸: {size}")
    
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=60)
        
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


def save_image(image_data, output_path):
    """保存图片"""
    try:
        # 解码base64图片数据
        image_bytes = base64.b64decode(image_data)
        
        with open(output_path, 'wb') as f:
            f.write(image_bytes)
        
        file_size = os.path.getsize(output_path)
        print(f"✅ 图片已保存: {output_path}")
        print(f"   文件大小: {file_size / 1024:.2f} KB")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False


def generate(prompt, output=None, model=None, size="1024x1024"):
    """生成图片的主函数"""
    api_key = load_credentials()
    
    if not api_key:
        print("❌ 未找到 ARK_API_KEY")
        sys.exit(1)
    
    # 生成图片
    result = generate_image(api_key, prompt, model, size)
    
    if not result:
        sys.exit(1)
    
    # 获取图片数据
    image_data = result.get('data', [{}])[0].get('b64_json')
    
    if not image_data:
        print("❌ 未找到图片数据")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    # 保存图片
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"jimeng_image_{timestamp}.png"
    
    save_image(image_data, output)
    
    # 显示结果信息
    print(f"\n📊 生成结果:")
    print(f"   尺寸: {size}")
    print(f"   模型: {model or DEFAULT_MODEL}")
    
    return result


def main():
    if len(sys.argv) < 2:
        print("即梦AI图片生成工具")
        print()
        print("用法:")
        print(f"  {sys.argv[0]} <提示词> [选项]")
        print()
        print("选项:")
        print("  -o, --output <文件名>  输出文件名")
        print("  -m, --model <模型ID>   指定模型")
        print("  -s, --size <尺寸>      图片尺寸 (1024x1024, 1024x1536, 1536x1024)")
        print()
        print("示例:")
        print(f'  {sys.argv[0]} "一只可爱的猫咪" -o cat.png')
        print(f'  {sys.argv[0]} "夕阳下的海滩" -s 1024x1536')
        print()
        sys.exit(1)
    
    prompt = sys.argv[1]
    output = None
    model = None
    size = "1024x1024"
    
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
        else:
            i += 1
    
    generate(prompt, output, model, size)


if __name__ == "__main__":
    main()
