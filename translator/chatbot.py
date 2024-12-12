import time
from collections import deque
from loguru import logger
from openai import OpenAI
import tiktoken
from dataclasses import dataclass
from typing import Dict
from .config import PRICE_PER_1K_TOKENS_BLT


@dataclass
class UsageMetrics:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    first_char_time: float = None


class Chatbot:
    def __init__(
        self,
        api_key,
        model="gpt-4o-mini",
        base_url="https://api.bltcy.ai/v1",
        system_prompt=None,
        initial_assistant_message=None,
        max_tokens=1024,
        temperature=0.7,
        max_history_length=10,
    ):
        """通用聊天机器人（使用柏拉图AI）"""
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.system_prompt = (
            system_prompt
            or """你是一个友好的AI助手。
                            - 你应该用简洁清晰的语言回答问题
                            - 对于复杂问题，你应该分步骤解释
                            - 你应该保持礼貌和专业性
                            - 如果你不确定答案，要诚实地说出来"""
        )

        # 初始化对话历史
        self.conversation_history = deque(
            [{"role": "system", "content": self.system_prompt}],
            maxlen=max_history_length,
        )
        if initial_assistant_message:
            self.conversation_history.append(
                {"role": "assistant", "content": initial_assistant_message}
            )

        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_history_length = max_history_length
        self.encoding = tiktoken.get_encoding("o200k_base")
        self.usage_metrics = UsageMetrics()
        self.first_char_time = None

    def count_tokens(self, messages) -> int:
        """计算消息列表的token数"""
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # 每条消息的基础token
            for key, value in message.items():
                num_tokens += len(self.encoding.encode(str(value)))
                if key == "name":
                    num_tokens += -1  # 如果包含name字段，减去1个token
        num_tokens += 2  # 对话开始和结束的token
        return num_tokens

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """计算API调用成本"""
        if self.model not in PRICE_PER_1K_TOKENS_BLT:
            return 0.0

        prices = PRICE_PER_1K_TOKENS_BLT[self.model]
        prompt_cost = (prompt_tokens / 1000) * prices["prompt"]
        completion_cost = (completion_tokens / 1000) * prices["completion"]
        return prompt_cost + completion_cost

    def update_usage_metrics(self, prompt_tokens: int, completion_tokens: int):
        """更新使用量指标"""
        self.usage_metrics.prompt_tokens += prompt_tokens
        self.usage_metrics.completion_tokens += completion_tokens
        self.usage_metrics.total_tokens += prompt_tokens + completion_tokens
        cost = self.calculate_cost(prompt_tokens, completion_tokens)
        self.usage_metrics.total_cost += cost

    def chat_stream(self, message: str):
        if not message.strip():
            yield "Error: Empty message"
            return

        self.conversation_history.append({"role": "user", "content": message})
        prompt_tokens = self.count_tokens(list(self.conversation_history))

        try:
            start_time = time.time()
            stream_response = self.client.chat.completions.create(
                messages=self.conversation_history,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True,
            )
            collected_content = []
            for chunk in stream_response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    collected_content.append(content)
                    if self.first_char_time is None:
                        self.first_char_time = time.time() - start_time
                        self.usage_metrics.first_char_time = self.first_char_time
                    yield content

            full_response = "".join(collected_content)
            self.conversation_history.append(
                {"role": "assistant", "content": full_response}
            )
            completion_tokens = self.count_tokens(
                [{"role": "assistant", "content": full_response}]
            )
            self.update_usage_metrics(prompt_tokens, completion_tokens)
        except Exception as e:
            error_message = f"Error during chat: {str(e)}"
            self.conversation_history.append(
                {"role": "assistant", "content": error_message}
            )
            yield error_message

    def chat(self, message: str, stream=True):
        if stream:
            return self.chat_stream(message)
        else:
            self.conversation_history.append({"role": "user", "content": message})
            prompt_tokens = self.count_tokens(list(self.conversation_history))

            try:
                response = (
                    self.client.chat.completions.create(
                        messages=self.conversation_history,
                        model=self.model,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        stream=False,
                    )
                    .choices[0]
                    .message.content
                )
                self.conversation_history.append(
                    {"role": "assistant", "content": response}
                )
                completion_tokens = self.count_tokens(
                    [{"role": "assistant", "content": response}]
                )
                self.update_usage_metrics(prompt_tokens, completion_tokens)

                return response
            except Exception as e:
                return f"Error during chat: {str(e)}"

    def get_usage_statistics(self, debug=False) -> Dict[str, float]:
        """获取使用统计信息"""
        stat = {
            "prompt_tokens": self.usage_metrics.prompt_tokens,
            "completion_tokens": self.usage_metrics.completion_tokens,
            "total_tokens": self.usage_metrics.total_tokens,
            "total_cost_rmb": self.usage_metrics.total_cost,
        }
        if debug:
            # logger.debug(f"提示令牌数：{self.usage_metrics.prompt_tokens}")
            # logger.debug(f"补全令牌数：{self.usage_metrics.completion_tokens}")
            logger.debug(f"累计令牌数：{self.usage_metrics.total_tokens}")
            logger.debug(f"累计成本：{self.usage_metrics.total_cost:.6f}元")
        return stat

    def get_response(self, message: str, stream=True, print_response=True, debug=False):
        try:
            metrics = {
                "start_time": time.time(),
                "first_char_time": None,
                "chunk_count": 0,
                "total_tokens": 0,
            }

            response = self.chat(message, stream=stream)
            if stream:
                response_chunks = []
                for chunk in response:
                    if chunk:
                        metrics["chunk_count"] += 1
                        if print_response:
                            print(chunk, end="", flush=True)
                        response_chunks.append(chunk)
                        metrics["total_tokens"] += len(chunk.split())

                full_response = "".join(response_chunks)

                total_time = time.time() - metrics["start_time"]
                if debug:
                    print("\n")
                    logger.debug(f"模型：{self.model}")
                    logger.debug(f"总耗时：{total_time:.2f}秒")
                    logger.debug(f"总字数：{len(full_response)}")
                    logger.debug(f"每秒字数：{len(full_response) / total_time:.2f}")
                    logger.debug(f"总块数：{metrics['chunk_count']}")
                    logger.debug(
                        f"每秒令牌数：{metrics['total_tokens'] / total_time:.2f}"
                    )
                    logger.debug(f"首字延迟: {self.first_char_time:.2f}秒")
                stat = self.get_usage_statistics(debug)

                return full_response, stat
            else:
                if print_response:
                    print(response)
                total_time = time.time() - metrics["start_time"]
                if debug:
                    print("\n")
                    logger.debug(f"总耗时：{total_time:.2f}秒")
                stat = self.get_usage_statistics(debug)
                return response, stat
        except Exception as e:
            error_message = f"Error displaying response: {str(e)}"
            print(error_message)
            return None