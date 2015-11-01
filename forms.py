import re
from web import form

def _set_value(self, value):
    self.value = value.strip()

form.Input.set_value = _set_value


SignUpForm = form.Form(
    form.Textbox('name'),
    form.Textbox('rating'),
    form.Textbox('passwd'),
    validators=[
        form.Validator(
            'Password length too short.',
            lambda i: len(i.passwd) >= 4,
        ),
        form.Validator(
            'Names are only letters and spaces.',
            lambda i: re.match(r"^[-'_ a-zA-Z0-9]+$", i.name),
        ),
        form.Validator(
            'Invalid rating. (30k - 7d)',
            lambda i: (
                i.rating[-1] in 'dD' and 1 <= int(i.rating[:-1]) <= 7
                or
                i.rating[-1] in 'kK' and 1 <= int(i.rating[:-1]) <= 30
            )
        ),
    ],
)

LoginForm = form.Form(
    form.Textbox('name'),
    form.Textbox('passwd'),
    validators=[
        form.Validator(
            'Names are only letters and spaces.',
            lambda i: re.match(r"^[-'_ a-zA-Z0-9]+$", i.name),
        ),
    ],
)

VoteForm = form.Form(
    form.Textbox('pos'),
    form.Textbox('notes'),
    validators=[
        form.Validator(
            'Notes cannot exceed 1000 characters.',
            lambda i: len(i.notes) < 1000,
        ),
    ],
)

ChatForm = form.Form(
    form.Textbox('message'),
    validators=[
        form.Validator(
            'Message cannot exceed 300 characters.',
            lambda i: len(i.message) < 300,
        ),
        form.Validator(
            'Message cannot be empty.',
            lambda i: len(i.message) > 0,
        ),
    ],
)
