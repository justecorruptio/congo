from models.base import Model


class ChatMessage(Model):

    table_name = 'Chat_Messages'

    @classmethod
    def load(cls, room_id, last_id=0):
        messages = cls.db.query("""
            SELECT
                c.id as id,
                u.name as name,
                u.rating as rating,
                c.message as message
            FROM Chat_Messages c
            JOIN Users u ON u.id = c.user_id
            WHERE c.room_id = $room_id
            AND c.id > $last_id
            AND deleted = 0
            ORDER BY id DESC
            LIMIT 20
        """, vars={
            'room_id': room_id,
            'last_id': last_id,
        })
        return messages
