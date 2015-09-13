import web

sub_render = web.template.render(
    'templates',
    globals={
        'web': web,
    },
)

render = web.template.render(
    'templates',
    base='base',
    globals={
        'render': sub_render,
        'web': web,
    }
)
