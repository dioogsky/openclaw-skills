#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即梦AI视频生成工具 - 带声音版本
使用 Ark API Key 认证
"""

import os
import sys
import json
import time
from datetime import datetime
import requests

# 设置UTF-8编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# API配置
ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/contents/generations"

# 默认模型（带声音）
DEFAULT_MODEL = "doubao-seedance-1-5-pro-251215"


def load_credentials():
    """加载API凭证"""
    env_file = os.path.expanduser("~/.openclaw/.credentials/volcengine-dreamina.env")
    
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    api_key = os.environ.get('ARK_API_KEY')
    
    if not api_key:
        print("错误：未找到 ARK_API_KEY")
        print(f"请确保 {env_file} 文件存在并包含：")
        print("  ARK_API_KEY=your-ark-api-key")
        sys.exit(1)
    
    return api_key


def create_task(api_key, prompt, model=None, reference_image=None):
    """创建视频生成任务"""
    if model is None:
        model = DEFAULT_MODEL
    
    url = f"{ENDPOINT}/tasks"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 构建 content
    content = []
    
    # 如果有参考图，先添加图片
    if reference_image and os.path.exists(reference_image):
        print(f"📎 使用参考图: {reference_image}")
        import base64
        with open(reference_image, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image_data}"
            }
        })
    
    # 添加文本提示词
    content.append({
        "type": "text",
        "text": prompt
    })
    
    payload = {
        "model": model,
        "content": content
    }
    
    print(f"正在创建视频生成任务...")
    print(f"   模型: {model}")
    print(f"   提示词: {prompt}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"状态码: {e.response.status_code}")
            print(f"错误详情: {e.response.text}")
        sys.exit(1)


def get_task_status(api_key, task_id):
    """查询任务状态"""
    url = f"{ENDPOINT}/tasks/{task_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"查询失败: {e}")
        sys.exit(1)


def wait_for_completion(api_key, task_id, timeout=300):
    """等待任务完成"""
    print(f"\n等待任务完成 (任务ID: {task_id})...")
    print(f"   超时时间: {timeout}秒")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = get_task_status(api_key, task_id)
        status = result.get('status', 'unknown')
        
        if status == 'succeeded':
            print(f"✅ 任务完成!")
            return result
        elif status == 'failed':
            print(f"❌ 任务失败: {result.get('error', '未知错误')}")
            sys.exit(1)
        elif status == 'running':
            print(f"   ⏳ 生成中... ({int(time.time() - start_time)}s)")
        else:
            print(f"   状态: {status}")
        
        time.sleep(5)
    
    print(f"⏰ 等待超时")
    sys.exit(1)


def download_video(url, output_path):
    """下载视频文件"""
    print(f"\n📥 正在下载视频...")
    
    try:
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(output_path)
        print(f"✅ 视频已保存: {output_path}")
        print(f"   文件大小: {file_size / 1024 / 1024:.2f} MB")
        return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False


def generate(prompt, output=None, model=None, wait=True, reference_image=None):
    """生成视频的主函数"""
    api_key = load_credentials()
    
    # 创建任务
    result = create_task(api_key, prompt, model, reference_image)
    
    task_id = result.get('id')
    
    if not task_id:
        print("❌ 未能获取任务ID")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    print(f"✅ 任务已创建 (ID: {task_id})")
    
    if not wait:
        print(f"   使用以下命令查询状态:")
        print(f"   python jimeng_video.py status {task_id}")
        return result
    
    # 等待完成
    final_result = wait_for_completion(api_key, task_id)
    
    # 下载视频
    video_url = final_result.get('content', {}).get('video_url')
    if video_url:
        if output is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output = f"jimeng_video_{timestamp}.mp4"
        
        download_video(video_url, output)
        
        # 显示结果信息
        print(f"\n📊 生成结果:")
        print(f"   分辨率: {final_result.get('resolution', 'unknown')}")
        print(f"   时长: {final_result.get('duration', 'unknown')}秒")
        print(f"   帧率: {final_result.get('framespersecond', 'unknown')}fps")
        print(f"   带音频: {'✅ 是' if final_result.get('generate_audio') else '❌ 否'}")
    else:
        print("⚠️ 未找到视频URL")
        print(json.dumps(final_result, indent=2, ensure_ascii=False))
    
    return final_result


def status(task_id):
    """查询任务状态"""
    api_key = load_credentials()
    result = get_task_status(api_key, task_id)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def list_models():
    """列出可用模型"""
    print("可用模型列表:")
    print()
    print("🌟 推荐（带声音）:")
    print(f"  doubao-seedance-1-5-pro-251215")
    print()
    print("其他模型:")
    print(f"  doubao-seedance-1-0-pro-250528")
    print(f"  doubao-seedance-1-0-lite-t2v-250428")
    print(f"  doubao-seedance-2-0-260128")


def main():
    if len(sys.argv) < 2:
        print("即梦AI视频生成工具 v2.0")
        print()
        print("用法:")
        print(f"  {sys.argv[0]} generate <提示词> [选项]")
        print(f"  {sys.argv[0]} status <任务ID>")
        print(f"  {sys.argv[0]} list-models")
        print()
        print("示例:")
        print(f'  {sys.argv[0]} generate "一只可爱的猫咪在阳光下打盹" -o cat.mp4')
        print()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "generate":
        if len(sys.argv) < 3:
            print("请提供提示词")
            sys.exit(1)
        
        prompt = sys.argv[2]
        output = None
        model = None
        wait = True
        reference_image = None
        
        # 解析参数
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "-o" or sys.argv[i] == "--output":
                output = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "-m" or sys.argv[i] == "--model":
                model = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "-r" or sys.argv[i] == "--reference":
                reference_image = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--no-wait":
                wait = False
                i += 1
            else:
                i += 1
        
        generate(prompt, output, model, wait, reference_image)
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("请提供任务ID")
            sys.exit(1)
        status(sys.argv[2])
    
    elif command == "list-models":
        list_models()
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
