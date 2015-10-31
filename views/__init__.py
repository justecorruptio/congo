from .chat import ChatView
from .index import IndexView
from .game import (
    CommentView,
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
from .stats import StatsView

views = globals()

urls = (
    "/login", "LoginView",
    "/logout", "LogoutView",
    "/signup", "SignUpView",

    "/api/comment", "CommentView",
    "/api/game_state", "GameStateView",
    "/api/game_state/(\d+)", "GameStateView",
    "/api/game_votes/(\d+)/(.+)", "GameVotesView",
    "/api/vote", "VoteView",

    "/chat", "ChatView",

    "/sgf", "SgfDownloadView",
    "/stats", "StatsView",

    "/", "IndexView",
)
