import web

import settings
from views import views

web.config.debug = settings.DEBUG

urls = (
    ".*", "SignUp",
)

app = web.application(urls, views)
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
