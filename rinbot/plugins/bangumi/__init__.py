from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11.event import Event

import aiohttp
from datetime import datetime

class BangumiInfo:
    def __init__(self, name: str, score) -> None:
        self.name = name
        self.score = score

    def __str__(self) -> str:
        if self.score is None:
            return '{} (BGM: 暂无评分)'.format(self.name, self.score)
        else:
            return '{} (BGM: {})'.format(self.name, self.score)

bangumi_today_command = on_command('今日新番')

@bangumi_today_command.handle()
async def bangumi_today(bot: Bot, event: Event):
    today = datetime.today()
    today_weekday = today.weekday()
    bangumi_list: list[BangumiInfo] = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.bgm.tv/calendar') as resp:
                payload = await resp.json()
                items = payload[today_weekday]['items']
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
    except Exception as e:
        print('Error: {}'.format(e))
        await bot.send(event, '获取今日新番表失败')
    else:
        msg = today.strftime('%Y-%m-%d (%A)\n\n')
        msg += '\n'.join(map(str, bangumi_list))
        await bot.send(event, msg)
    
    


