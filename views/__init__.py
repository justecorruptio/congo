from .index import IndexView
from .game import (
    GameStateView,
    GameVotesView,
    VoteView,
)
from .login import (
    LoginView,
    LogoutView,
    SignUpView,
)
from .sgf import SgfDownloadView

views = globals()

urls = (
    "/login", "LoginView",
    "/logout", "LogoutView",
    "/signup", "SignUpView",
    "/api/game_state", "GameStateView",
    "/api/game_votes/(.+)", "GameVotesView",
    "/api/vote", "VoteView",
    "/sgf", "SgfDownloadView",
    "/", "IndexView",
)
