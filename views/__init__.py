from .index import IndexView
from .game import GameStateView
from .login import (
    LoginView,
    LogoutView,
)
from .sign_up import SignUpView

views = globals()
