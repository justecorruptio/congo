import redis
import web

from models.base import Model


class ChatRoom(object):

    @classmethod
    def set_online(cls, room_id):
        key = 'chat.online:%d:%d:%s:%d' % (
            room_id,
            web.ctx.user.id,
            web.ctx.user.name,
            web.ctx.user.rating,
        )
        client = redis.Redis()
        pipeline = client.pipeline()
        pipeline.set(key, "1")
        pipeline.expire(key, 10 * 60)
        pipeline.execute()

    @classmethod
    def get_online(cls, room_id):
        client = redis.Redis()
        matches = client.keys('chat.online:%d:*' % (
            room_id,
        ))

        ret = []
        for match in matches:
            _, room_id, user_id, name, rating = match.split(":")
            user_id = int(user_id)
            rating = int(rating)
            ret.append((user_id, name, rating))

        ret.sort(key=lambda x: x[1].lower())
        return ret


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
            LEFT JOIN Users u ON u.id = c.user_id
            WHERE c.room_id = $room_id
            AND c.id > $last_id
            AND deleted = 0
            ORDER BY id DESC
            LIMIT 100
        """, vars={
            'room_id': room_id,
            'last_id': last_id,
        })
        return messages
