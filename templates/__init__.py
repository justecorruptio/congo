import web

render = web.template.render(
    'templates',
    base='base',
    globals={
        'render': web.template.render(
            'templates',
        ),
    }
)
