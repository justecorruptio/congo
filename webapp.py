import web

import settings
from models.utils import Version
from views import (
    urls,
    views,
)

web.config.debug = settings.DEBUG
app = web.application(urls, views)

def set_version():
    web.ctx.version = Version.version
app.add_processor(web.loadhook(set_version))

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
