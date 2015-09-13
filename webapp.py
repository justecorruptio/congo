import web

import settings
from views import (
    urls,
    views,
)

web.config.debug = settings.DEBUG

app = web.application(urls, views)
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
