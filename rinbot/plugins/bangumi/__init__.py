from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.exception import FinishedException

from typing import Optional, List
import aiohttp
from datetime import datetime

class BangumiInfo:
    def __init__(self, name: str, score: Optional[str]) -> None:
        self.name = name
        self.score = score

    def __str__(self) -> str:
        if self.score is None:
            return '{} (BGM: 暂无评分)'.format(self.name, self.score)
        else:
            return '{} (BGM: {})'.format(self.name, self.score)

async def get_bangumi_list(weekday: int) -> List[BangumiInfo]:
    bangumi_list: List[BangumiInfo] = []
    async with aiohttp.ClientSession() as session:
            async with session.get('https://api.bgm.tv/calendar') as resp:
                payload = await resp.json()
                items = payload[weekday]['items']
                for item in items:
                    name = item['name_cn']
                    if name == '':
                        name = item['name']
                    if 'rating' in item:
                        score = item['rating']['score']
                    else:
                        score = None
                    bangumi_list.append(BangumiInfo(name, score))
            await session.close()
    return bangumi_list

bangumi_today_command = on_command('今日新番')

@bangumi_today_command.handle()
async def bangumi_today(bot: Bot, event: Event):
    today = datetime.today()
    today_weekday = today.weekday()
    try:
        bangumi_list = await get_bangumi_list(today_weekday)
        msg = today.strftime('%Y-%m-%d (%A)\n\n')
        msg += '\n'.join(map(str, bangumi_list))
        await bot.send(event, msg)
    except Exception as e:
        print('Error: {}'.format(e))
        await bot.send(event, '获取今日新番表失败')
        

bangumi_of_command = on_command('新番表')

@bangumi_of_command.handle()
async def bangumi_of(args: Message = CommandArg()):
    weekday = args.extract_plain_text()
    try:
        weekday = int(weekday)
        if weekday <= 0 or weekday > 7:
            msg = 'Usage: 新番表 [数字] (星期一: 1, ... , 星期日: 7)'
        else:
            bangumi_list = await get_bangumi_list(weekday)
            msg = '\n'.join(map(str, bangumi_list))
    except ValueError:
        msg = 'Usage: 新番表 [数字] (星期一: 1, ... , 星期日: 7)'
    except Exception as e:
        print('Error: {}'.format(e))
        await bangumi_of_command.finish('获取新番表失败')
        
    await bangumi_of_command.finish(msg)
