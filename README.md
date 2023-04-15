# rinbot

基于 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 与 [nonebot2](https://github.com/nonebot/nonebot2) 的 QQ 机器人。

## 功能

### SDVX（BUPT 网限定）

- `sdvx_bind CARD`: 将 QQ 与卡号绑定。
- `sdvx_recent`: 查看最近一次游戏记录。
- `sdvx_today`: 查看今日游玩记录。

### BUPT 相关

- `去哪吃`: 去哪个食堂吃饭。
- `去<食堂名>吃啥`: 去某个食堂吃啥。
- `来个菜单`: 查看支持的食堂与菜品。
- `查电费 <宿舍号>`: 查询电费，支持西土城与沙河校区。
- `充电费 <宿舍号>`: 生成充电费微信二维码。

电费相关功能更多信息详见: [OpenBUPT/bupt-elec](https://github.com/OpenBUPT/bupt-elec) (MIT License, forked from [jerrymakesjelly/electricity-monitor](https://github.com/jerrymakesjelly/electricity-monitor))

### MaimaiDX 

- `mai_help`: 使用指南。

Codes copied from: [Diving-Fish/mai-bot](https://github.com/Diving-Fish/mai-bot) (MIT License)

### 搜图

Git submodule: [RinChanNOWWW/nonebot_plugin_imgsearch](https://github.com/RinChanNOWWW/nonebot_plugin_imgsearch) (MIT License, forked from [bakashigure/nonebot_plugin_imgsearch](https://github.com/bakashigure/nonebot_plugin_imgsearch))

## 0. 前提

1. 安装 python (3.8+), go-cqhttp。并运行 go-cqhttp。
2. 在 *rinbot/plugins/bupt* 下创建 *menu.json* 文件，填入食堂与菜品，如:

```json
{
    "新一": ["面", "粥", "自选", "铁板砂锅"],
    "新二": ["面", "自选"],
    "新四": ["大盘鸡拌面", "自选", "酸菜鱼"],
    "老一": ["面", "自选"],
    "老二": ["牛肉汤", "烤肉饭", "大鸡饭", "自选", "盖浇饭", "羊肉烩面"],
    "风味": ["香锅", "魔饭青年", "意面", "粥", "汉堡", "自选"]
}
```

## 1. 使用正向 WS 方式运行 go-cqhttp

config.yaml:

```yaml
# server 部分
servers:
- ws:
  # 正向WS服务器监听地址
  address: 0.0.0.0:8080
  middlewares:
  <<: *default # 引用默认中间件
```

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
BUPT_USERNAME=学号
BUPT_PASSWORD=信息门户密码
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

