import asyncio
from typing import Generator
from requests.exceptions import SSLError, ProxyError, RequestException
from urllib3.exceptions import MaxRetryError
from httpx import HTTPStatusError, ConnectTimeout

from EdgeGPT import Chatbot as EdgeChatbot, ConversationStyle

import re
import config
from utils import *

class BingAdapter:
    cookieData = None
    count: int = 0

    conversation_style: ConversationStyle = None

    bot: EdgeChatbot
    """实例"""

    def __init__(self, session_id: str = "unknown", conversation_style: ConversationStyle = ConversationStyle.creative):
        self.session_id = session_id
        self.conversation_style = conversation_style
        self.cookieData = []
        for line in config.bing_cookie.split("; "):
            name, value = line.split("=", 1)
            self.cookieData.append({"name": name, "value": value})

        self.bot = EdgeChatbot(cookies=self.cookieData, proxy= "http://" + config.loc_proxy)

    async def rollback(self):
        raise "BotOperationNotSupportedException"

    async def on_reset(self):
        self.count = 0
        await self.bot.reset()

    async def ask(self, prompt: str) -> Generator[str, None, None]:
        self.count = self.count + 1
        parsed_content = ''
        try:
            async for final, response in self.bot.ask_stream(prompt=prompt,
                                                             conversation_style=self.conversation_style,
                                                             wss_link=config.bing_wss_link):
                if not final:
                    response = re.sub(r"\[\^\d+\^\]", "", response)
                    if config.bing_show_references:
                        response = re.sub(r"\[(\d+)\]: ", r"\1: ", response)
                    else:
                        response = re.sub(r"(\[\d+\]\: .+)+\n", "", response)
                        response = re.sub(r"\[\d+\]", "", response)
                    parsed_content = response

                else:
                    try:
                        max_messages = response["item"]["throttling"]["maxNumUserMessagesInConversation"]
                    except:
                        max_messages = config.context_length
                    remaining_conversations = f'\n剩余回复数：{self.count} / {max_messages} '
                    if len(response["item"].get('messages', [])) > 1 and config.bing_show_suggestions:
                        suggestions = response["item"]["messages"][-1].get("suggestedResponses", [])
                        if len(suggestions) > 0:
                            parsed_content = parsed_content + '\n猜你想问：  \n'
                            for suggestion in suggestions:
                                parsed_content = parsed_content + f"* {suggestion.get('text')}  \n"
                        yield parsed_content
                    parsed_content = parsed_content + remaining_conversations
                    # not final的parsed_content已经yield走了，只能在末尾加剩余回复数，或者改用EdgeGPT自己封装的ask之后再正则替换
                    if parsed_content == remaining_conversations:  # No content
                        yield "Bing 已结束本次会话。继续发送消息将重新开启一个新会话。"
                        await self.on_reset()
                        return

                yield parsed_content
            # print("[Bing AI 响应] " + parsed_content)
        except (RequestException, SSLError, ProxyError, MaxRetryError, HTTPStatusError, ConnectTimeout) as e:  # 网络异常
            raise e
        except Exception as e:
            yield "Bing 已结束本次会话。继续发送消息将重新开启一个新会话。"
            await self.on_reset()
            return
    async def preset_ask(self, role: str, text: str):
        yield None  # Bing 不使用预设功能