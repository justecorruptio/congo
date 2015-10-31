from models.base import Model


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
            LIMIT 20
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
            LIMIT 10
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
