from typing import Optional

import flask
from flask import Request

from pypi_org.infrastructure import request_dict, cookie_auth
from pypi_org.infrastructure.request_dict import RequestDictionary
from services.user_service import find_user_by_id


class ViewModelBase:
    def __init__(self):
        # This binds the request for easy reference(?)
        self.request: Request = flask.request
        # This is the pattern Michael made to arrange data differently.  This means we dont need to remember which flask
        # source the data came from (because there's .form, .get, ...)
        self.request_dict: RequestDictionary = request_dict.create('')

        self.error: Optional[str] = None
        # This just gets uid via cookie if possible whenever we instantiate this class
        self.user_id_logged_in: Optional[int] = cookie_auth.get_user_id_via_auth_cookie(self.request)
        if self.user_id_logged_in:
            self.user = find_user_by_id(self.user_id_logged_in)

    def to_dict(self):
        return self.__dict__
