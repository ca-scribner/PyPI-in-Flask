from typing import Optional

from pypi_org.data.users import User
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase
from pypi_org.services import user_service


class RegisterViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.name: Optional[str] = self.request_dict.name
        self.email_address: Optional[str] = self.request_dict.email_address.lower().strip()
        self.password: Optional[str] = self.request_dict.password.strip()

        self.error: Optional[str] = None
        self.user: Optional[User] = None

    def validate(self):
        if not self.name or\
           not self.email_address or\
           not self.password:
            self.error = "Error: Some fields are missing"
        else:
            if user_service.find_user_by_email(self.email_address):
                self.error = "Error: New user rejected - user already exists with this email address"

    def create_user(self):
        self.user = user_service.create_user(self.name, self.email_address, self.password)
        if not self.user:
            self.error = "Error: New user rejected - invalid password or a user with that email already exists"
