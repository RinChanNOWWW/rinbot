# rinbot

基于 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 与 [nonebot2](https://github.com/nonebot/nonebot2) 的 QQ 机器人。

## 功能

给巴普特水龙头网定制的功能。

- `\bind CARD`: 将 QQ 与卡号绑定。
- `\recent`: 查看最近一次游戏记录。
- `\today`: 查看今日游玩记录。

## Run

1. 安装依赖

```bash
pip3 install -r requirements.txt
```

2. 在 `.env` 中填入所需参数

```
CQHTTP_WS_URLS={"QQ 号": "ws://127.0.0.1:6700/"}
MYSQL_USER=user
MYSQL_PASSWD=passwd
MYSQL_HOST=ipaddr
```

3. 使用 `nb-cli` 启动 bot

```bash
nb run
```
