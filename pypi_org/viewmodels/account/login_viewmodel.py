from typing import Optional

import flask

from pypi_org.infrastructure import cookie_auth
from pypi_org.data.users import User
from pypi_org.services.user_service import login_user
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class LoginViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.email_address: Optional[str] = self.request_dict.email_address.lower().strip()
        self.password: Optional[str] = self.request_dict.password
        self.user: Optional[User] = None
        self.error: Optional[str] = None

        if not self.email_address or not self.password:
            self.error = "Missing email address or password"

    def login_user(self) -> flask.Response:
        self.user = login_user(self.email_address, self.password)
        if self.user:
            # Redirect to the account page, but do it as a logged in session (where user has a cookie telling us we're in a
            # session)
            resp = flask.redirect("/account")
            cookie_auth.set_auth(resp, self.user.id)
            return resp
        else:
            self.error = "Invalid email address or password"
            return flask.render_template("/account/login.html", **self.to_dict())
