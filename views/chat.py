import json
import random
import redis
import time
import web

from forms import ChatForm
from models import (
    ChatMessage,
    Pretty,
)
from views.utils import (
    is_admin,
    require_admin,
    require_login,
)

def wait_for_message(room_id, timeout=120):
    pubsub = redis.Redis(socket_timeout=timeout).pubsub()
    pubsub.subscribe(['chat.%s' % (room_id,)])
    for i in xrange(5):
        try:
            msg_type, channel, data = pubsub.parse_response()
            if msg_type == 'message':
                return json.loads(data)
        except redis.exceptions.TimeoutError:
            return None, None
    pubsub.unsubscribe()


def signal_message(room_id, action, **kwargs):
    client = redis.Redis()
    client.publish(
        'chat.%s' % (room_id,),
        json.dumps((action, kwargs)),
    )


class ChatView(object):

    @require_login
    def GET(self):
        get_data = web.input(last_id=0)

        last_id = int(get_data.last_id)
        room_id = web.ctx.game.player_color

        messages = []
        delete_id = None
        if last_id == 0:
            messages = ChatMessage.load(room_id, last_id)
        else:
            action, kwargs = wait_for_message(room_id)
            #sleep up to 300 ms to prevent the thundering herd
            time.sleep(random.random() * .3)
            if action == 'send':
                messages = ChatMessage.load(room_id, last_id)
            elif action == 'delete':
                delete_id = kwargs['id']

        deletable = is_admin()

        return json.dumps({
            'messages': list(reversed([
                {
                    'id': x.id,
                    'name': x.name,
                    'rating': Pretty.rating(x.rating),
                    'message': x.message,
                    'deletable': deletable,
                } for x in messages
            ])),
            'refresh': False,
            'delete_id': delete_id,
        })

    @require_login
    def POST(self):
        room_id = web.ctx.game.player_color

        form = ChatForm()
        if not form.validates():
            raise web.notfound(form.note)

        ChatMessage.insert(
            room_id=room_id,
            user_id=web.ctx.user.id,
            message=form.d.message,
        )
        signal_message(room_id, 'send')


    @require_login
    @require_admin
    def DELETE(self):
        get_data = web.input(id=None)
        chat_id = int(get_data.id)

        msg = ChatMessage.get(id=chat_id)
        ChatMessage.update(
            ('id',),
            id=chat_id,
            deleted=1,
        )
        signal_message(msg.room_id, 'delete', id=chat_id)

        return "OK"
