#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雨滴翻译器 - 字符到诗歌的转换服务
使用ChatGPT API将用户输入的字符转换为雨相关的诗歌
"""
from get_prompt import get_prompt_rainTrans
import os
import json
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from ChatGPT_SDK import ChatGPTClient

# 加载环境变量
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # 允许跨域请求

# 初始化ChatGPT客户端
try:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    client = ChatGPTClient(api_key=api_key)
    print("✅ ChatGPT客户端初始化成功")
except Exception as e:
    print(f"❌ ChatGPT客户端初始化失败: {e}")
    client = None



def get_prompt_text():
    """从 get_prompt.py 获取提示词"""
    try:
        return get_prompt_rainTrans()
    except Exception as e:
        raise ValueError(f"Failed to get prompt from get_prompt.py: {e}")

def translate_text_to_poetry(input_text):
    """
    将输入文本转换为雨相关的诗歌
    
    Args:
        input_text (str): 用户输入的字符串
        
    Returns:
        str: 转换后的诗歌，如果失败则返回None
    """
    if not client:
        return None
        
    try:
        # 获取提示词模板
        prompt_template = get_prompt_text()
        
        # 替换模板中的占位符
        user_prompt = prompt_template.replace('{{input text}}', input_text)
        
        # 系统消息
        system_message = "You are a creative AI poet specializing in rain-themed poetry and character transformation."
        
        print(f"🌧️ 正在处理输入: '{input_text}'")
        
        # 调用ChatGPT API
        response, stats = client.chat(
            prompt=user_prompt,
            system_message=system_message,
            temperature=0.8,  # 较高的创造性
            max_tokens=1000
        )
        
        if response:
            print(f"✅ 转换成功，用时: {stats.get('elapsed_time', 0):.2f}秒")
            return response
        else:
            print("❌ ChatGPT返回空响应")
            return None
            
    except Exception as e:
        print(f"❌ 文本转换失败: {str(e)}")
        return None

@app.route('/')
def index():
    """主页路由"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """静态文件服务"""
    return send_from_directory('.', filename)

@app.route('/api/translate', methods=['POST'])
def translate_api():
    """
    翻译API端点
    接收POST请求，包含要转换的文本
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': '请求数据格式错误，需要包含text字段'
            }), 400
        
        input_text = data['text'].strip()
        
        if not input_text:
            return jsonify({
                'success': False,
                'error': '输入文本不能为空'
            }), 400
        
        if len(input_text) > 15:
            return jsonify({
                'success': False,
                'error': '输入文本长度不能超过15个字符'
            }), 400
        
        # 调用翻译函数
        result = translate_text_to_poetry(input_text)
        
        if result:
            return jsonify({
                'success': True,
                'input': input_text,
                'output': result,
                'timestamp': int(time.time() * 1000)  # 毫秒时间戳
            })
        else:
            return jsonify({
                'success': False,
                'error': 'ChatGPT服务暂时不可用，请稍后重试'
            }), 500
            
    except Exception as e:
        print(f"❌ API错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'chatgpt_available': client is not None,
        'timestamp': int(time.time() * 1000)
    })

if __name__ == '__main__':
    import time
    
    print("🌧️ 雨滴翻译器启动中...")
    print(f"📝 提示词: {get_prompt_text()[:100]}...")
    
    # 检查环境变量
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️ 警告: 未找到OPENAI_API_KEY环境变量")
    
    if not os.getenv('PROMPT_TEXT'):
        print("⚠️ 警告: 未找到PROMPT_TEXT环境变量，使用默认提示词")
    
    # 启动Flask应用
    print("🚀 服务器启动在 http://localhost:5001")
    print("📡 API端点: http://localhost:5001/api/translate")
    print("💚 健康检查: http://localhost:5001/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5001)