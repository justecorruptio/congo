import web

import settings
from views import views

web.config.debug = settings.DEBUG

urls = (
    "/login", "LoginView",
    "/signup", "SignUpView",
    "/", "IndexView",
)

app = web.application(urls, views)
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
