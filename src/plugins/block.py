from nonebot import get_plugin_config
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from pydantic import BaseModel, Field


class Config(BaseModel):
    white_group_list: list[int] = Field(default_factory=list)
    white_private_list: list[int] = Field(default_factory=list)

    black_group_list: list[int] = Field(default_factory=list)
    black_private_list: list[int] = Field(default_factory=list)

    use_white: bool = True


config = get_plugin_config(Config)


@event_preprocessor
async def block_event(event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id

        if config.use_white:
            if group_id not in config.white_group_list:
                raise IgnoredException("group is blocked")
            if group_id in config.black_group_list:
                raise IgnoredException("group is blocked")
            return
        else:
            if (
                group_id in config.black_group_list
                and group_id not in config.white_group_list
            ):
                raise IgnoredException("group is blocked")
            return
    else:
        user_id = event.user_id

        if config.use_white:
            if user_id not in config.white_private_list:
                raise IgnoredException("user is blocked")
            if user_id in config.black_private_list:
                raise IgnoredException("user is blocked")
            return
        else:
            if (
                user_id in config.black_private_list
                and user_id not in config.white_private_list
            ):
                raise IgnoredException("user is blocked")
            return
