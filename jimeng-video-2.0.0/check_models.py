#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查可用的即梦AI模型
"""

import os
import sys
import requests

# 设置UTF-8编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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


def check_model(api_key, model_id):
    """检查模型是否可用"""
    url = f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model_id,
        "content": [{"type": "text", "text": "test"}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            return True, "可用"
        elif "ModelNotOpen" in str(data) or response.status_code == 404:
            return False, "未开通"
        elif "Unauthorized" in str(data) or response.status_code == 401:
            return False, "认证失败"
        else:
            return False, f"错误: {data.get('error', {}).get('message', '未知')}"
    except Exception as e:
        return False, f"请求失败: {e}"


def main():
    api_key = load_credentials()
    
    if not api_key:
        print("❌ 未找到 ARK_API_KEY")
        sys.exit(1)
    
    print("🔍 检查即梦AI模型状态...\n")
    
    models = [
        ("doubao-seedance-1-5-pro-251215", "Seedance 1.5 Pro (带声音) ⭐推荐"),
        ("doubao-seedance-2-0-260128", "Seedance 2.0 (最新版)"),
        ("doubao-seedance-1-0-pro-250528", "Seedance 1.0 Pro"),
        ("doubao-seedance-1-0-lite-t2v-250428", "Seedance 1.0 Lite (轻量版)"),
        ("doubao-seedance-1-0-i2v-250428", "Seedance 1.0 I2V (图生视频)"),
    ]
    
    available_models = []
    
    for model_id, description in models:
        print(f"检查 {model_id}...", end=" ")
        is_available, status = check_model(api_key, model_id)
        
        if is_available:
            print(f"✅ {status}")
            available_models.append((model_id, description))
        else:
            print(f"❌ {status}")
    
    print("\n" + "="*60)
    
    if available_models:
        print(f"\n✅ 你有 {len(available_models)} 个可用模型:")
        for model_id, desc in available_models:
            print(f"   • {desc}")
            print(f"     ID: {model_id}")
    else:
        print("\n❌ 没有可用的模型")
        print("\n📋 你需要在 Ark 控制台开通模型服务:")
        print("   1. 访问 https://console.volcengine.com/ark")
        print("   2. 左侧菜单 → 模型广场")
        print("   3. 搜索 'seedance' 或 '即梦'")
        print("   4. 选择模型并点击'开通服务'")
        print("\n💡 推荐开通: doubao-seedance-1-5-pro-251215 (带声音)")


if __name__ == "__main__":
    main()
