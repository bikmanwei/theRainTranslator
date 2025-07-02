# 雨滴翻译器 (Rain Translator)

一个将用户输入的字符转换为雨相关诗歌的创意Web应用。使用ChatGPT API将随机字符串转换为富有想象力的雨主题诗歌。

## 项目介绍

雨滴翻译器是一个创意文本处理工具，它能够：
- 接收用户输入的最多10个字符
- 通过ChatGPT API将字符转换为雨主题的诗歌
- 提供实时进度条显示
- 支持自动提交（10字符时）或手动提交（回车键）
- 显示转换历史记录

## 快速启动指南

### 1. 环境准备

确保你的系统已安装：
- Python 3.7+
- pip（Python包管理器）

### 2. 获取OpenAI API密钥

1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册并登录账户
3. 获取API密钥

### 3. 项目配置

1. **克隆或下载项目到本地**

2. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   
   在项目根目录创建 `.env` 文件，添加以下内容：
   ```
   OPENAI_API_KEY=你的OpenAI_API密钥
   PROMPT_TEXT=你的自定义提示词（可选，有默认值）
   ```

### 4. 启动服务

在项目根目录运行：
```bash
python translate_ChatGPT.py
```

看到以下信息表示启动成功：
```
🌧️ 雨滴翻译器启动中...
✅ ChatGPT客户端初始化成功
🚀 服务器启动在 http://localhost:5001
```

### 5. 使用网页

1. **打开浏览器**，访问：`http://localhost:5001`

2. **使用方式**：
   - 在左侧输入框输入最多10个字符
   - 方式一：输入满10个字符后自动提交转换
   - 方式二：输入任意字符后按回车键提交
   - 右侧会显示转换过程和结果

3. **功能特点**：
   - 实时字符计数和进度条
   - 转换过程中显示加载动画
   - 自动保存最近10次转换记录
   - 每条记录显示输入内容、转换结果和时间戳

## 故障排除

### 常见问题

1. **服务启动失败**
   - 检查Python版本是否为3.7+
   - 确认已安装所有依赖：`pip install -r requirements.txt`

2. **API调用失败**
   - 检查`.env`文件中的`OPENAI_API_KEY`是否正确
   - 确认OpenAI账户有足够的API额度
   - 检查网络连接是否正常

3. **网页无法访问**
   - 确认服务已成功启动
   - 检查端口5001是否被占用
   - 尝试访问：`http://127.0.0.1:5001`

### 健康检查

访问 `http://localhost:5001/api/health` 检查服务状态

## 技术架构

- **前端**：HTML + CSS + JavaScript
- **后端**：Python Flask
- **AI服务**：OpenAI ChatGPT API
- **主要文件**：
  - `index.html` - 网页界面
  - `script.js` - 前端交互逻辑
  - `style.css` - 样式文件
  - `translate_ChatGPT.py` - 后端服务
  - `ChatGPT_SDK.py` - ChatGPT API封装

## 启动服务