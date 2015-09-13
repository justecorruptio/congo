import web

import settings
from views import views

web.config.debug = settings.DEBUG

urls = (
    "/login", "LoginView",
    "/logout", "LogoutView",
    "/signup", "SignUpView",
    "/api/game_state", "GameStateView",
    "/", "IndexView",
)

app = web.application(urls, views)
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
