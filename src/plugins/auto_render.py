from re import findall
from nonebot import logger, on_message, get_plugin_config
from nonebot.matcher import Matcher
from nonebot_plugin_htmlrender import get_new_page
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from pydantic import BaseModel, Field
from yarl import URL

pep = on_message(block=False, priority=10)
reg = r"http[s]?://(?:[a-zA-Z0-9$-_@.&+!*',]|[()%#]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"


class Config(BaseModel):
    auto_render_hosts: list[str] = Field(default_factory=list)


config = get_plugin_config(Config)


@pep.handle()
async def pep_handler(matcher: Matcher, event: MessageEvent):
    message = event.get_message()
    txt = message.extract_plain_text()
    if len(urls := findall(reg, txt)) == 0:
        return

    async with get_new_page() as page:
        for url in urls:
            try:
                if URL(url).host not in config.auto_render_hosts:
                    continue
                await page.goto(url)
                await page.wait_for_load_state("load")
                img = await page.screenshot(type="jpeg", full_page=True)
                await matcher.send(MessageSegment.image(img))
            except Exception as e:
                logger.error(f"Error when render url: {url}\n{e}")
                continue
