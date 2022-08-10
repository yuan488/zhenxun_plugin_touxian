from ast import If
import json
import nonebot
from nonebot.adapters import Message
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, NoticeEvent
from nonebot.adapters.onebot.exception import ActionFailed
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from typing import Union, Optional

__zx_plugin_name__ = "头衔"
__plugin_usage__ = """
usage：
    群员自助申请头衔，需要让真寻当群主哦~~~
    指令：
        头衔 XXX
    注意：
        头衔最多6个字。
        若只发送 [头衔] ，则删除用户原有头衔。
""".strip()
__plugin_des__ = "群员自助申请头衔"
__plugin_cmd__ = [
    "头衔"
]
__plugin_version__ = 0.1
__plugin_author__ = "小源"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["头衔"],
}
__plugin_cd_limit__ = {
    "cd": 30,
    "rst": "改太快了，冷却中！"
}

title = on_command('头衔', priority=1, block=True)

def MsgText(data: str):
    """
    返回消息文本段内容(即去除 cq 码后的内容)
    :param data: event.json()
    :return: str
    """
    try:
        data = json.loads(data)
        # 过滤出类型为 text 的【并且过滤内容为空的】
        msg_text_list = filter(lambda x: x["type"] == "text" and x["data"]["text"].replace(" ", "") != "",
                               data["message"])
        # 拼接成字符串并且去除两端空格
        msg_text = " ".join(map(lambda x: x["data"]["text"].strip(), msg_text_list)).strip()
        return msg_text
    except:
        return ""

async def change_s_title(bot: Bot, matcher: Matcher, gid: int, uid: int, s_title: Optional[str]):
    """
    改头衔
    :param bot: bot
    :param matcher: matcher
    :param gid: 群号
    :param uid: 用户号
    :param s_title: 头衔
    """
    try:
        await bot.set_group_special_title(
            group_id=gid,
            user_id=uid,
            special_title=s_title,
            duration=-1,
        )
    except ActionFailed:
        logger.info("权限不足")
    else:
        logger.info(f"头衔操作成功:{s_title}")

@title.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /头衔 xxx  自助申请头衔
    """
    msg = MsgText(event.json())
    s_title = msg.replace(" ", "").replace("头衔", "",1)
    gid = event.group_id
    uid = event.user_id
    await change_s_title(bot, matcher, gid, uid, s_title)
