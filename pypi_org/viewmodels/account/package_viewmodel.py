from pypi_org.services import package_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class PackageViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.package_name = self.request_dict.package_name.strip().lower()
        print(f'self.package_name = {self.package_name}')
        self.package = package_service.get_package_by_id(self.package_name)
        print(f'self.package = {self.package}')
        self.latest_version = "0.0.0"
        self.release_version = None
        self.is_latest = True
        if self.package.releases:
            self.release_version = self.package.releases[0]
            self.latest_version = self.release_version.version_text
        self.release_version = self.latest_version
