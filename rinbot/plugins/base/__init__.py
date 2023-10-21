from nonebot.adapters import Bot
from nonebot import on_command
from nonebot.rule import to_me

help_command = on_command("help", rule=to_me(), aliases={"帮助", "指南"})


@help_command.handle()
async def help():
    await help_command.finish("康康 https://github.com/RinChanNOWWW/rinbot")
