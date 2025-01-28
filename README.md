# rinbot

基于 [NapCatQQ](https://github.com/NapNeko/NapCatQQ) 与 [nonebot2](https://github.com/nonebot/nonebot2) 的 QQ 机器人。

## 功能

### 获取帮助

使用方法：@bot 帮助

### SDVX（BUPT 网限定）

- `sdvx_bind CARD`: 将 QQ 与卡号绑定。
- `sdvx_recent`: 查看最近一次游戏记录。
- `sdvx_today`: 查看今日游玩记录。

### MaimaiDX

- `mai_help`: 使用指南。

Codes copied from: [Diving-Fish/mai-bot](https://github.com/Diving-Fish/mai-bot) (MIT License)

### 搜图

Git submodule: [RinChanNOWWW/nonebot_plugin_imgsearch](https://github.com/RinChanNOWWW/nonebot_plugin_imgsearch) (MIT License, forked from [bakashigure/nonebot_plugin_imgsearch](https://github.com/bakashigure/nonebot_plugin_imgsearch))

### Bangumi

- `今日新番`：列出当日新番。（数据来源：Bangumi）
- `新番表 <星期>`: 列出指定星期的新番表。（星期一：1, ..., 星期日：7）
- 新番推送。See: https://github.com/RinChanNOWWW/blooming

### DeepSeek 集成

Git submodule: [RinChanNOWWW/nonebot_plugin_imgsearch](https://github.com/RinChanNOWWW/nonebot-plugin-deepseek) (MIT License, forked from [KomoriDev/nonebot-plugin-deepseek](https://github.com/KomoriDev/nonebot-plugin-deepseek))

## 0. 前提

1. 安装 python (3.10+), go-cqhttp。并运行 go-cqhttp。

## 1.启动 NapCatQQ 并启动 WS 服务暖

详见文档 https://napneko.github.io/use/integration#nonebot

## 2. 运行 bot

1. 创建虚拟环境并安装依赖

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 在 `.env.*` 中填入所需参数


```
DRIVER=~websockets
ONEBOT_WS_URLS=["ws://<ip>:8080"]
PORT=8081
NICKNAME=["rin", "rinbot", "凛", "芝麻凛", "志摩凛", "志摩凛"]
COMMAND_START=[""]
MYSQL_HOST=mysql_host
MYSQL_USER=user
MYSQL_PASSWD=passwd
SUPERUSERS=["qq", ...]
saucenao_api_key=SAUCENAO_API
```

### Opt 1. 直接运行

使用 `nb-cli` 启动 bot

```bash
nb run
```

### Opt 2. Docker 部署

```bash
nb docker up # https://v2.nonebot.dev/docs/best-practice/deployment
```

或

```bash
sudo docker-compose up -d
```

