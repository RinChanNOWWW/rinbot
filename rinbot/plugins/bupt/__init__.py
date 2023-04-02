import base64
from io import BytesIO
import json
import random

from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11 import Message
from nonebot.plugin import on_keyword, on_regex
from nonebot.adapters import Bot
from nonebot.typing import T_State

from buptelecmon.electricitymonitor import ElectricityMonitor
import qrcode

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

menu_file = 'rinbot/plugins/bupt/menu.json'

bupt_help = on_command('bupt_help')


@bupt_help.handle()
async def help(bot: Bot, event: Event):
    msg = """BUPT相关功能:
- 去哪吃: 去哪个食堂吃饭。
- 去<食堂名>吃啥。
- 来个菜单: 查看支持的食堂与菜品。
- 查电费 <宿舍号>: 查询宿舍电量。
- 充电费 <宿舍号>: 生成充电费微信二维码。
电费相关功能详见: https://github.com/jerrymakesjelly/electricity-monitor
"""
    await bot.send(event, msg)

where_to_eat = on_keyword(set(["去哪吃"]))


@where_to_eat.handle()
async def to_eat(bot: Bot, event: Event):
    try:
        f = open(menu_file)
        menu = json.load(f)
        rest = list(dict(menu).keys())
    except Exception as e:
        await bot.send(event, f'获取菜单失败: {e}')
        return

    r = random.randint(0, len(rest))
    if r >= len(rest):
        await bot.send(message="随便你。", event=event)
    else:
        await bot.send(message=f'去{rest[r]}吃吧。', event=event)

what_to_eat = on_regex(pattern="^[去|在](.*)吃[啥|什么]$")


@what_to_eat.handle()
async def pick_menu(bot: Bot, event: Event, state: T_State):
    try:
        f = open(menu_file)
        menu = json.load(f)
        rest = list(dict(menu).keys())
    except Exception as e:
        await bot.send(event, f'获取菜单失败: {e}')
        return

    r = state['_matched_groups'][0]
    if r not in menu:
        if r == '':
            i = random.randint(0, len(rest) - 1)
            j = random.randint(0, len(menu[rest[i]]) - 1)
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

get_menu = on_command('来个菜单')


@get_menu.handle()
async def send_menu(bot: Bot, event: Event):
    try:
        f = open(menu_file)
        menu = dict(json.load(f))
    except Exception as e:
        await bot.send(event, f'获取菜单失败: {e}')
        return
    msg = ''
    for k in menu:
        msg += f"{k}: {','.join(menu[k])}\n"
    print(msg)
    await bot.send(event, msg)

elec_query = on_command("查电费")


@elec_query.handle()
async def query_get_dorm(bot: Bot, event: Event, state: T_State):
    dorm = str(event.get_message()).strip().split(' ')[1]
    if dorm:
        state['dorm'] = dorm


@elec_query.got("dorm", prompt="请输入宿舍号")
async def elec_query_body(bot: Bot, event: Event, state: T_State):
    dorm = state['dorm']

    def convert_to_float(v):
        ret = 0
        try:
            ret = float(v)
        except:
            pass
        return ret

    try:
        em = ElectricityMonitor()
        em.login(config.bupt_username, config.bupt_password)
        res = em.query([dorm])
        if dorm in res:
            data = res[dorm]  # xitucheng
        else:
            data = list(res.values())[0]  # shahe
        if data['areaid'] == 1:  # xitucheng
            msg = f'''校区: 西土城\n宿舍号: {dorm}
剩余电量: {convert_to_float(data['surplus'])+convert_to_float(data['freeEnd'])} kWh
剩余赠送电量: {convert_to_float(data['freeEnd'])} kWh
查询时间: {data['time']}'''
        else:  # shahe
            msg = f'''校区: 沙河
宿舍号: {dorm}
剩余电费: {convert_to_float(data['surplus'])} 元
查询时间: {data['time']}'''
    except Exception as e:
        await elec_query.finish(f"查询失败: {e}")

    await elec_query.finish(msg)

elec_charge = on_command("充电费")


@elec_charge.handle()
async def charge_get_dorm(bot: Bot, event: Event, state: T_State):
    dorm = str(event.get_message()).strip()
    if dorm:
        state['dorm'] = dorm


@elec_charge.got("dorm", prompt="请输入宿舍号")
async def elec_charge_body(bot: Bot, event: Event, state: T_State):
    dorm = state['dorm']

    try:
        em = ElectricityMonitor()
        em.login(config.bupt_username, config.bupt_password)
        qr = qrcode.QRCode(version=1, box_size=1)
        qr.add_data(em.get_recharge_link(dorm))
        img = qr.make_image()
        output_buffer = BytesIO()
        img.save(output_buffer, 'PNG')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)

    except Exception as e:
        await elec_charge.finish(f"获取充值地址失败: {e}")

    await elec_charge.finish(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(base64_str, encoding='utf-8')}"
        }
    }]))
