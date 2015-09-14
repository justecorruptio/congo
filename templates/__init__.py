import os
import web

import settings

sub_render = web.template.render(
    os.path.join(settings.BASE_DIR, 'templates'),
    globals={
        'web': web,
    },
)

render = web.template.render(
    os.path.join(settings.BASE_DIR, 'templates'),
    base='base',
    globals={
        'render': sub_render,
        'web': web,
    }
)
