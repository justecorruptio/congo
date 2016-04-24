import web

import settings
from models.utils import Version
from views import (
    urls,
    views,
)

web.config.debug = settings.DEBUG
web.config.version = Version.version

app = web.application(urls, views)
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
