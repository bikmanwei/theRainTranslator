import os
import time
from openai import OpenAI, OpenAIError
from typing import Optional, List, Dict, Union, Tuple

class ChatGPTClient:
    """
    一个简洁的 ChatGPT SDK，用于与 OpenAI API 进行交互。

    主要功能:
    - 初始化 OpenAI 客户端。
    - 发送聊天请求并获取回复。
    - 支持自定义模型、系统消息和对话历史。
    - 统计 token 使用量和调用时间。

    使用方法:
    1. 设置环境变量 `OPENAI_API_KEY` 为你的 API 密钥。
    2. 创建 `ChatGPTClient` 实例。
    3. 调用 `chat` 方法进行对话。

    示例:
        >>> client = ChatGPTClient()
        >>> response = client.chat("你好，ChatGPT！")
        >>> print(response)
        你好！有什么可以帮助你的吗？

        >>> history = [
        ...     {"role": "user", "content": "珠穆朗玛峰有多高？"},
        ...     {"role": "assistant", "content": "珠穆朗玛峰的最新测量高度是8848.86米。"}
        ... ]
        >>> response = client.chat("谁测量了这个高度？", conversation_history=history)
        >>> print(response)
        这个高度是由中国和尼泊尔两国的测量登山队在2020年共同测量的。
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4.1-mini"):
        """
        初始化 ChatGPTClient。

        参数:
            api_key (Optional[str]): OpenAI API 密钥。如果未提供，则从环境变量 `OPENAI_API_KEY` 读取。
            model (str): 默认使用的模型名称，例如 "gpt-4o", "gpt-3.5-turbo"。
        """
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API密钥未提供。请设置 OPENAI_API_KEY 环境变量或在初始化时传入 api_key参数。")

        self.client = OpenAI(api_key=api_key)
        self.default_model = model
        self.total_tokens_used = 0
        self.total_calls = 0

    def chat(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 40000,  # 更合理的默认值
        **kwargs  # 允许传递其他 OpenAI API 参数
    ) -> Tuple[Optional[str], Dict]:
        """
        向 ChatGPT 发送消息并获取回复。

        参数:
            prompt (str): 用户当前的输入。
            system_message (Optional[str]): 系统消息，用于设定助手的行为或角色。
            conversation_history (Optional[List[Dict[str, str]]]):
                之前的对话历史。列表中的每个字典应包含 "role" ("user" 或 "assistant") 和 "content"。
            model (Optional[str]): 要使用的模型名称。如果未提供，则使用初始化时设置的默认模型。
            temperature (float): 控制输出的随机性，0 表示最确定性，2 表示最随机。
            max_tokens (int): 生成响应的最大 token 数量。
            **kwargs: 其他可以传递给 OpenAI API `chat.completions.create` 方法的参数。

        返回:
            Tuple[Optional[str], Dict]: 包含 ChatGPT 的回复文本和使用统计信息的元组。
            如果发生错误则回复文本为 None。统计信息包含 tokens_used, elapsed_time 等。
        """
        messages = []
        used_model = model if model else self.default_model
        
        # 显示调用前的提醒
        print(f"\n🤖 正在调用模型: {used_model}...")
        
        if system_message:
            messages.append({"role": "system", "content": system_message})

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": prompt})

        stats = {
            "model": used_model,
            "tokens_used": 0,
            "elapsed_time": 0,
            "success": False
        }
        
        start_time = time.time()
        
        try:
            completion = self.client.chat.completions.create(
                model=used_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # 计算使用的时间
            elapsed_time = time.time() - start_time
            
            # 获取使用的 token 数量
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            total_tokens = completion.usage.total_tokens
            
            # 更新统计信息
            self.total_tokens_used += total_tokens
            self.total_calls += 1
            
            stats.update({
                "success": True,
                "elapsed_time": elapsed_time,
                "tokens_used": total_tokens,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens
            })
            
            response_content = completion.choices[0].message.content
            result = response_content.strip() if response_content else None
            
            # 显示使用统计
            print(f"✅ 调用完成! 用时: {elapsed_time:.2f}秒")
            print(f"📊 Token统计: 提示词={prompt_tokens}, 回复={completion_tokens}, 总计={total_tokens}")
            
            return result, stats
            
        except OpenAIError as e:
            elapsed_time = time.time() - start_time
            stats["elapsed_time"] = elapsed_time
            print(f"❌ 发生 OpenAI API 错误: {e}")
            print(f"⏱️ 用时: {elapsed_time:.2f}秒")
            return None, stats
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            stats["elapsed_time"] = elapsed_time
            print(f"❌ 发生未知错误: {e}")
            print(f"⏱️ 用时: {elapsed_time:.2f}秒")
            return None, stats
    
    def get_usage_stats(self) -> Dict:
        """获取总体使用统计"""
        return {
            "total_tokens": self.total_tokens_used,
            "total_calls": self.total_calls,
            "average_tokens_per_call": self.total_tokens_used / self.total_calls if self.total_calls > 0 else 0
        }

# --- 使用示例 ---
if __name__ == "__main__":
    # 确保你已经设置了 OPENAI_API_KEY 环境变量
    # 例如: export OPENAI_API_KEY='sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    print("正在初始化 ChatGPT 客户端...")
    try:
        # 1. 基本用法
        print("\n--- 示例 1: 基本对话 ---")
        gpt_client = ChatGPTClient()  # 默认使用 gpt-4.1-mini
        # 你也可以指定模型，例如: gpt_client = ChatGPTClient(model="gpt-3.5-turbo")

        user_prompt = "你好，ChatGPT！你能做什么？"
        print(f"用户: {user_prompt}")
        response, stats = gpt_client.chat(user_prompt)
        if response:
            print(f"ChatGPT: {response}")
        else:
            print("未能获取回复。")

        # 2. 带有系统消息的对话
        print("\n--- 示例 2: 带系统消息的对话 ---")
        system_prompt = "你是一个乐于助人的AI助手，专门回答有关宇宙的问题，并且语言风格要像莎士比亚。"
        user_prompt_cosmic = "告诉我关于黑洞的奇妙之处。"
        print(f"系统设定: {system_prompt}")
        print(f"用户: {user_prompt_cosmic}")
        response_cosmic, stats = gpt_client.chat(user_prompt_cosmic, system_message=system_prompt)
        if response_cosmic:
            print(f"ChatGPT (莎士比亚风格): {response_cosmic}")

        # 3. 带有对话历史的连续对话
        print("\n--- 示例 3: 连续对话 ---")
        history = []

        user_prompt_1 = "法国的首都是哪里？"
        print(f"用户: {user_prompt_1}")
        response_1, stats = gpt_client.chat(user_prompt_1)
        if response_1:
            print(f"ChatGPT: {response_1}")
            history.append({"role": "user", "content": user_prompt_1})
            history.append({"role": "assistant", "content": response_1})
        else:
            print("未能获取回复。")

        if response_1:  # 只有在第一次成功后才继续
            user_prompt_2 = "那里有什么著名的建筑物？"
            print(f"用户: {user_prompt_2}")
            response_2, stats = gpt_client.chat(user_prompt_2, conversation_history=history)
            if response_2:
                print(f"ChatGPT: {response_2}")
            else:
                print("未能获取回复。")

        # 4. 更改模型和参数
        print("\n--- 示例 4: 使用不同模型和参数 ---")
        # 注意：gpt-3.5-turbo 可能更快，成本更低，但能力不如 gpt-4o
        user_prompt_creative = "写一句关于春天的小诗。"
        print(f"用户: {user_prompt_creative}")
        response_creative, stats = gpt_client.chat(
            user_prompt_creative,
            model="gpt-3.5-turbo",  # 临时覆盖默认模型
            temperature=0.9,
            max_tokens=50
        )
        if response_creative:
            print(f"ChatGPT (gpt-3.5-turbo, T=0.9): {response_creative}")
        
        # 显示总体使用统计
        usage = gpt_client.get_usage_stats()
        print("\n--- 总体使用统计 ---")
        print(f"总调用次数: {usage['total_calls']}")
        print(f"总Token消耗: {usage['total_tokens']}")
        print(f"平均每次调用Token: {usage['average_tokens_per_call']:.1f}")

    except ValueError as ve:
        print(f"初始化错误: {ve}")
    except Exception as e:
        print(f"发生意外错误: {e}")