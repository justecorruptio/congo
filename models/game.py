import settings
from models.base import Model


class Game(Model):

    STATUS_FINISHED = 20
    STATUS_RUNNING = 10

    table_name = 'Games'

    @classmethod
    def current(cls):
        return cls.get(
            status=cls.STATUS_RUNNING,
        )

    @classmethod
    def join(cls, user_id):
        game = cls.current()
        player = Player.get(user_id=user_id, game_id=game.id)
        if player is None:
            teams = Player.db.query("""
                SELECT color AS color, SUM(1) AS cnt
                FROM Players
                GROUP BY color
            """)
            teams = dict((x.color, x.cnt) for x in teams)
            teams = [(teams.get(x, 0), x) for x in (1, 2)]
            teams.sort()
            color = teams[0][1]

            Player.insert(
                game_id=game.id,
                user_id=user_id,
                color=color,
            )


class Player(Model):

    table_name = 'Players'

    @classmethod
    def game_stats(cls, game_id):
        players = cls.db.query("""
            SELECT
                u.name AS name,
                u.rating AS rating,
                p.color AS color
            FROM Players p
            JOIN Users u ON u.id = p.user_id
            WHERE p.game_id = $game_id
            ORDER BY u.rating DESC
        """, vars={
            'game_id': game_id,
        })
        return players



class Vote(Model):

    table_name = 'Votes'

    @classmethod
    def count(cls, game_id, seq, move):
        cnt = cls.db.query("""
            SELECT COUNT(*) AS cnt
            FROM Votes
            WHERE game_id = $game_id
            AND seq = $seq
            AND move = $move
        """, vars={
            'game_id': game_id,
            'seq': seq,
            'move': move,
        })[0].cnt

        return cnt

    @classmethod
    def details(cls, game_id, seq, move):
        votes = cls.db.query("""
            SELECT
                u.name as name,
                u.rating as rating,
                v.notes as notes
            FROM Votes v
            JOIN Users u ON u.id = v.user_id
            WHERE v.game_id = $game_id
            AND v.seq = $seq
            AND v.move = $move
            AND v.notes != ''
            ORDER BY u.rating DESC
            LIMIT 5
        """, vars={
            'game_id': game_id,
            'seq': seq,
            'move': move,
        })
        return votes

    @classmethod
    def summary(cls, game_id, seq):
        vote_counts = cls.db.query("""
            SELECT
                v.move,
                SUM(1) as cnt
            FROM Votes v
            JOIN Users u ON u.id = v.user_id
            WHERE v.game_id = $game_id
            AND v.seq = $seq
            GROUP BY v.move
            ORDER BY cnt DESC, SUM(u.rating) DESC
            LIMIT 7
        """, vars={
            'game_id': game_id,
            'seq': seq,
        })
        return vote_counts

    @classmethod
    def game_stats(cls, game_id):
        count = cls.db.query("""
            SELECT SUM(1) AS count
            FROM Votes
            WHERE game_id = $game_id
        """, vars={
            'game_id': game_id,
        })[0].count
        return int(count)


class GameState(Model):

    table_name = 'Game_States'


class SystemMessage(Model):

    table_name = 'System_Message'
