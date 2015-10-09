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
                WHERE game_id = $game_id
                GROUP BY color
            """, vars={
                'game_id': game.id,
            })
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


class GameState(Model):

    table_name = 'Game_States'


class SystemMessage(Model):

    table_name = 'System_Message'
