from models.base import Model


class Comment(Model):
    table_name = 'Comments'

    @classmethod
    def summary(cls, game_id, seq):
        comment_counts = cls.db.query("""
            SELECT
                v.move,
                SUM(1) as cnt
            FROM Comments v
            JOIN Users u ON u.id = v.user_id
            WHERE v.game_id = $game_id
            AND v.seq = $seq
            GROUP BY v.move
            ORDER BY cnt DESC, SUM(u.rating) DESC
            LIMIT 30
        """, vars={
            'game_id': game_id,
            'seq': seq,
        })
        return comment_counts

    @classmethod
    def details(cls, game_id, seq, move):
        comments = cls.db.query("""
            SELECT
                u.name as name,
                u.rating as rating,
                v.notes as notes
            FROM Comments v
            JOIN Users u ON u.id = v.user_id
            WHERE v.game_id = $game_id
            AND v.seq = $seq
            AND v.move = $move
            AND v.notes != ''
            ORDER BY u.rating DESC
            LIMIT 50
        """, vars={
            'game_id': game_id,
            'seq': seq,
            'move': move,
        })
        return comments
