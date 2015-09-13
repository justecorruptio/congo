from .index import IndexView
from .game import (
    GameStateView,
    GameVotesView,
)
from .login import (
    LoginView,
    LogoutView,
)
from .sign_up import SignUpView

views = globals()

urls = (
    "/login", "LoginView",
    "/logout", "LogoutView",
    "/signup", "SignUpView",
    "/api/game_state", "GameStateView",
    "/api/game_votes/(.+)", "GameVotesView",
    "/", "IndexView",
)
