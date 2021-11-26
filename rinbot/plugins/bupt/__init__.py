import random
from typing import AnyStr

from nonebot import get_driver
from nonebot.adapters.cqhttp.event import Event
from nonebot.plugin import on_keyword, on_regex
from nonebot.adapters import Bot
from nonebot.typing import T_State

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

rest = ["新一", "新二", "老一", "老二", "风味"]

menu = {
    "新一": ["面", "粥", "自选", "铁板砂锅"],
    "新二": ["面", "自选"],
    "老一": ["面", "自选"],
    "老二": ["牛肉汤", "烤肉饭", "大鸡饭", "自选", "盖浇饭", "羊肉烩面"],
    "风味": ["香锅", "魔饭青年", "意面", "粥", "汉堡", "自选"]
}

where_to_eat = on_keyword(set(["去哪吃"]))


@where_to_eat.handle()
async def to_eat(bot: Bot, event: Event):
    r = random.randint(0, len(rest) + 1)
    if r >= len(rest):
        await bot.send(message="随便你。", event=event)
    else:
        await bot.send(message=f'去{rest[r]}吃吧。', event=event)

what_to_eat = on_regex(pattern="^[去|在](.*)吃啥$")


@what_to_eat.handle()
async def pick_menu(bot: Bot, event: Event, state: T_State):
    r = state['_matched_groups'][0]
    if r not in menu:
        if r == '':
            i = random.randint(0, len(rest))
            j = random.randint(0, len(rest[i]))
            await bot.send(message=f'去{rest[i]}吃{menu[rest[i]][j]}吧。', event=event)
        else:
            await bot.send(message=f"在巴普特找不到{r}这个餐厅捏。", event=event)
    else:
        meals = menu[r]
        m = random.randint(0, len(meals) + 1)
        if m >= len(meals):
            await bot.send(message=f'随便你。', event=event)
        else:
            await bot.send(message=f'去{r}吃{meals[m]}吧。', event=event)
