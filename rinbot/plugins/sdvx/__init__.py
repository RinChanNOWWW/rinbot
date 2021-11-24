# import nonebot
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot import on_command
from nonebot import get_driver
from nonebot.typing import T_State


from .config import Config
from .data_source import BindError, DataBase, NoPlays, UserNotFoundError, format_score

global_config = get_driver().config
rinbot_config = Config(**global_config.dict())


db = DataBase(rinbot_config)

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

bind = on_command("bind")


@bind.handle()
async def read_card(bot: Bot, event: Event, state: T_State):
    card = str(event.get_message()).strip()
    if card:
        state['card'] = card


@bind.got("card", prompt="请输入您的卡号")
async def bind_card(bot: Bot, event: Event, state: T_State):
    qq = event.get_user_id()
    card = state['card']
    print(card)
    # 首先查找 card 是否在数据库中
    try:
        user_id = db.get_user_id(card)
        db.bind_user_id_with_qq(user_id, qq)
    except UserNotFoundError as e:
        await bind.reject(f"卡号 {card} 不存在。")
        return
    except BindError as e:
        await bind.reject(f"绑定失败： {e}。")
        return

    await bind.finish(f"您的卡号为 {card}，绑定成功！")

recent = on_command("recent")


@recent.handle()
async def recent_play(bot: Bot, event: Event):
    qq = event.get_user_id()
    try:
        score = db.get_recent_score(int(qq))
        formatted = format_score(score)
    except UserNotFoundError:
        await bot.send(message="您还未绑定卡号。使用 `\\bind CARD` 绑定卡号。", event=event)
        return
    except NoPlays:
        await bot.send(message="您还没有游玩记录。", event=event)
        return
    except Exception as e:
        print("exception", e)
        await bot.send(message="未知错误。", event=event)
        return

    play = (f"曲名: {formatted['name']}\n" +
            f"Artist: {formatted['artist']}\n" +
            f"BPM: {formatted['bpm']}\n" +
            f"等级: {formatted['difficulty']} ({formatted['chart']})\n" +
            f"评价: {formatted['grade']}\n" +
            f"分数: {formatted['score']}\n" +
            f"时间: {formatted['timestamp']}\n"
            )

    await bot.send(message=f"最近的游玩记录:\n" + play, event=event)
