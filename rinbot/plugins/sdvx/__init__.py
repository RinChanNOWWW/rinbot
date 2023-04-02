import time

from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot import on_command
from nonebot import get_driver
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_keyword
from nonebot.rule import to_me
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

# 绑定卡号
bind = on_command("sdvx_bind")


@bind.handle()
async def read_card(bot: Bot, event: Event, state: T_State):
    card = str(event.get_message()).strip()
    if card:
        state['card'] = card


@bind.got("card", prompt="请输入您的卡号")
async def bind_card(bot: Bot, event: Event, state: T_State):
    qq = event.get_user_id()
    card = state['card']
    # 首先查找 card 是否在数据库中
    try:
        user_id = db.get_user_id(card)
        db.bind_user_id_with_qq(user_id, qq)
    except UserNotFoundError as e:
        await bind.finish(f"卡号 {card} 不存在。")
    except BindError as e:
        await bind.finish(f"绑定失败： {e}。")

    await bind.finish(f"您的卡号为 {card}，绑定成功！")

# 查询最近的一次游玩分数
recent = on_command("sdvx_recent")


@recent.handle()
async def recent_play(bot: Bot, event: Event):
    qq = event.get_user_id()
    try:
        score = db.get_recent_scores(int(qq))
        formatted = format_score(score)
        play = (
            f"最近的游玩记录:\n" +
            f"曲名: {formatted['name']}\n" +
            f"Artist: {formatted['artist']}\n" +
            f"BPM: {formatted['bpm']}\n" +
            f"等级: {formatted['difficulty']} ({formatted['chart']})\n" +
            f"评价: {formatted['grade']}\n" +
            f"分数: {formatted['score']}\n" +
            f"Max-Chain: {formatted['combo']}\n" +
            f"Critical: {formatted['critical']}\n" +
            f"Near: {formatted['near']}\n" +
            f"Error: {formatted['error']}\n" +
            f"时间: {formatted['timestamp']}\n"
        )
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

    await bot.send(message=play, event=event)

# 查询今日游玩情况
today = on_command("sdvx_today")


@today.handle()
async def today_play(bot: Bot, event: Event):
    qq = event.get_user_id()
    try:
        scores = db.get_today_scores(int(qq))
        formatted_scores = [format_score(score) for score in scores]
        best = max(formatted_scores, key=lambda x: x['score'])
        worst = min(formatted_scores, key=lambda x: x['score'])
        start = min(scores, key=lambda x: x['timestamp'])
        start_time = time.strftime(
            "%H:%M:%S", time.localtime(start['timestamp']))
        end = max(scores, key=lambda x: x['timestamp'])
        end_time = time.strftime("%H:%M:%S", time.localtime(end['timestamp']))
        now = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        play = (
            f"今日 ({now}) 总共游玩 {len(scores)} 首曲目:\n" +
            f"最高分: {best['score']} ({best['name']} {best['chart']} {best['difficulty']})\n" +
            f"最低分: {worst['score']} ({worst['name']} {worst['chart']} {worst['difficulty']})\n" +
            f"游玩时间: {start_time}-{end_time}\n"
        )
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

    await bot.send(message=play, event=event)

bye = on_keyword(set(["下线", "拜拜", "睡觉", "bye", "Bye"]),
                 rule=to_me(), permission=SUPERUSER)


@bye.handle()
async def bye(bot: Bot, event: Event):
    await bot.send(message="おやすみなさい～Bye～", event=event)
    exit(0)
