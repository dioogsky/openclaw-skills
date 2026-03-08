#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尝试不同的 Seedream 模型ID格式
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
        "prompt": "a cat",
        "size": "1024x1024"
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
    
    print("🔍 尝试不同的 Seedream 模型ID格式...\n")
    
    # 尝试不同的模型ID格式（基于文档中的示例）
    models = [
        # Seedream 5.0
        "doubao-seedream-5-0-260128",
        "doubao-seedream-5-0-lite-260128",
        # Seedream 4.5
        "doubao-seedream-4-5-250115",
        # Seedream 4.0
        "doubao-seedream-4-0-250115",
        "doubao-seedream-4-0-250128",
        "doubao-seedream-4-0-250228",
        # Seedream 3.0
        "doubao-seedream-3-0-t2i-250115",
        "doubao-seedream-3-0-t2i-250128",
        # SeedEdit
        "doubao-seededit-3-0-i2i-250115",
        # 不带日期的版本
        "doubao-seedream-4-0",
        "doubao-seedream-3-0-t2i",
    ]
    
    available_models = []
    
    for model_id in models:
        print(f"尝试 {model_id}...", end=" ")
        is_available, status = try_model(api_key, model_id)
        print(status)
        
        if is_available:
            print(f"\n✅ 找到可用模型: {model_id}")
            available_models.append(model_id)
    
    print("\n" + "="*60)
    
    if available_models:
        print(f"\n✅ 找到 {len(available_models)} 个可用模型:")
        for model_id in available_models:
            print(f"   • {model_id}")
    else:
        print("\n❌ 没有找到可用的图片生成模型")
        print("\n📋 请在 Ark 控制台确认已开通的模型ID:")
        print("   1. 访问 https://console.volcengine.com/ark")
        print("   2. 左侧菜单 → 模型广场 → 已开通模型")
        print("   3. 查看准确的模型ID")


if __name__ == "__main__":
    main()
