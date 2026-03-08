#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尝试不同的图片生成模型ID
"""

import os
import sys
import requests

# 设置UTF-8编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def load_credentials():
    env_file = os.path.expanduser("~/.openclaw/.credentials/volcengine-dreamina.env")
    
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    return os.environ.get('ARK_API_KEY')


def try_model(api_key, model_id):
    """尝试使用指定模型生成图片"""
    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model_id,
        "prompt": "a cat"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            return True, "✅ 可用"
        elif "does not exist" in str(data) or "not have access" in str(data):
            return False, "❌ 不存在或无权限"
        elif "ModelNotOpen" in str(data):
            return False, "❌ 未开通"
        else:
            error_msg = data.get('error', {}).get('message', '未知错误')
            return False, f"❌ {error_msg[:50]}"
    except Exception as e:
        return False, f"❌ 请求失败: {e}"


def main():
    api_key = load_credentials()
    
    if not api_key:
        print("❌ 未找到 ARK_API_KEY")
        sys.exit(1)
    
    print("🔍 尝试不同的 Doubao-Seedream 模型ID...\n")
    
    # 尝试不同的模型ID格式
    models = [
        "Doubao-Seedream-4.0",
        "doubao-seedream-4.0",
        "doubao-seedream-4-0",
        "seedream-4.0",
        "seedream-4-0",
        "Doubao-Seedream-4-0",
        "doubao-seedream-4.0-pro",
        "doubao-seedream-4-0-pro",
    ]
    
    for model_id in models:
        print(f"尝试 {model_id}...", end=" ")
        is_available, status = try_model(api_key, model_id)
        print(status)
        
        if is_available:
            print(f"\n✅ 找到可用模型: {model_id}")
            break
    
    print("\n" + "="*60)
    print("\n如果以上都失败，请确认:")
    print("1. 模型ID的准确拼写（区分大小写）")
    print("2. 在 Ark 控制台的 模型广场 → 已开通模型 中查看完整模型ID")


if __name__ == "__main__":
    main()
