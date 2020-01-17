from typing import Optional

from pypi_org.data.users import User
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase
from pypi_org.services import user_service


class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.user: Optional[User] = user_service.find_user_by_id(self.user_id_logged_in)
