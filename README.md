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
电费相关功能更多信息详见: https://github.com/jerrymakesjelly/electricity-monitor

### MaimaiDX 

- `mai_help`: 使用指南。

From: https://github.com/Diving-Fish/mai-bot

## 0. 前提

1. 安装 python, poetry, go-cqhttp。并运行 go-cqhttp。
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

## 1. 运行 bot

1. 使用 peotry 安装需要的依赖

```
poetry install 
```

2. 在 `.env.*` 中填入所需参数

```
CQHTTP_WS_URLS={"QQ 号": "ws://127.0.0.1:6700/"}
MYSQL_USER=user
MYSQL_PASSWD=passwd
MYSQL_HOST=ipaddr
```

### Opt 1. 直接运行

使用 `nb-cli` 启动 bot

```bash
nb run
```

### Opt 2. Docker 部署

```bash
nb deploy
```

或

```bash
sudo docker-compose up -d
```

P.S. peotry 中引入新依赖后需要重新构建镜像:

```bash
sudo docker-compose build
```

## 2. 使用反向代理方式运行 go-cqhttp

config.yaml:

```yaml
# server 部分
servers:
- http:
  host: 127.0.0.1
  port: 5700
  timeout: 5
  middlewares:
    <<: *default
- ws-reverse:
  universal: ws://127.0.0.1:8080/cqhttp/ws
```
