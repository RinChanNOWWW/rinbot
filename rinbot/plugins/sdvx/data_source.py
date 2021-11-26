import time
import datetime
from typing import Any, Dict
import sqlalchemy
from sqlalchemy.sql.expression import text

from utils import deserialize

from .config import Config


class UserNotFoundError(Exception):
    pass


class BindError(Exception):
    def __init__(self, err_msg: str) -> None:
        super().__init__(self)
        self.msg = err_msg

    def __str__(self) -> str:
        return self.msg


class NoPlays(Exception):
    pass


class DataBase:
    def __init__(self, config: Config):

        def sqlalchemy_url() -> str:
            return f"mysql://{config.mysql_user}:{config.mysql_passwd}@{config.mysql_host}?charset=utf8mb4"

        self.engine = sqlalchemy.create_engine(
            sqlalchemy_url(),
            pool_recycle=3600,
        )

    def get_user_id(self, card):
        sql = "select userid from bemani.card where id = :card"
        cursor = self.engine.execute(text(sql), card=card)
        if cursor.rowcount != 1:
            raise UserNotFoundError()
        result = cursor.fetchone()
        return result['userid']

    def get_user_id_by_qq(self, qq):
        sql = "select user_id from rinbot. user_info where qq = :qq"
        cursor = self.engine.execute(text(sql), qq=qq)
        if cursor.rowcount != 1:
            raise UserNotFoundError()
        result = cursor.fetchone()
        return result['user_id']

    def bind_user_id_with_qq(self, uid, qq):
        sql = "insert into rinbot. user_info (qq, user_id) values (:qq, :uid)"
        try:
            self.engine.execute(text(sql), qq=qq, uid=uid)
        except sqlalchemy.exc.IntegrityError:
            raise BindError("您已经绑定过卡号了")
        except Exception:
            raise BindError("其他错误")

    def get_recent_scores(self, qq, limit=1):
        sql = "select user_id from rinbot.sdvx_user_info where qq = :qq"
        cursor = self.engine.execute(text(sql), qq=qq)
        if cursor.rowcount != 1:
            raise UserNotFoundError()
        result = cursor.fetchone()
        userid = result['user_id']
        sql = (
            "SELECT DISTINCT(music.name) AS name, music.chart AS chart, music.artist AS artist, music.data AS mus_data, score.points AS points, score.data AS data, score.timestamp AS timestamp " +
            "FROM bemani.score_history AS score, bemani.music AS music " +
            "WHERE score.userid = :userid AND score.musicid = music.id " +
            "AND music.game = 'sdvx' AND music.version = 6 " +
            "ORDER BY timestamp DESC LIMIT :limit"
        )
        cursor = self.engine.execute(text(sql), userid=userid, limit=limit)
        if cursor.rowcount < 1:
            raise NoPlays()
        result = cursor.fetchone()
        return result

    def get_today_scores(self, qq):
        sql = "select user_id from rinbot.sdvx_user_info where qq = :qq"
        cursor = self.engine.execute(text(sql), qq=qq)
        if cursor.rowcount != 1:
            raise UserNotFoundError()
        result = cursor.fetchone()
        userid = result['user_id']
        sql = (
            "SELECT DISTINCT(music.name) AS name, music.chart AS chart, music.artist AS artist, music.data AS mus_data, score.points AS points, score.data AS data, score.timestamp AS timestamp " +
            "FROM bemani.score_history AS score, bemani.music AS music " +
            "WHERE score.userid = :userid AND score.musicid = music.id " +
            "AND music.game = 'sdvx' AND music.version = 6 " +
            "AND timestamp >= :t " +
            "ORDER BY timestamp DESC"
        )
        t = int(time.mktime(datetime.date.today().timetuple()))
        cursor = self.engine.execute(text(sql), userid=userid, t=t)
        if cursor.rowcount < 1:
            raise NoPlays()
        result = cursor.fetchall()
        return result


def format_score(score) -> Dict[str, Any]:
    CLEAR_TYPE_NO_PLAY = 50
    CLEAR_TYPE_FAILED = 100
    CLEAR_TYPE_CLEAR = 200
    CLEAR_TYPE_HARD_CLEAR = 300
    CLEAR_TYPE_ULTIMATE_CHAIN = 400
    CLEAR_TYPE_PERFECT_ULTIMATE_CHAIN = 500
    GRADE_NO_PLAY = 100
    GRADE_D = 200
    GRADE_C = 300
    GRADE_B = 400
    GRADE_A = 500
    GRADE_A_PLUS = 550
    GRADE_AA = 600
    GRADE_AA_PLUS = 650
    GRADE_AAA = 700
    GRADE_AAA_PLUS = 800
    GRADE_S = 900
    CHART_TYPE_NOVICE = 0
    CHART_TYPE_ADVANCED = 1
    CHART_TYPE_EXHAUST = 2
    CHART_TYPE_INFINITE = 3
    CHART_TYPE_MAXIMUM = 4

    mdata = deserialize(score['mus_data'])
    data = deserialize(score['data'])
    stats = data['stats']

    formatted_score = {}
    formatted_score['name'] = score['name']
    formatted_score['artist'] = score['artist']
    formatted_score['difficulty'] = mdata['difficulty']
    formatted_score['critical'] = stats['critical']
    formatted_score['near'] = stats['near']
    formatted_score['error'] = stats['error']
    formatted_score['combo'] = data['combo']
    formatted_score['bpm'] = f"{int(mdata['bpm_min'])}" if mdata['bpm_max'] == mdata[
        'bpm_min'] else f"{int(mdata['bpm_min'])}-{int(mdata['bpm_max'])}"
    formatted_score['score'] = score['points']
    formatted_score['timestamp'] = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(score['timestamp']))
    formatted_score['chart'] = {
        CHART_TYPE_NOVICE: 'NOV',
        CHART_TYPE_ADVANCED: 'ADV',
        CHART_TYPE_EXHAUST: 'EXH',
        CHART_TYPE_INFINITE: 'INF/GRV/HVN/VVD',
        CHART_TYPE_MAXIMUM: 'MXM',
    }.get(score['chart'], 'UNKNOWN')
    formatted_score['grade'] = {
        GRADE_NO_PLAY: 'No Play',
        GRADE_D: 'D',
        GRADE_C: 'C',
        GRADE_B: 'B',
        GRADE_A: 'A',
        GRADE_A_PLUS: 'A+',
        GRADE_AA: 'AA',
        GRADE_AA_PLUS: 'AA+',
        GRADE_AAA: 'AAA',
        GRADE_AAA_PLUS: 'AAA+',
        GRADE_S: 'S',
    }.get(data['grade'], 'No Play')
    formatted_score['clear_type'] = {
        CLEAR_TYPE_NO_PLAY: 'No Play',
        CLEAR_TYPE_FAILED: 'CRASH',
        CLEAR_TYPE_CLEAR: 'Clear',
        CLEAR_TYPE_HARD_CLEAR: 'HC',
        CLEAR_TYPE_ULTIMATE_CHAIN: 'UC',
        CLEAR_TYPE_PERFECT_ULTIMATE_CHAIN: 'PUC',
    }.get(data['clear_type'], 'CRASH')
    return formatted_score
